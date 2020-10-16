import requests
import jsons

url = 'http://cardel.pythonanywhere.com/apiregions/'

response = requests.get(url)

print(response.json())
