from app import users,application_search, application_details,open_application, send_file
from login import login_check, login_verify
from entrydetails import new_entry
from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_mysqldb import MySQL
import io

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '26761117'
app.config['MYSQL_DB'] = 'jobportal'


mysql=MySQL(app)

#Check details for registering or logging into account from login page
@app.route("/login",methods=['POST'])
def login_run():
    return login_check()


#Throw search results from search box
@app.route("/search",methods=['POST'])
def app_run():
    return users(   )


#Load register/login page from home page (index.html)
@app.route("/login1")
def open_login():
    return render_template('login.html',error='',f=0)

#Performing Validation check on entry form for new users
@app.route("/entry",methods=['POST'])
def entry_details_check():
    return new_entry()

#Opening Job details page for appying
@app.route("/job_details")
def job_display():
    job_id=request.args.get('job_id')
    cur = mysql.connection.cursor()
    cur.execute("""SELECT * FROM job_postings WHERE JOB_ID='{0}'""".format(job_id))
    rv = cur.fetchall()
    print(rv,job_id)
    return render_template('job-details.html',results=rv[0])

#To verify and apply for job
@app.route("/apply")
def apply():
    job_id=request.args.get('job_id')
    print("The job_id =",job_id)
    return render_template('verification_apply.html',f=0,job_id=job_id)

@app.route("/login_verify",methods=['POST'])
def login_verify1():
    
    return login_verify()


#Searching job_application:
@app.route("/application_search",methods=['POST'])
def application_search1():
    
    return application_search()

@app.route("/application_details")
def application_details1():
    return application_details()


#To view an application
@app.route('/open_application')
def open_application1():
    return open_application()

@app.route('/download')
def download_file():
     app_id=request.args.get('app_id')
     print(app_id)
     cur = mysql.connection.cursor()
     cur.execute("""SELECT PDF_DATA FROM APPLICATION WHERE APP_ID={0}""".format(app_id))
     file = cur.fetchone()[0]
     print(file)
     file = io.BytesIO(file)
     return send_file(file, mimetype='application/pdf', as_attachment=True,download_name='resume.pdf')
     """with open('output_file.jpg', 'wb') as f:
        f.write(file.read())
        f.save(f.filename)
     return send_file(file, mimetype='image/jpeg')"""


if __name__=='__main__':
    app.run(debug=True)
