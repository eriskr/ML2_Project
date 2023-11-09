from flask import Flask, request, render_template
import openai

from dotenv import load_dotenv
import os

load_dotenv()  # This loads the .env file and its variables

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')  # You would create a corresponding HTML file for the chat interface.

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.form['message']
    response = openai.Completion.create(
      engine="davinci",
      prompt=user_message,
      max_tokens=150
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    app.run(debug=True)
