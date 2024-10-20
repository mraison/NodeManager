from flask import Flask, request, Response

from NodeManager.model import DeviceCollection

app = Flask(__name__)

global c
c = DeviceCollection([])


@app.route("/config", methods=['GET', 'POST'])
def config():
    global c
    if request.method == 'POST':
        c = DeviceCollection.load_from_struct(request.get_json())
        return Response(None, status=200)
    if request.method == 'GET':
        return c.to_struct()

