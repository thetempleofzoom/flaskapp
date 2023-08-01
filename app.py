from flask import Flask, render_template

# instance of flask class
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

app.run(debug=True, port=5000)
