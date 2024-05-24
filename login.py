from flask import Flask, request, jsonify, render_template, send_file
import mysql.connector
from flask_mysqldb import MySQL
from io import BytesIO
from datetime import datetime

app = Flask(__name__,template_folder='templates', static_folder='static')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '26761117'
app.config['MYSQL_DB'] = 'jobportal'

mysql=MySQL(app)

@app.route("/login",methods=['POST'])
def login_check():
    if 'login' in request.form:
        u_name = request.form['txt']
        psw =request.form['pswd']
        print(u_name,psw)
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM login WHERE USERNAME LIKE '{0}' AND PASSWRD LIKE '{1}'""".format(u_name,psw))
        rv = cur.fetchall()
        l=len(rv)
        if l==0:
         
            error='Invalid Login Credentials!'
            return render_template('login.html',error=error,f=1)
        else:
          cur.execute("""SELECT * FROM JOB_APPLICANT WHERE USERNAME LIKE '{0}'""".format(u_name))
          rv = cur.fetchall()
          l=len(rv)
          if l!=0:
            return render_template('searchpage.html',f=0)
          else:
             return render_template('search-applicants.html',f=0)
        
    elif 'signup' in request.form:
        u_name = request.form['txt1']
        psw =request.form['pswd1']
        e_mail=request.form['email1']
        print(u_name,psw,e_mail)
        cur = mysql.connection.cursor()
        f=True
        cur.execute("""SELECT * FROM login WHERE USERNAME LIKE '{0}' OR MAIL LIKE '{1}'""".format(u_name,e_mail))
        chk=cur.fetchall()
        if len(chk)!=0:
            return render_template('login.html',error='username or mail already exists',f=1)
        
        cur.execute("""INSERT INTO LOGIN VALUES('{0}','{1}','{2}')""".format(u_name,psw,e_mail))
        mysql.connection.commit()
        i=0
        cur.execute("""SELECT USER_ID FROM JOB_APPLICANT""")
        print(chk,type(chk))
        user_ids = [row[0] for row in cur.fetchall()]
        while(True):
            e=1
            for j in user_ids:
                if j==i:
                    i+=1
                    e=0
                    break
            if e==1:
                break

        cur.execute("""INSERT INTO JOB_APPLICANT(USER_ID, USERNAME, MAIL_ID) VALUES('{0}','{1}','{2}')""".format(i,u_name,e_mail))
        mysql.connection.commit()
        print("Successful sign up!")
        return render_template('newentry.html',f=0,user_id=i)

@app.route("/login_verify",methods=['POST'])
def login_verify():
    if 'login' in request.form:
        job_id=request.form['job_id']
        print("The job_id 2=",job_id)

        u_name = request.form['txt']
        psw =request.form['pswd']
        print(u_name,psw)
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM login WHERE USERNAME LIKE '{0}' AND PASSWRD LIKE '{1}'""".format(u_name,psw))
        rv = cur.fetchall()
        l=len(rv)
        if l==0:
            error='Invalid Login Credentials!'
            return render_template('verification_apply.html',error=error,f=1)
        else:

            #get User id
            cur.execute("""SELECT USER_ID FROM job_applicant WHERE USERNAME LIKE '{0}'""".format(u_name))
            rv = cur.fetchall()
            user_id=rv[0]
            user_id=user_id[0]
            print(user_id)

            #Check if same applicant is submitting twice
            cur.execute("""SELECT USER_ID FROM APPLICATION WHERE USER_ID={0} AND JOB_ID={1}""".format(user_id,job_id))
            rv = cur.fetchall()
            print(rv)
            
            if rv:
              error="Applicant has already submitted for this Job!"
              return render_template('verification_apply.html',error=error,f=1)

            i=0
            cur.execute("""SELECT APP_ID FROM APPLICATION""")
            app_ids = [row[0] for row in cur.fetchall()]
            while(True):
             e=1
             for j in app_ids:
                if j==i:
                    i+=1
                    e=0
                    break
             if e==1:
                break
     
            file = request.files['pdf_file']
            print(type(file))
            print("content_type =", file.content_type)
            print("content_length =", file.content_length)
            #file.save('/' + file.filename)
            #return send_file(file, mimetype='application/pdf', as_attachment=True,download_name='resume.pdf')
            print(file.filename)
            today = datetime.today()
            print(type(job_id))

            # Format the date as a string in the format YYYY-MM-DD
            formatted_date = today.strftime('%Y-%m-%d')
            cur.execute("INSERT INTO APPLICATION (APP_ID,PDF_DATA) VALUES(%s, %s )",(i,file))
            mysql.connection.commit()
            cur.execute("""UPDATE APPLICATION SET JOB_ID={0}, USER_ID={1}, STATUS='{2}', DOS='{3}' WHERE APP_ID={4}""".format(job_id, user_id, 'NEW', formatted_date,i))
            mysql.connection.commit()
            print("Successful application!")
            # Save the uploaded PDF file to a desired location
            return render_template('searchpage.html',f=0)
            #else:
            #error='Upload PDF File!'
            #return render_template('verification_apply.html',error=error,f=1)
        




'''if __name__=='__main__':
    app.run(debug=True)'''
