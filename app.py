from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    website = request.form["url"]

    try:
        response = requests.get(website, timeout=5)

        if website.startswith("https://"):
            result = "✅ HTTPS is enabled"
        else:
            result = "⚠️ HTTPS is not being used"

        return f"""
        Website: {website}<br>
        Status Code: {response.status_code}<br>
        {result}
        """

    except requests.exceptions.RequestException:
        return "❌ Could not connect to this website"
        
app.run(debug=True)