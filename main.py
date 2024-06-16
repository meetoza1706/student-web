from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'meet'
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
bcrypt = Bcrypt(app)

# Schedule dictionary
schedule = {
    "Monday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
        "lectures": ["SE", "ICT", "ADBMS-LAB", "ADBMS-LAB", "Break", "DS-LAB", "DS-LAB", "end of day"],
        "class_numbers": ["Class 1", "Class 2", "Class 3", "Class 4", "", "Class 5", "Class 6", ""]
    },
    "Tuesday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:20 PM", "02:10 PM"],
        "lectures": ["MS", "WT", "ICT", "DS", "Break", "ADBMS", "SE", "end of day"],
        "class_numbers": ["Class 7", "Class 8", "Class 9", "Class 10", "", "Class 11", "Class 12", ""]
    },
    "Wednesday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
        "lectures": ["ADBMS-LAB", "ADBMS-LAB", "ADBMS", "DS", "Break", "EVA", "EVA", "end of day"],
        "class_numbers": ["Class 13", "Class 14", "Class 15", "Class 16", "", "Class 17", "Class 18", ""]
    },
    "Thursday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
        "lectures": ["SE-LAB", "SE-LAB", "SE", "ICT", "Break", "WT-LAB", "WT-LAB", "end of day"],
        "class_numbers": ["Class 19", "Class 20", "Class 21", "Class 22", "", "Class 23", "Class 24", ""]
    },
    "Friday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM", "12:30 PM", "01:30 PM", "02:10 PM"],
        "lectures": ["MS", "ADBMS", "WT-LAB", "WT-LAB", "Break", "EVA", "EVA", "end of day"],
        "class_numbers": ["Class 25", "Class 26", "Class 27", "Class 28", "", "Class 29", "Class 30", ""]
    },
    "Saturday": {
        "time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 AM"],
        "lectures": ["MS", "ADBMS", "WT-LAB", "WT-LAB", "end of day"],
        "class_numbers": ["Class 31", "Class 32", "Class 33", "Class 34", ""]
    }
}

def get_current_lecture_and_class(schedule):
    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()

    if current_day in schedule:
        day_schedule = schedule[current_day]
        for i, time_slot in enumerate(day_schedule["time_slots"]):
            start_time = datetime.strptime(time_slot, "%I:%M %p").time()
            if i < len(day_schedule["time_slots"]) - 1:
                end_time = datetime.strptime(day_schedule["time_slots"][i + 1], "%I:%M %p").time()
            else:
                end_time = (datetime.strptime(time_slot, "%I:%M %p") + timedelta(hours=1)).time()

            if start_time <= current_time < end_time:
                current_lecture = day_schedule["lectures"][i]
                current_class = day_schedule["class_numbers"][i]
                if i < len(day_schedule["time_slots"]) - 1:
                    timing = f"{time_slot} to {day_schedule['time_slots'][i + 1]}"
                else:
                    timing = f"{time_slot} to end of day"
                break
        else:
            current_lecture = "No lectures going on Right now 😁"
            current_class = "no classes just relax!!"
            timing = "Enjoy your off time :)"
    else:
        current_lecture = "Enjoy the day off mate 😁"
        current_class = "    "
        timing = ""

    return current_lecture, current_class, timing


@app.route('/')
def home():
    current_lecture, current_class, timing = get_current_lecture_and_class(schedule)

    now = datetime.now()
    if 5 <= now.hour < 12:
        greeting = "Good Morning!"
    elif 12 <= now.hour < 18:
        greeting = "Good Afternoon!"
    elif 18 <= now.hour < 22:
        greeting = "Good Evening!"
    else:
        greeting = "Good Evening!"

    username = session.get('username', 'guest')
    ausername = session.get('username')
    first_letter = username[0]
    if 'logged_in' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email FROM user_data WHERE username = %s', (username,))
        email = cursor.fetchone()[0]
    else:
        email = None

    return render_template('index.html', current_lecture=current_lecture, current_class=current_class, timing=timing, greeting=greeting, username=username, ausername=ausername, email=email)

def hash_password(password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
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

def verify_password(plain_password, hashed_password):
    return bcrypt.check_password_hash(hashed_password, plain_password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT username, password FROM user_data WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            username_from_db = account[0]
            hashed_password = account[1]  
            
            if bcrypt.check_password_hash(hashed_password, password):
                session['logged_in'] = True
                session['username'] = username_from_db
                return redirect('/')
            else:
                msg = 'Incorrect password. Please try again.'
        else:
            msg = 'Username not found. Please try again.'

        cursor.close()

    return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        username = session['username']
        return f'Welcome, {username}! This is your dashboard.'
    else:
        return redirect(url_for('login'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    msg = ''
    if request.method == 'POST':
        email = request.form['email']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_data WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            otp = generate_otp()
            session['reset_email'] = email
            session['otp'] = otp
            if send_email(email, otp):
                msg = 'An OTP has been sent to your email. Please check and enter it below.'
                return render_template('reset_password.html', msg=msg)
            else:
                msg = 'Failed to send OTP. Please try again later.'
        else:
            msg = 'Email not found in our records. Please check and try again.'
        cursor.close()
    return render_template('forgot_password.html', msg=msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    msg = ''
    if request.method == 'POST':
        otp = request.form['otp']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        if otp != session.get('otp'):
            msg = 'Invalid OTP. Please try again.'
        elif new_password != confirm_password:
            msg = 'Passwords do not match.'
        else:
            hashed_password = hash_password(new_password)
            email = session.get('reset_email')
            try:
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE user_data SET password = %s WHERE email = %s', (hashed_password, email))
                mysql.connection.commit()
                cursor.close()
                session.pop('otp', None)
                session.pop('reset_email', None)
                msg = 'Password successfully reset.'
                return render_template('login.html', msg=msg)
            except Exception as e:
                msg = 'Error resetting password: ' + str(e)
    return render_template('reset_password.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
