from flask import Flask,Response
from flask import render_template
from flask import request,redirect, url_for

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)