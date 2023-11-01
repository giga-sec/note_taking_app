from flask import Flask, render_template, request, jsonify
from summarizer import summarize

app = Flask(__name__)

@app.route("/")
def index():
    # Do something with the text, such as save it to a database or send it in an email
    print("Started")
    # Return a response to the client
    return render_template("index.html")



@app.route("/add_note", methods=["POST"])
def add_note():
    # Get the text from the textarea tag
    description = request.json["description"]
    # Print the text to the console
    summarized_text = summarize(description)

    # Return a response to the AJAX request
    return jsonify({"summarized_text": summarized_text})



if __name__ == "__main__":
    app.run(debug=True)