import os
from flask import Flask, request, render_template

# Create a Flask web application
app = Flask(__name__)

# Specify the file path where your questions and answers are stored
file_path = "mdcat_questions.txt"

# Check if the file exists
if not os.path.isfile(file_path):
    print("File 'mdcat_questions.txt' not found. Please make sure the file exists in the same directory as this script.")
else:
    # Read questions and answers from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Create a dictionary to store questions and answers
    questions = {}
    current_question = None
    for line in lines:
        line = line.strip()
        if line.startswith("Question"):
            current_question = line[len("Question") + 1:].strip()
        elif line.startswith("Answer"):
            if current_question:
                answer = line[len("Answer") + 1:].strip()
                questions[current_question] = answer
                current_question = None

    # Define a route to handle chatbot interactions
    @app.route("/", methods=["GET", "POST"])
    def chatbot():
        if request.method == "POST":
            user_input = request.form["user_input"]
            response = chatbot_response(user_input, questions)
        else:
            response = "MDCAT Practice Chatbot: Hello! How can I assist you with MDCAT practice questions?"
        return render_template("chatbot.html", response=response)

    # Define a function to get the chatbot's response based on user input and questions
    def chatbot_response(user_input, questions):
        # Directly compare user input with each question
        for question, answer in questions.items():
            if user_input.lower() in question.lower():
                return answer

        return "I'm sorry, I don't have the answer to that question."

    # Run the Flask application
    if __name__ == "__main__":
        app.run(debug=True)
