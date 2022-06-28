from email.policy import default
from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///swiftskuharsh.db"
app.config['SQLALCHEMY_TRACK_NOTIFICATIONS']=False
db=SQLAlchemy(app)

class contactsearch(db.Model):
    person_sno = db.Column(db.Integer, primary_key=True)
    person_name=db.Column(db.String(50), nullable=False)
    person_second_name=db.Column(db.String(100))
    person_number=db.Column(db.Integer) 
    person_email=db.Column(db.String(50), nullable=True)

    def __repr__(self) -> str:
        return f"{self.person_name} - {self.person_second_name}"

#This section is to enter new contact details
@app.route('/' ,methods=['GET', 'POST'])
def indexx():
    if(request.method=='POST'):
        first_name = request.form['first_name']
        phone = ((request.form['phone']).replace(" ", ""))
        if((contactsearch.query.filter_by(person_number=phone).first())!=None):
            flash('A contact with this phone number already exists')
            
        else:
            phone=int(phone)
        last_name= request.form['last_name']
        email= (request.form['email'])
        contact=contactsearch(person_name=first_name, person_second_name=last_name,person_number=phone, person_email=email)
        db.session.add(contact)
        db.session.commit()
    allcontact= contactsearch.query.all()
    return render_template('index.html', allcontact=allcontact)


#Section to delete contact
@app.route('/delete/<int:person_sno>/<int:person_number>')
def delete(person_sno,person_number):
    allcontact= contactsearch.query.filter_by(person_sno=person_sno,person_number=person_number).first()
    db.session.delete(allcontact)
    db.session.commit()
    return redirect('/')

#Section to update a contact
@app.route('/update/<int:person_sno>/<int:person_number>',methods=['GET', 'POST'])
def update(person_sno,person_number):
    if(request.method=="POST"):
        first_name = request.form['first_name']
        phone = ((request.form['phone']).replace(" ", ""))
        phone=int(phone)
        last_name= request.form['last_name']
        email= (request.form['email'])
        if(len(email)==0):
            print("inseide")
            email=" "
        else:
            email=email
        
        print(email)
        contact=contactsearch(person_name=first_name, person_second_name=last_name,person_number=phone, person_email=email)
        
        allcontact= contactsearch.query.filter_by(person_sno=person_sno,person_number=person_number).first()
        
        allcontact.person_name=first_name
        allcontact.person_second_name=last_name
        allcontact.person_number=phone
        allcontact.person_dmail=email
        db.session.add(allcontact)
        db.session.commit()
        flash("Contact Successfully Updated!")
        return redirect("/")

    allcontact= contactsearch.query.filter_by(person_sno=person_sno,person_number=person_number).first()
    return render_template('update.html', allcontact=allcontact)

@app.route('/new')
def fulldetails():
    allcontact= contactsearch.query.all()
    print(allcontact)
    return render_template('result.html')


if __name__ =="__main__":
    app.run(debug=True)