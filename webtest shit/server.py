from flask import Flask, render_template
app = Flask(__name__)

global student

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teacher/')
def createRoom():
    student = False

@app.route('/student/')
def enterRoom():
    student = True
    return 'Click.'

if __name__ == '__main__':
  app.run(debug=True)
