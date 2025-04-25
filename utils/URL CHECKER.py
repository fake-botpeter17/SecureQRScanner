from flask import Flask, request, jsonify, redirect
import requests
import re
from os import getenv 

app = Flask(__name__)

# Replace this with your Google Safe Browsing API Key
GOOGLE_API_KEY = getenv('SAFE_URL_API')

def is_url_safe_google(url):
    safe_browsing_url = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}'
    payload = {
        "client": {
            "clientId": "yourapp",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    response = requests.post(safe_browsing_url, json=payload)
    return not response.json().get("matches")

def is_valid_url_format(url):
    regex = re.compile(
        r'^(https?://)?'  # http:// or https://
        r'(([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,})'  # domain
        r'(/[^\s]*)?$',  # optional path
        re.IGNORECASE
    )
    return re.match(regex, url)

@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.json
    url = data.get('url')

    if not is_valid_url_format(url):
        return jsonify({"status": "invalid", "message": "Malformed or suspicious URL format."}), 400

    if is_url_safe_google(url):
        return jsonify({"status": "safe", "redirect": url}), 200
    else:
        return jsonify({"status": "unsafe", "message": "URL is flagged as unsafe!"}), 403

@app.route('/secure_redirect', methods=['GET'])
def secure_redirect():
    url = request.args.get('url')
    if url and is_url_safe_google(url):
        return redirect(url)
    return "<h2>Invalid or unsafe URL!</h2>", 403

if __name__ == '__main__':
    app.run(debug=True)