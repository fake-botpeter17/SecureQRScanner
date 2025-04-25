from google import genai
from flask import Flask, request, jsonify
from os import getenv
from flask_cors import CORS

client = genai.Client(api_key=getenv("GeminiAPI"))

model = "gemini-2.0-flash-lite"

prompt = '''
You are a security expert and your task is to analyze a URL and determine if it is safe or not.
You will be given a URL and your job is to analyze it and provide a response.
If the URL is safe, you will return "Safe". If the URL is unsafe, you will return "Unsafe". Check for the http or https.
You will also provide a reason for your response and a short description of what the URL does.
Example:
Input: https://www.google.com
Output: Safe
Reason: The URL is safe.
Description: The URL is a search engine.
Now, the URL you will be given is: "{}"
'''

app = Flask(__name__)
CORS(app)
@app.route('/scan', methods=['GET'])
def scan():
    url = request.args.get('url')
    print(f"url = {url}")

    response = client.models.generate_content(
        model=model,
        contents=prompt.format(url)
    )
    print(response.text)
    return response.text

if __name__ == '__main__':
    app.run(debug=True, port=5001)
