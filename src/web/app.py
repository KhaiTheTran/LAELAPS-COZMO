from flask import Flask, render_template
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main
import cozmo

app = Flask(__name__)


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/api/function1')
def function1():
    main.main()
    return "f1"


@app.route('/api/function2')
def function2():
    return "f2"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
