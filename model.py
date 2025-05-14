import requests

def ask_chatnote(question, context):
    url = "https://chatnote.api.pygen.in/ask"
    data = {
        "question": question,
        "context": context
    }
    try:
        print(f"\nMaking request to {url}")
        print(f"Request data length: Question ({len(question)} chars), Context ({len(context)} chars)")
        
        response = requests.post(url, json=data)
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        
        if response.status_code == 200:
            return response.json().get("answer", "No answer returned.")
        return "Error: " + response.text
    except Exception as e:
        print(f"Error in ask_chatnote: {str(e)}")
        return f"Error: {str(e)}"