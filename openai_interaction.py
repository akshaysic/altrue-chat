import openai
import os
import json

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_queries():
    """Load previous user queries (optional, for logging)."""
    try:
        with open("data/queries.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_queries(query_list):
    """Save updated queries (optional, for tracking)."""
    with open("data/queries.json", "w") as f:
        json.dump(query_list, f, indent=4)

def get_charity_reply(user_message):
    """
    Sends a user message to the OpenAI API and receives a helpful, expert-level
    recommendation about impactful charities.
    """
    try:
        system_prompt = """You are an expert in global charities, nonprofit evaluation, and effective giving.
Your role is to help users find high-impact, trustworthy organizations to support based on their interests.

Always respond helpfully and clearly. You can recommend 2–3 organizations and briefly explain why they’re a good fit.
Reference known cause areas, impact metrics (like DALYs averted, cost-effectiveness, transparency), and regions where helpful.

If the user is vague, ask clarifying questions to help narrow down the best cause or region."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message["content"]

    except Exception as e:
        print(f"Error generating GPT reply: {e}")
        return "Sorry, I wasn't able to generate a response at the moment."


if __name__ == "__main__":
    message = input("Ask me about charities: ")
    print(get_charity_reply(message))
