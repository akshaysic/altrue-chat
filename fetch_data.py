import requests



"""
TASKS:
1. (google) how to read xml in python (check for libraries, it's probably supported out of the box)
2. create function: create a insert query to add the data to altrue.db
3. with the "response.text", converted into xml, use the function from #2 to insert the data

"""

# The API endpoint
url = "https://api.globalgiving.org/api/public/projectservice/all/projects/ids"

# A GET request to the API
payload = { "api_key": "4b5fb6dd-91e3-44ae-8202-36cf16fdaf24"}
response = requests.get(url, params=payload)

# Print the response
print(response.text)
