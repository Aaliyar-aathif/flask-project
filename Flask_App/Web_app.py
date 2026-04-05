from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymongo, os


# Load environment variables
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')

print(f"MongoDB URI: {MONGO_URI}") 

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client.test
collection = db['flask_tutorial']

print("MongoDB connected:", db.name)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = dict(request.form)
    message =''
    success = False

    if not any(form_data.values()):
        message = "Please fill out the form before submitting."
        success = False 
        
        return render_template('index.html', message=message, success=success)
    else:
        try:
            collection.insert_one(form_data)
            message = "Data submitted successfully!"  # Success message
            success = True
        except Exception as e:
            message = f"Error submitting data: {e}"
            success = False

    
    return render_template('submit.html', data=form_data, message=message, success=success)

@app.route('/view')
def view():
    viewdata = collection.find()
    viewdata = list(viewdata)
        
    for item in viewdata:
        del item['_id']

    viewdata = {
        'viewdata' : viewdata
    }
    return viewdata


if __name__ == '__main__':
    app.run(debug=True)

