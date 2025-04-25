from flask import Flask, render_template, request, jsonify
from utils.qrFuncs import scan_qr

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    img = request.files['qr_file']

    if img.filename == "":
        return jsonify("No file selected", 400)

    data = scan_qr(img)

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
