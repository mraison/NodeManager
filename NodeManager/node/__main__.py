import sys

from NodeManager.node.app import app


if __name__ == '__main__':
    opt = sys.argv
    opt.pop(0)
    app.run(debug=False, port=int(opt[0]), host='0.0.0.0')
