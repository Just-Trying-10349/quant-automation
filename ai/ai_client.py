import json
import os

from openai import OpenAI


def load_ai_config():
    with open("config/ai_config.json", "r") as file:
        return json.load(file)


def create_client(config):
    """
    Create an OpenAI-compatible client.

    The API key itself NEVER lives in this file.
    """

    environment_variable = config["api_key_env"]

    api_key = os.environ.get(
        environment_variable
    )

    if not api_key:
        raise RuntimeError(
            f"Missing environment variable: "
            f"{environment_variable}"
        )

    return OpenAI(
        base_url=config["base_url"],
        api_key=api_key
    )


def ask_ai(prompt):
    """
    Send the research request to the selected model.
    """

    config = load_ai_config()

    client = create_client(config)

    response = client.chat.completions.create(
        model=config["model"],

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a quantitative research "
                    "and Python strategy analyst."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=config["temperature"],

        max_tokens=config["max_tokens"]
    )

    return response.choices[0].message.content
