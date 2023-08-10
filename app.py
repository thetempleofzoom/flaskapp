from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import pws

# instance of flask class
app = Flask(__name__)

app.config["SECRET_KEY"] = pws.secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = pws.mail_server
app.config["MAIL_PORT"] = pws.mail_port
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = pws.username
app.config["MAIL_PASSWORD"] = pws.password

mail = Mail(app)
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

        #send email
        msg_body = f'''Dear {firstname}, \n Thank you for your online submission on {date_obj.strftime("%d/%m/%Y")}. 
        You have provided the following info:\n
        Name: {firstname} {lastname} \n
        Email: {email} \n
        Occupational Status: {occupation}
        '''
        message = Message(subject="New form submission", sender=app.config["MAIL_USERNAME"],
                          recipients=[email], body=msg_body)
        mail.send(message)

        #show 'submitted' message
        flash(f"{firstname}, form successfully submitted!")
        

    return render_template("index.html")

if __name__ =="__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5000)
