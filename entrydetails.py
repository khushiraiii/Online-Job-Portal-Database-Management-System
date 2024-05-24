from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_mysqldb import MySQL
from datetime import datetime
import re

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '26761117'
app.config['MYSQL_DB'] = 'jobportal'

mysql=MySQL(app)

@app.route("/entry",methods=['POST'])
def new_entry():

    user_id=request.form['user_id']
    print("The user id is =",user_id)

    dob = request.form['dob']
    dob_date = datetime.strptime(dob, '%Y-%m-%d')
    current_date = datetime.now()
    if dob_date >= current_date:
        error = "Date of birth must be in the past."
        return render_template('newentry.html', error=error,f=1)
    
    
    #Check Name
    Name=request.form['name']
    pattern = r'^[a-zA-Z\s]+$'  # Matches only alphabetic characters and whitespace
    match = re.search(pattern, Name)

    if(match==None):
        print(Name)
        error = "Name field contains special characters or number."
        return render_template('newentry.html', error=error,f=1)
    

    #Check Valid phone number
    phone_number=request.form['phoneno']
    pattern = r'^\d{10}$'  # Matches exactly 10 digits
    
    # Check if the phone number matches the pattern
    if(re.match(pattern, phone_number)==None):
        error = "Enter Valid Phone NUmber."
        return render_template('newentry.html', error=error,f=1)
    addr=request.form['addr']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE JOB_APPLICANT SET FULLNAME='{0}',PHONE_NO='{1}',ADDRESS='{2}',DOB='{3}' WHERE USER_ID={4}""".format(Name,phone_number,addr,dob,user_id))
    mysql.connection.commit()
    print("Successful sign up!")
 
    return render_template('searchpage.html')
