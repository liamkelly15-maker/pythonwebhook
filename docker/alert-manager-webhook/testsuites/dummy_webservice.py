#RECEIVE ALERTS NOTIFICATION
import json
from flask import Flask, jsonify, request, render_template, redirect, url_for
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if(request.method == 'POST'):
        app.logger.critical('Headers: %s' ,request.headers)
        app.logger.critical('Body: %s' ,request.get_data())
        with open('/var/tmp/data.txt','w') as outfile:
             json.dump(request.get_json(),outfile)
        data = "hello world"
        return data
# driver function
if __name__ == '__main__':

    app.run(host='0.0.0.0',port='8082')