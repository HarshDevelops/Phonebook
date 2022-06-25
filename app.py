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
    person_alt_number=db.Column(db.Integer) 

    def __repr__(self) -> str:
        return f"{self.person_name} - {self.person_second_name}"

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
        altphone= (request.form['altphone'])
        if(len(altphone)==0):
            altphone=0
        else:
            altphone=(altphone.replace(" ", ""))
            altphone=int(altphone)
        contact=contactsearch(person_name=first_name, person_second_name=last_name,person_number=phone, person_alt_number=altphone)
        db.session.add(contact)
        db.session.commit()
    allcontact= contactsearch.query.all()
    return render_template('index.html', allcontact=allcontact)


@app.route('/search/elo',methods=['GET', 'POST'])
def index():
    if(request.method=='POST'):
         print("INSIDE POST")
         to_be_found = request.form['contact_search']
         print("tbf: ", to_be_found)
         flag=0
         if(contactsearch.query.filter_by(person_name=to_be_found).all()!=0):
            flag=1
         elif(contactsearch.query.filter_by(person_second_name=to_be_found).all()!=0):
            flag=2
         else:
            flag=3

         if(flag==3):
            allcontact=contactsearch.query.filter_by(person_name=to_be_found).first()
    # allcontact= contactsearch.query.filter_by(person_second_name=to_be_found).all()
    
    return redirect('/')



@app.route('/delete/<int:person_sno>/<int:person_number>')
def delete(person_sno,person_number):
    allcontact= contactsearch.query.filter_by(person_sno=person_sno,person_number=person_number).first()
    db.session.delete(allcontact)
    db.session.commit()
    return redirect('/')


@app.route('/update/<int:person_sno>/<int:person_number>',methods=['GET', 'POST'])
def update(person_sno,person_number):
    if(request.method=="POST"):
        first_name = request.form['first_name']
        phone = ((request.form['phone']).replace(" ", ""))
        phone=int(phone)
        last_name= request.form['last_name']
        altphone= (request.form['altphone'])
        print(altphone)
        print(len(altphone))
        if(len(altphone)==0 or altphone==" "):
            print("got it")
            altphone=0
        else:
            print("got else")
            altphone=(altphone.replace(" ", ""))
            altphone=int(altphone)

        contact=contactsearch(person_name=first_name, person_second_name=last_name,person_number=phone, person_alt_number=int(altphone))
        
        allcontact= contactsearch.query.filter_by(person_sno=person_sno,person_number=person_number).first()
        
        allcontact.person_name=first_name
        allcontact.person_second_name=last_name
        allcontact.person_number=phone
        allcontact.person_alt_number=int(altphone)
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