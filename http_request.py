
import requests
def transition(message, note):
    url = "https://antoniompvsarafana.app.n8n.cloud/webhook-test/upload-audio"

    # Two separate strings to send
    data = {
        "message": message,
        "note": note
    }

    response = requests.post(url, data=data)

    print("Status:", response.status_code)
    print("Response body:", response.text)
url = "https://antoniompvsarafana.app.n8n.cloud/webhook-test/upload-audio"

# Two separate strings to send
data = {
    "message": "hello I want to know when my policy began (happy)",
    "note": "912345678"
}

response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Response body:", response.text)
