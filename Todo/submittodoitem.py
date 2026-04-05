from flask import Flask,render_template, request, jsonify
from dotenv import load_dotenv 
import pymongo, os

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db['flask_tutorial']

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')


@app.route("/")
def home():
    message = "Welcome to Todo page - Navigate to /submittodoitem"
    
    return render_template('Todo.html', message=message)

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    if not item_name or not item_description:
        return jsonify({"error": "Item name and description are required"}), 400

    todo_item = {"itemName": item_name, "itemDescription": item_description}
    collection.insert_one(todo_item)

    return jsonify({"message": "To-Do item added successfully!"}), 201

if __name__ == "__main__":
    app.run(debug=True)


