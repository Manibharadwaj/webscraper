from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def extract_content(url):
    try:
        # Fetch the webpage
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTP errors

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try to extract the main content by targeting specific elements like <article> or <main>
        main_content = soup.find(['article', 'main'])

        # If main content is not found, fallback to getting all text
        if not main_content:
            main_content = soup.get_text(separator='\n', strip=True)
        else:
            # Clean up the main content text
            main_content = main_content.get_text(separator='\n', strip=True)

        # Optionally, remove ads and unwanted elements
        for ad in soup.find_all(['iframe', 'div', {'class': 'ads'}]):
            ad.decompose()

        return main_content

    except requests.exceptions.RequestException as e:
        return f"Error fetching the webpage: {e}"

@app.route("/", methods=["GET", "POST"])
def home():
    content = None
    if request.method == "POST":
        url = request.form.get("url")
        content = extract_content(url)
    
    return render_template("index.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)
