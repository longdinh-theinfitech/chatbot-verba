import os
import json
from typing import List
import io

import aiohttp
from wasabi import msg

from goldenverba.components.interfaces import Embedding
from goldenverba.components.types import InputConfig
from goldenverba.components.util import get_environment


class CustomEmbedder(Embedding):
    """OpenAIEmbedder for Verba."""

    def __init__(self):
        super().__init__()
        self.name = "Custom"
        self.description = "Vectorizes documents and queries using Custom AI"

        # Fetch available models
        api_key = "ollama"
        base_url = "http://192.168.1.107:11434/v1"
        models = self.get_models(api_key, base_url)

        # Set up configuration
        self.config = {
            "Model": InputConfig(
                type="dropdown",
                value="nomic-embed-text:latest",
                description="Select an Custom Embedding Model",
                values=models,
            )
        }

        # Add API Key and URL configs if not set in environment
        if api_key is None:
            self.config["API Key"] = InputConfig(
                type="password",
                value="",
                description="Custom API Key (or set OPENAI_API_KEY env var)",
                values=[],
            )
        if os.getenv("OPENAI_BASE_URL") is None:
            self.config["URL"] = InputConfig(
                type="text",
                value=base_url,
                description="Custom API Base URL (if different from default)",
                values=[],
            )

    async def vectorize(self, config: dict, content: List[str]) -> List[List[float]]:
        """Vectorize the input content using OpenAI's API."""
        model = config.get("Model", {"value": "nomic-embed-text:latest"}).value
        # api_key = get_environment(
        #     config, "API Key", "OPENAI_API_KEY", "No OpenAI API Key found"
        # )
        base_url = get_environment(
            config, "URL", "OPENAI_BASE_URL", "No OpenAI URL found"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer ollama",
        }
        payload = {"input": content, "model": model}

        # Convert payload to BytesIO object
        payload_bytes = json.dumps(payload).encode("utf-8")
        payload_io = io.BytesIO(payload_bytes)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{base_url}/embeddings",
                    headers=headers,
                    data=payload_io,
                    timeout=30,
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

                    if "data" not in data:
                        raise ValueError(f"Unexpected API response: {data}")

                    embeddings = [item["embedding"] for item in data["data"]]
                    if len(embeddings) != len(content):
                        raise ValueError(
                            f"Mismatch in embedding count: got {len(embeddings)}, expected {len(content)}"
                        )

                    return embeddings

            except aiohttp.ClientError as e:
                if isinstance(e, aiohttp.ClientResponseError) and e.status == 429:
                    raise Exception("Rate limit exceeded. Waiting before retrying...")
                raise Exception(f"API request failed: {str(e)}")

            except Exception as e:
                msg.fail(f"Unexpected error: {type(e).__name__} - {str(e)}")
                raise

    @staticmethod
    def get_models(token: str, url: str) -> List[str]:
        """Fetch available embedding models from OpenAI API."""
        if token is None:
            return [
                "nomic-embed-text:latest"
            ]

        import requests  # Import here to avoid dependency if not needed

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{url}/models", headers=headers)
        response.raise_for_status()
        return [
            model["id"]
            for model in response.json()["data"]
            if "embed" in model["id"]
        ]
