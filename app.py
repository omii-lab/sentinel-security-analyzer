from flask import Flask, render_template, request
import requests
import ssl
import socket

app = Flask(__name__)
def check_ssl(website):
    try:
        hostname = website.replace("https://", "").replace("http://", "").split("/")[0]

        context = ssl.create_default_context()

        with context.wrap_socket(
            socket.socket(),
            server_hostname=hostname
        ) as sock:
            sock.settimeout(5)
            sock.connect((hostname, 443))

            certificate = sock.getpeercert()

        return "✅ SSL certificate is valid"

    except Exception:
        return "❌ SSL certificate could not be verified"

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
            
        ssl_result = check_ssl(website)

        return f"""
        Website: {website}<br>
        Status Code: {response.status_code}<br>
        {result}<br>
        {ssl_result}
        """

    except requests.exceptions.RequestException:
        return "❌ Could not connect to this website"
        
app.run(debug=True)
