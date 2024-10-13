from flask import Flask, request, Response


app = Flask(__name__)

global c
c = {}


@app.route("/config", methods=['GET', 'POST'])
def config():
    global c
    if request.method == 'POST':
        c = request.data
        return Response(None, status=200)
    if request.method == 'GET':
        print(c)
        return c

