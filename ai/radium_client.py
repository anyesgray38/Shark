import os


def get_client():
    key = os.getenv("RADIUM_API_KEY")
    if not key:
        return None
    from openai import OpenAI
    return OpenAI(api_key=key, base_url="https://api.radium.cloud/v1")


def ask_research_agent(instruction: str) -> str:
    client = get_client()
    if client is None:
        raise RuntimeError("RADIUM_API_KEY is not configured")
    response = client.chat.completions.create(
        model=os.getenv("RADIUM_MODEL", "hal-1.0"),
        messages=[
            {"role": "system", "content": "You are a Shark Engine research agent. Propose and challenge hypotheses; never claim profitability without quantitative evidence."},
            {"role": "user", "content": instruction},
        ],
    )
    return response.choices[0].message.content
