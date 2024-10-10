import os
from dotenv import load_dotenv
from goldenverba.components.interfaces import Generator
from goldenverba.components.types import InputConfig
from goldenverba.components.util import get_environment
import httpx
import json

class CustomGenerator(Generator):
    """
    Custom Generator.
    """

    def __init__(self):
        super().__init__()
        self.name = "Custom"
        self.description = "Using Custom LLM models to generate answers to queries"
        self.context_window = 10000

        try:
            models = getLocalModels()
        except:
            models = ["Cannot fetch available models"]
        
        self.config["Model"] = InputConfig(
            type="dropdown",
            value=models[0],
            description="Select an OpenAI Embedding Model",
            values=models,
        )
        
        self.config["API Key"] = InputConfig(
            type="password",
            value="ollama",
            description="You can set your Custom API Key here or set it as environment variable `OPENAI_API_KEY`",
            values=[],
        )


        self.config["URL"] = InputConfig(
            type="text",
            value="http://192.168.1.107:11434/v1",
            description="You can change the Base URL here if needed",
            values=[],
        )
    

    async def generate_stream(
        self,
        config: dict,
        query: str,
        context: str,
        conversation: list[dict] = [],
    ):
        system_message = config.get("System Message").value
        model = config.get("Model", {"value": "codestral:latest"}).value
        custom_key = get_environment(
            config, "API Key", "CUSTOM_API_KEY", "No Custom API Key found"
        )
        custom_url = get_environment(
            config, "URL", "CUSTOM_BASE_URL", "http://192.168.1.107:11434/v1"
        )
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {custom_key}",
        }
        messages = self.prepare_messages(query, context, conversation, system_message)

        data = {
            "messages": messages,
            "model": model,
            "stream": True
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    f"{custom_url}/chat/completions",
                    json=data,
                    headers=headers,
                    timeout=None,
                ) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            if line.strip() == "data: [DONE]":
                                break
                            json_line = json.loads(line[6:])
                            choice = json_line["choices"][0]
                            if "delta" in choice and "content" in choice["delta"]:
                                yield {
                                    "message": choice["delta"]["content"],
                                    "finish_reason": choice.get("finish_reason"),
                                }
                            elif "finish_reason" in choice:
                                yield {
                                    "message": "",
                                    "finish_reason": choice["finish_reason"],
                                }
        except Exception as e:
            yield {"message": f"Error: {e}", "finish_reason": "error"}

    def prepare_messages(
        self, query: str, context: str, conversation: list[dict], system_message: str
    ) -> list[dict]:
        messages = [
            {
                "role": "system",
                "content": "Hello, I am a custom model. I can help you with your queries.",
            }
        ]

        for message in conversation:
            print(message.content)
            messages.append({"role": message.type, "content": message.content})

        messages.append(
            {
                "role": "user",
                "content": f"Answer this query: '{query}' with this provided context: {context}",
            }
        )

        return messages

import requests

def getLocalModels():
    client = requests.request("GET", "http://192.168.1.107:11434/v1/models")
    models = [model["id"] for model in client.json()["data"]]
    return models
