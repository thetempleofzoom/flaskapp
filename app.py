from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# instance of flask class
app = Flask(__name__)

app.config["SECRET_KEY"] = "password"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

db = SQLAlchemy(app)


#construct database
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String(80))
    last = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))

#get uploads data, post downloads data
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        #request.form calls 'name' attribute of input class from index.html
        firstname = request.form["first"]
        lastname = request.form["last"]
        email = request.form["email"]
        date = request.form["avail"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        #for radio button, the 'value' variable of the item chosen will be transmitted
        #to occupation
        occupation = request.form["occupation"]

        form=Form(first=firstname, last=lastname, email=email, date=date_obj,
                  occupation=occupation)
        db.session.add(form)
        db.session.commit()

        flash(f"{firstname}, form successfully submitted!")
        

    return render_template("index.html")

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
