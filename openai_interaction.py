from openai import OpenAI
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load OpenAI API key from environment variable
#init openai client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# response = client.responses.create(
#     model="gpt-4o-mini",
#     instructions="You are an expert in global charities, nonprofit evaluation, and effective giving.",
#     input="How do I check if a charity is effective?",
# )

#print(response.output_text)

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

        response = client.responses.create(
            model="gpt-4o-mini",
            instructions = "You are an expert in global charities, nonprofit evaluation, and effective giving. Your role is to help users find high-impact, trustworthy organizations to support based on their interests. Always respond helpfully and clearly. You can recommend 2–3 organizations and briefly explain why they’re a good fit. Reference known cause areas, impact metrics (like DALYs averted, cost-effectiveness, transparency), and regions where helpful. If the user is vague, ask clarifying questions to help narrow down the best cause or region.",
            input="How do I check if a charity is effective?",
        )

        return response.output_text

    except Exception as e:
        print(f"Error generating GPT reply: {e}")
        return "Sorry, I wasn't able to generate a response at the moment."


if __name__ == "__main__":
    message = input("Ask me about charities: ")
    print(get_charity_reply(message))
