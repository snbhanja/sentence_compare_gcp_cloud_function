import requests
import json

url = "https://us-central1-braided-lambda-320710.cloudfunctions.net/function-3"

payload = json.dumps({
  "given_answer": "Although rose you feel pain now",
  "correct_answer": "All right, Ross. Look, you're feeling a lot of pain right now"
})
headers = {
  'Authorization': 'Bearer *****',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
