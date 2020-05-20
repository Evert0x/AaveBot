from flask import Flask
import database
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'