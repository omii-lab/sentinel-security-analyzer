from flask import Flask, render_template, request
import requests
import ssl
import socket

app = Flask(__name__)


def check_ssl(website):
    try:
        hostname = website.replace("https://", "").replace("http://", "").split("/")[0]

        context = ssl.create_default_context()

        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                certificate = secure_sock.getpeercert()

        if certificate:
            return "✅ SSL certificate is valid"
        else:
            return "⚠️ SSL certificate information not available"

    except Exception as e:
        return f"❌ SSL check failed: {e}"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/scan", methods=["POST"])
def scan():
    website = request.form["url"].strip()

    # Add HTTPS automatically if the user doesn't provide a protocol
    if not website.startswith(("http://", "https://")):
        website = "https://" + website

    try:
        response = requests.get(
            website,
            timeout=5,
            allow_redirects=True
        )

        # HTTPS check
        if website.startswith("https://"):
            https_result = "✅ HTTPS is enabled"
        else:
            https_result = "⚠️ HTTPS is not being used"

        # SSL check
        ssl_result = check_ssl(website)

        return f"""
        <h2>🛡️ Sentinel Security Analyzer</h2>

        <p><b>Website:</b> {website}</p>

        <p><b>Status Code:</b> {response.status_code}</p>

        <p>{https_result}</p>

        <p>{ssl_result}</p>
        """

    except requests.exceptions.RequestException as e:
        return f"""
        <h2>🛡️ Sentinel Security Analyzer</h2>
        <p>❌ Could not connect to this website.</p>
        <p>Error: {e}</p>
        """


if __name__ == "__main__":
    app.run(debug=True)
