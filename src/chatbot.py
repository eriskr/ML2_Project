from flask import Flask, request, render_template, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Load the OpenAI API key from the environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Confirm the API key is present
if not openai.api_key:
    raise ValueError("No OpenAI API key found. Set the OPENAI_API_KEY environment variable.")

# Global variable to store the current historical figure
current_historical_figure = None

# Route to serve the HTML page
@app.route("/")
def index():
    global current_historical_figure
    current_historical_figure = None  # Reset at the start of each session
    return render_template('index.html')

# Route to handle sending messages to OpenAI and getting the response
@app.route("/ask", methods=["POST"])
def ask():
    global current_historical_figure
    try:
        data = request.get_json()
        user_message = data['message']

        # Check if setting a new historical figure
        if not current_historical_figure:
            current_historical_figure = user_message
            return jsonify(f"You are now talking to {current_historical_figure}. What would you like to ask?")

        # Prepare the prompt for the OpenAI API call
        prompt = (f"Imagine you are {current_historical_figure}, speaking in the present day. As {current_historical_figure}, "
          f"you're sharing your thoughts, experiences, and insights in response to the user's questions. Your responses should be "
          f"reflective of your historical knowledge, personal experiences, and unique perspective, just as if {current_historical_figure} were "
          f"here to answer them. Engage in the conversation naturally and insightfully.\n\n"
          f"Question: {user_message}\nResponse:")

        # Make the API call to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are {current_historical_figure}."},
                {"role": "user", "content": user_message},
            ]
        )

        # Extract the response text
        bot_response = response['choices'][0]['message']['content']

        # Return the bot response as JSON
        return jsonify(bot_response)

    except Exception as e:
        # Log the exception message
        app.logger.error(f'An error occurred: {e}')

        # Return a JSON error message
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
