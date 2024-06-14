from flask import Flask, render_template, request , session,  jsonify, redirect, url_for
from flask_mysqldb import MySQL
import datetime
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt

app = Flask(__name__)
app.secret_key = os.urandom(24)

OUTLOOK_SMTP_SERVER = 'smtp-mail.outlook.com'
OUTLOOK_SMTP_PORT = 587
OUTLOOK_EMAIL = 'studentweb24@hotmail.com'
OUTLOOK_PASSWORD = 'Studentweb@2420'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'studentweb'

mysql = MySQL(app)

schedule = {
    "Monday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
               "lectures": ["SE", "ICT", "ADBMS-LAB", "ADBMS-LAB", "Break", "DS-LAB", "DS-LAB", "end of day"],
               "class_numbers": ["Class 1", "Class 2", "Class 3", "Class 4", "", "Class 5", "Class 6", ""]},
    "Tuesday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:20 PM", "02:10 PM"],
                "lectures": ["MS", "WT", "ICT", "DS", "Break", "ADBMS", "SE", "end of day"],
                "class_numbers": ["Class 7", "Class 8", "Class 9", "Class 10", "", "Class 11", "Class 12", ""]},
    "Wednesday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
                  "lectures": ["ADBMS-LAB", "ADBMS-LAB", "ADBMS", "DS", "Break", "EVA", "EVA", "end of day"],
                  "class_numbers": ["Class 13", "Class 14", "Class 15", "Class 16", "", "Class 17", "Class 18", ""]},
    "Thursday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
                 "lectures": ["SE-LAB", "SE-LAB", "SE", "ICT", "Break", "WT-LAB", "WT-LAB", "end of day"],
                 "class_numbers": ["Class 19", "Class 20", "Class 21", "Class 22", "", "Class 23", "Class 24", ""]},
    "Friday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
               "lectures": ["MS", "ADBMS", "WT-LAB", "WT-LAB", "Break", "EVA", "EVA", "end of day"],
               "class_numbers": ["Class 25", "Class 26", "Class 27", "Class 28", "", "Class 29", "Class 30", ""]},
    "Saturday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM"],
                 "lectures": ["MS", "ADBMS", "WT-LAB", "WT-LAB", "end of day"],
                 "class_numbers": ["Class 31", "Class 32", "Class 33", "Class 34", ""]}
}

@app.route('/')
def home():
    current_time = datetime.datetime.now()
    
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_number = current_time.weekday()
    weekday_name = weekdays[weekday_number]

    schedule_info = schedule.get(weekday_name)
    current_lecture = ""
    current_class = ""
    timing = ""

    if schedule_info:
        if weekday_name == "Saturday":
            if current_time.hour < 11 or (current_time.hour == 11 and current_time.minute <= 50):
                for i, time_slot in enumerate(schedule_info["time_slots"]):
                    slot_time = datetime.datetime.strptime(time_slot, "%I:%M %p")
                    slot_time = slot_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                    if current_time < slot_time:
                        current_lecture = schedule_info["lectures"][i]
                        current_class = schedule_info["class_numbers"][i]
                        if i == len(schedule_info["time_slots"]) - 1:
                            timing = f"{schedule_info['time_slots'][i]} - End of day"
                        else:
                            timing = f"{schedule_info['time_slots'][i]} - {schedule_info['time_slots'][i+1]}"
                        break
            else:
                current_lecture = "No lectures going on Right now 😁"
                current_class = "no classes just relax!!"
                timing = "Enjoy your off time :)"
        else:
            for i, time_slot in enumerate(schedule_info["time_slots"]):
                slot_time = datetime.datetime.strptime(time_slot, "%I:%M %p")
                slot_time = slot_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
                if current_time < slot_time:
                    current_lecture = schedule_info["lectures"][i-1]
                    current_class = schedule_info["class_numbers"][i-1]
                    if i == len(schedule_info["time_slots"]) - 1:
                        timing = f"{schedule_info['time_slots'][i-1]} - End of day"
                    else:
                        timing = f"{schedule_info['time_slots'][i-1]} - {schedule_info['time_slots'][i]}"
                    if current_lecture == "end of day":
                        current_lecture = ""
                    break
            else:
                current_lecture = schedule_info["lectures"][-1]
                current_class = schedule_info["class_numbers"][-1]
                timing = f"{schedule_info['time_slots'][-1]} - End of day"
                if current_lecture == "end of day":
                        current_lecture = ""

    if 5 <= current_time.hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_time.hour < 18:
        greeting = "Good Afternoon!"
    elif 18 <= current_time.hour < 22:
        greeting = "Good Evening!"
    else:
        greeting = "Good Evening!"

    return render_template('index.html', current_lecture=current_lecture, current_class=current_class, timing=timing, greeting=greeting)

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def generate_otp():
    return str(random.randint(100000, 999999))

def send_email(email, otp):
    msg = MIMEMultipart()
    msg['From'] = OUTLOOK_EMAIL
    msg['To'] = email
    msg['Subject'] = 'Your OTP Code'
    body = f'Your OTP code is {otp}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("Connecting to the SMTP server...")
        server = smtplib.SMTP(OUTLOOK_SMTP_SERVER, OUTLOOK_SMTP_PORT)
        server.starttls()
        server.login(OUTLOOK_EMAIL, OUTLOOK_PASSWORD)
        text = msg.as_string()
        print(f"Sending email to {email}...")
        server.sendmail(OUTLOOK_EMAIL, email, text)
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        if 'otp' in request.form:
            otp = request.form['otp']
            if otp == session.get('otp'):
                user_data = session.get('user_data')
                hashed_password = hash_password(user_data['password'])  # Hash the password
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO user_data (username, password, email) VALUES (%s, %s, %s)',
                               (user_data['username'], hashed_password, user_data['email']))  # Store hashed password
                mysql.connection.commit()
                cursor.close()
                session.pop('otp', None)
                session.pop('user_data', None)
                msg = 'You have successfully registered!'
                return render_template('login.html', msg=msg)
            else:
                msg = 'Invalid OTP. Please try again.'
                return render_template('register.html', msg=msg, otp_sent=True)

        try:
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            email = request.form['email']
            
            if not (username and password and confirm_password and email):
                msg = 'Please fill out all the fields!'
            elif password != confirm_password:
                msg = 'Passwords do not match!'
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('SELECT * FROM user_data WHERE username = %s', (username,))
                account = cursor.fetchone()
                
                if account:
                    msg = 'Username already exists!'
                else:
                    cursor.execute('SELECT * FROM user_data WHERE email = %s', (email,))
                    account = cursor.fetchone()
                    if account:
                        msg = 'Email already exists!'
                    elif username == email:
                        msg = 'Username cannot be the same as email!'
                    else:
                        otp = generate_otp()
                        session['otp'] = otp
                        session['user_data'] = {
                            'username': username,
                            'password': password,  # Store plain password temporarily for OTP verification
                            'email': email
                        }
                        if send_email(email, otp):
                            msg = 'OTP has been sent to your email. Please verify.'
                            return render_template('register.html', msg=msg, otp_sent=True)
                        else:
                            msg = 'Failed to send OTP. Please try again.'

        except Exception as e:
            msg = 'Error occurred during registration: ' + str(e)
    
    return render_template('register.html', msg=msg)

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)