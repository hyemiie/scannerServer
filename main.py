from flask import Flask, jsonify, request, json
import os
import dotenv

dotenv.load_dotenv()
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPEN_ROUTER_AI_KEY") 


@app.route('/get_suggestions', methods = ['POST'])
def get_ai_suggestion():
    try:
        data = request.json
        issue_text =  data.get('issue_text')
        code_snippet =  data.get('code_snippet')
        print('code', code_snippet, issue_text)

        
        if not OPENROUTER_API_KEY:
            return jsonify({"error": "API key not configured on the backend"}), 500

        prompt = f"""🔒 Security Issue:
        

    Issue: {issue_text}

    Code:
    {code_snippet}

    🔧 Suggest a concise fix (max 5 lines of code) and a 1-line explanation. Skip extra details or long best practices.
    """

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/mistral-7b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()
            reply = response.json()
            return jsonify({"content": reply["choices"][0]["message"]["content"]})

        except Exception as e:
            return f"AI request failed: {str(e)}"
    except Exception as e:
            return f"AI Service failed"

port = int(os.environ.get("PORT", 5000)) 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

        

        


