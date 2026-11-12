
import requests

user_message = "Hi How are you?"

request_message = {
    "message": user_message
}

url = "https://sidd-workflows.app.n8n.cloud/webhook/18126197-4367-4e48-b877-f46177eda12b"

response = requests.post(
    url,
    json={"message": user_message}
)

print("Status:", response.status_code)

if response.status_code == 200:
    data = response.json()
    print("AI Response:", data["output"])
else:
    print(response.text)