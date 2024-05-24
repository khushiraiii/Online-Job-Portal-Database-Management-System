import csv
import mysql.connector
import MySQLdb
from datetime import datetime, timedelta
import random
import re

def random_future_date(start_date, end_date):
    # Generate a random number of days to add to the start date
    random_days = random.randint(1, (end_date - start_date).days)
    
    # Add the random number of days to the start date
    future_date = start_date + timedelta(days=random_days)
    
    return future_date
# Connect to MySQL database


conn = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='26761117',
    db='jobportal',
    
)
cursor = conn.cursor()


# Read CSV file and insert data into MySQL database
with open('naukri_com-job_sample.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row
    i=3
    for row in reader:
        company,req,exp,indus,descr,jobid,loc,title,numberofpositions,pay,postdate,site_name,skills,uniq_id=row
        emp_id=1

        start_date = datetime.now()
        end_date = start_date + timedelta(days=365)  # One year from now
        postdate=re.sub(r'\s+\+\d+', '', postdate)
        # Generate a random future date
        random_date = random_future_date(start_date, end_date)
        random_date= random_date.strftime('%Y-%m-%d')
        #print("Random future date:", random_date)
        remove_string = "Job Description Â Send me Jobs like this"
        descr = descr.replace(remove_string, "").strip()
        print(descr)
        req=req+" "+skills
        try:
          cursor.execute("""INSERT INTO job_postings (JOB_ID, TITLE, DESCR, PAY, LOCATION, EMP_ID, DATE_POSTED, LAST_DATE, REQUIREMENTS, COMPANY)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (i, title, descr, pay, loc, emp_id, postdate, random_date, req, company))
          i=i+1
          conn.commit()
        except UnicodeDecodeError as e:
            print(f"Error inserting data: {e}. Skipping entry.")
            # Skip to the next iteration of the loop if an error occurs
            continue
    print(i)

     

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()