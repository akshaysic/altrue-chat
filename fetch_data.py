# fetch_data.py

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GLOBAL_GIVING_API_KEY")
BASE_URL = "https://api.globalgiving.org/api/public/projectservice"
HEADERS = {"Accept": "application/json"}


def search_projects(query, start=0, max_results=5):
    """
    Search for projects on GlobalGiving by keyword.

    Args:
        query (str): Search keyword like "education", "women", etc.
        start (int): Pagination offset (default 0).
        max_results (int): Maximum number of projects to return.

    Returns:
        list: List of project dicts with basic info.
    """
    url = f"{BASE_URL}/search/projects"
    params = {
        "q": query,
        "api_key": API_KEY,
        "start": start
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("projects", {}).get("project", [])[:max_results]
    except requests.RequestException as e:
        print(f"Search error: {e}")
        return []


def get_project_details(project_id):
    """
    Fetch a single project's full details from GlobalGiving.

    Args:
        project_id (str or int): The project ID from search results.

    Returns:
        dict: Detailed project information.
    """
    url = f"{BASE_URL}/projects/{project_id}"
    params = {"api_key": API_KEY}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("project", {})
    except requests.RequestException as e:
        print(f"Detail fetch error: {e}")
        return {}
