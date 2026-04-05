from flask import Flask, jsonify, render_template
import json

app = Flask(__name__)

@app.route("/")
def home():
   return render_template('index.html')


@app.route('/api')
def get_data():
    file = open('data.json','r')
    data = json.load(file)
    file.close()
    return render_template('api.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
