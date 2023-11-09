from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from summarizer import summarize
import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.String(20))

def create_database():
    """
    Create a database using the current app context and create all the necessary tables.

    This function does not take any parameters.

    This function does not return any values.
    """
    with app.app_context():
        db.create_all()

@app.route('/notes', methods=['GET'])
def get_notes():
    """
    Retrieves all notes from the database and returns them as a JSON response.

    Parameters:
        None

    Returns:
        A JSON response containing all the notes in the database.
    """
    notes = Note.query.all()
    notes_data = []
    for note in notes:
        notes_data.append({
            'id': note.id,
            'title': note.title,
            'description': note.description,
            'date': note.date
        })
    return jsonify(notes_data)

@app.route('/notes', methods=['POST'])
def add_note():
    """
    Adds a new note to the database.

    Parameters:
        None

    Returns:
        A JSON response containing the ID, title, description, and date of the added note.
    """
    print("GET")
    data = request.get_json()
    title = data['title']
    description = data['description']
    date = data['date']
    note = Note(title=title, description=description, date=date)
    db.session.add(note)
    db.session.commit()
    return jsonify({
        'id': note.id,
        'title': note.title,
        'description': note.description,
        'date': note.date
    })


@app.route('/notes/<int:id>', methods=['GET'])
def get_single_note(id):
    """
    Update a note with the given ID.

    Parameters:
        id (int): The ID of the note to be updated.

    Returns:
        dict: A dictionary containing the updated note's ID, title, description, and date.
    """
    print("GET SINGLE NOTE")
    if request.method == 'GET':
        # Handle the GET request to fetch the note contents
        note = Note.query.get(id)
        return jsonify({
            'id': note.id,
            'title': note.title,
            'description': note.description,
            'date': note.date
        })



@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    if request.method == 'PUT':
        # Handle the PUT request to update the note
        print(f"Received PUT request for note ID:hat {id}")
        data = request.get_json()
        print(f"Received data for note ID {id}: {data}")
        note = Note.query.get(id)
        if note:
            note.title = data.get('title', note.title)
            note.description = data.get('description', note.description)
            note.date = data.get('date', note.date)
            db.session.commit()
            return jsonify({
                'id': note.id,
                'title': note.title,
                'description': note.description,
                'date': note.date
            })
        else:
            return jsonify({'message': 'Note not found'}), 404

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    """
    Deletes a note with the given ID.

    Parameters:
        id (int): The ID of the note to be deleted.

    Returns:
        dict: A JSON object with a message indicating that the note was deleted successfully.
    """
    note = Note.query.get(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'})


@app.route("/")
def index():
    print("Started")
    # Return a response to the client
    return render_template("index.html")


if __name__ == "__main__":
    create_database()  # Create the table if it doesn't exist
    app.run(debug=True)