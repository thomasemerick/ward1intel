import requests, json

url = "https://maps2.dcgis.dc.gov/dcgis/rest/services/DCGIS_DATA/Administrative_Other_Boundaries_WebMercator/MapServer?f=json"
response = requests.get(url)
data = response.json()
for layer in data.get('layers', []):
    print(layer['id'], layer['name'])
