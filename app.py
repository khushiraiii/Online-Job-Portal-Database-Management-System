from flask import Flask, request, jsonify, render_template,send_file
import mysql.connector
from flask_mysqldb import MySQL
import base64

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '26761117'
app.config['MYSQL_DB'] = 'jobportal'

mysql=MySQL(app)
@app.route("/search",methods=['POST'])
def users():
    q = request.form['job-title']
    
    print(q)
    cur = mysql.connection.cursor()
    cur.execute("""SELECT TITLE, DESCR, PAY, LOCATION, COMPANY, JOB_ID FROM job_postings WHERE TITLE LIKE '%{0}%'""".format(q))
    rv = cur.fetchall()
    l=len(rv)
    print(type(rv))
    return render_template('searchpage.html',result=rv,length=l,flag=1)



#Searching job_application:
@app.route("/application_search",methods=['POST'])
def application_search():
     q = request.form['job-title']
     emp_id=request.form['emp_id']

     cur = mysql.connection.cursor()
     cur.execute("""SELECT * FROM job_postings WHERE TITLE LIKE '%{0}%' AND EMP_ID={1}""".format(q,emp_id))
     rv = cur.fetchall()
     return render_template('search-applicants.html',result=rv,flag=1)

#opening apllication details for page
@app.route("/application_details")
def application_details():
     job_id=request.args.get('job_id')
     cur = mysql.connection.cursor()
     cur.execute("""SELECT * FROM APPLICATION WHERE JOB_ID={0}""".format(job_id))
     rv = cur.fetchall()
     l=len(rv)
     print(rv)
     return render_template('application-details.html',flag=1,result=rv,length=l)

#open particular application
@app.route('/open_application',methods=['POST'])
def open_application():
     app_id=request.args.get('app_id')
     cur = mysql.connection.cursor()
     cur.execute("""SELECT PDF_DATA FROM APPLICATION WHERE APP_ID={0}""".format(app_id))
     file = cur.fetchone()
     print(file)
     file=file[0]
     
     #new_file = base64.b64encode(file).decode('utf-8')
     print(type(file))
     print(file)
     cur.execute("""SELECT * FROM JOB_APPLICANT J,APPLICATION A WHERE APP_ID={0} AND A.USER_ID=J.USER_ID""".format(app_id))
     rv = cur.fetchall()

     return render_template('open-application.html',file=file,result=rv[0],app_id=app_id)







     







'''if __name__=='__main__':
    app.run(debug=True)'''