from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import os
import base64
from config import key
app = Flask(__name__)
app.config["MONGO_URI"] = key
mongo = PyMongo(app)



@app.route("/")
def main():
    return render_template("login.html")

database = {"Pranav":"Pranav@369"}

@app.route("/Home", methods=["POST"])
def login():
    name = request.form.get('username')
    password = request.form.get('password')
    if name not in database:
        return render_template('login.html',info="Invalid Username or Password")
    elif database[name] != password:
        return render_template('login.html',info="Invalid Username or Password")
    else:
        return render_template('home.html')
    

@app.route("/home.html", methods=["POST"])
def insert():
    image = request.files.get('image')
    pnr_number = request.form.get('pnr_number')
    seat_number = request.form.get('seat_number')
    student_name = request.form.get('student_name')
    roll_no = request.form.get('roll_no')
    email_id = request.form.get('email_id')
    date_of_birth = request.form.get('date_of_birth')

    if image:
        image_data = image.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')

        mongo.db.students.insert_one({
            "image_data": image_base64,
            "pnr_number": pnr_number,
            "seat_number": seat_number,
            "student_name": student_name,
            "roll_no": roll_no,
            "email_id": email_id,
            "date_of_birth": date_of_birth
        })

    return render_template('home.html', info="Successfully Data has been Submitted")



@app.route("/Add Student")
def add_page():
    return render_template("add.html")

@app.route("/Home")
def home():
    return render_template("/home.html")

@app.route("/students", methods=["GET"])
def students():
    student = mongo.db.students.find({})
    return render_template("students.html", student=student)

@app.route("/Report")
def report():
    return render_template("/report.html")

@app.route("/students/update/<string:pnr_number>", methods=["GET", "POST"])
def update(pnr_number):
    if request.method == 'POST':
        image = request.files.get('image')
        pnr_number = request.form.get('pnr_number')
        seat_number = request.form.get('seat_number')
        student_name = request.form.get('student_name')
        roll_no = request.form.get('roll_no')
        email_id = request.form.get('email_id')
        date_of_birth = request.form.get('date_of_birth')
        if image:
            image_data = image.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        
        mongo.db.students.update_one(
            {"pnr_number": pnr_number}, 
            {"$set": {
                "image_data": image_base64,
                "seat_number": seat_number,
                "student_name": student_name,
                "roll_no": roll_no,
                "email_id": email_id,
                "date_of_birth": date_of_birth
            }}
        )

        return redirect("/students")  

    else:
        update_student = mongo.db.students.find_one({"pnr_number": pnr_number})
        return render_template("/update.html", update_student=update_student)



@app.route("/students/delete/<string:pnr_number>", methods=["GET"])
def delete(pnr_number):
    mongo.db.students.delete_one({"pnr_number": pnr_number})
    return redirect("/students")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
