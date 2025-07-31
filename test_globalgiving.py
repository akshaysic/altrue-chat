import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GLOBALGIVING_API_KEY")

def fetch_projects(search_term="clean water"):
    url = f"https://api.globalgiving.org/api/public/projectservice/projects/search?api_key={API_KEY}&q={search_term}"
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Save a sample
        with open("data/sample_projects.json", "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, indent=2)
        print("Sample project data saved to data/sample_projects.json ✅")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

fetch_projects("education india")
