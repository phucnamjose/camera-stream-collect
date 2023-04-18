import requests
import json

api_url = "https://chartimap1.sha.maryland.gov/arcgis/rest/services/CHART/Cameras/MapServer/0/query?outFields=*&where=1%3D1&f=geojson"
response = requests.get(api_url)
status = response.status_code
content_type = response.headers["Content-Type"]

print(status)
print(content_type)
if status == 200:
    data = response.json()
    with open("cameras.json", "w") as outfile:
        outfile.write(json.dumps(data, indent = 4))

