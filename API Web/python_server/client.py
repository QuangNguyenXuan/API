import requests

resp = requests.post("http://0.0.0.0:5000/predict",
                     files={"file": open('ants.jpg','rb')})

print(resp.json())