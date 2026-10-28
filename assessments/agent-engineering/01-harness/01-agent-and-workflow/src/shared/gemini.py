"""Gemini API plumbing; no workflow or agent control flow."""

import argparse
import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv(Path(__file__).resolve().parents[6] / ".env")


def generate(prompt: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY in the repository root .env.")

    with genai.Client(api_key=api_key) as client:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL") or "gemini-flash-latest",
            contents=prompt,
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            ),
        )
    if not response.text:
        raise RuntimeError("Gemini returned no text.")
    return response.text


class BudgetExceeded(RuntimeError):
    """A local run limit was reached; callers must stop rather than retry."""


class GeminiRun:
    """Explicit JSON requests with accounting; no SDK-managed agent loop."""

    def __init__(self):
        self.model = os.getenv("GEMINI_MODEL") or "gemini-flash-latest"
        self.max_steps = int(os.getenv("MAX_STEPS") or 12)
        self.max_tokens = int(os.getenv("MAX_TOKENS_PER_RUN") or 100_000)
        seconds = float(os.getenv("MAX_WALLCLOCK_SECONDS") or 300)
        if min(self.max_steps, self.max_tokens, seconds) <= 0:
            raise ValueError("Run limits must be positive.")
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Set GEMINI_API_KEY in the repository root .env.")
        self.started = time.monotonic()
        self.deadline = self.started + seconds
        self.tokens = 0
        self.calls = []
        self.client = genai.Client(api_key=api_key)

    def remaining(self) -> float:
        remaining = self.deadline - time.monotonic()
        if remaining <= 0:
            raise BudgetExceeded("Wall-clock limit reached.")
        return remaining

    def http_options(self):
        return types.HttpOptions(
            timeout=max(1, int(self.remaining() * 1000)),
            retry_options=types.HttpRetryOptions(attempts=1),
        )

    def ask(self, contents: list[types.Content], schema: type[BaseModel], output_tokens=12_000):
        if len(self.calls) >= self.max_steps:
            raise BudgetExceeded("Model-step limit reached.")
        # Put the schema in counted content: Developer API count_tokens does
        # not support system instructions/tools/generation_config.
        request = [*contents, types.Content(role="user", parts=[types.Part.from_text(
            text="Return only JSON matching this schema:\n" + json.dumps(schema.model_json_schema())
        )])]
        count = self.client.models.count_tokens(
            model=self.model, contents=request,
            config=types.CountTokensConfig(http_options=self.http_options()),
        ).total_tokens
        if count is None:
            raise RuntimeError("Provider did not return an input token count.")
        available = self.max_tokens - self.tokens - count - 256
        if available < 512:
            raise BudgetExceeded("Insufficient token budget for another response.")
        record = {"step": len(self.calls) + 1, "input_tokens": count}
        self.calls.append(record)  # Failed requests consume a step too.
        response = self.client.models.generate_content(
            model=self.model, contents=request,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                max_output_tokens=min(output_tokens, available),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                http_options=self.http_options(),
            ),
        )
        usage = response.usage_metadata
        actual = usage.total_token_count if usage else None
        if actual is None:
            raise RuntimeError("Missing usage metadata; cannot continue budget accounting.")
        self.tokens += actual
        record.update(total_tokens=actual, elapsed_seconds=round(time.monotonic() - self.started, 2))
        self.remaining()
        if self.tokens > self.max_tokens:
            raise BudgetExceeded("Actual provider usage exceeded the reserved token budget.")
        if not response.text:
            raise RuntimeError("Gemini returned no text.")
        return response

    def summary(self):
        return {"model": self.model, "tokens": self.tokens, "calls": self.calls,
                "elapsed_seconds": round(time.monotonic() - self.started, 2)}

    def close(self):
        self.client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send one prompt to Gemini.")
    parser.add_argument("prompt")
    print(generate(parser.parse_args().prompt))
