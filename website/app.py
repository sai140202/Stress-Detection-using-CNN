from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/userpage')
def page():
    return render_template('userpage.html')

@app.route('/my-link/')
def my_link():
   subprocess.call(["python", "C:\\Users\\shadow\\OneDrive\\Desktop\\python\\Final Year Project\\testStressDetector.py"])
   return render_template('userpage.html')


if __name__ == '__main__':
    app.run(debug= True)