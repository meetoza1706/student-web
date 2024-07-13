from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
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

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'studentweb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/studentweb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Upload configuration
UPLOAD_FOLDER = 'static/images/profile_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

last_attendb_dates = None

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
        current_class = "no classes just relax!!"
        timing = "Enjoy your off time :)"

    return current_lecture, current_class, timing

@app.route('/')
def home():
    current_lecture, current_class, timing = get_current_lecture_and_class(schedule)
    print(current_class)
    print(current_lecture)
    print(timing)

    now = datetime.now()
    if 5 <= now.hour < 12:
        greeting = "Good Morning!"
    elif 12 <= now.hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    username = session.get('username', 'guest')
    ausername = session.get('username')

    profile_photo = None
    email = None

    if 'username' in session:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT email, profile_photo FROM user_data WHERE username = %s', (username,))
        user_data = cursor.fetchone()
        if user_data:
            email = user_data[0]
            profile_photo = user_data[1]
        cursor.close()

    if 'user_id' in session:
        current_user_id = session['user_id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT present_lectures, absent_lectures, late_lectures FROM attendance WHERE user_id = %s', (current_user_id,))
        attendance_data = cursor.fetchall()  

        if attendance_data:
            total_present = 0
            total_absent = 0
            total_late = 0
            total_lectures = 0  

            for row in attendance_data:
                total_present += row[0]
                total_absent += row[1]
                total_late += row[2]
                total_lectures += row[0] + row[1] + row[2]

            if total_lectures > 0:
                present_percentage = round((total_present / total_lectures) * 100, 2)
                absent_percentage = round((total_absent / total_lectures) * 100, 2)
                late_percentage = round((total_late / total_lectures) * 100, 2)

                print(f"total present:{total_present}")
                print(f"total absent:{total_absent}")
                print(f"total late:{total_late}")
                print(f"Total Lectures: {total_lectures}")
                print(f"Overall Present percentage: {present_percentage:.2f}%")
                print(f"Overall Absent percentage: {absent_percentage:.2f}%")
                print(f"Overall Late percentage: {late_percentage:.2f}%")
            
                a_total_lectures = 295
                a_present_percentage = round((total_present / a_total_lectures) * 100, 2)
                a_absent_percentage = round((total_absent / a_total_lectures) * 100, 2)
                a_late_percentage = round((total_late / a_total_lectures) * 100, 2)
                remaining = 100 - (a_absent_percentage + a_present_percentage + a_late_percentage)
                if request.args.get('ajax'):
                    return jsonify({'present_percent': present_percentage, 'absent_percent': absent_percentage, 'late_percent': late_percentage, 'a_present_percent': a_present_percentage, 'a_absent_percent': a_absent_percentage, 'a_late_percent': a_late_percentage, 'remaining': remaining, 'present_lectures': total_present, 'absent_lectures': total_absent, 'late_lectures': total_late, 'total_lectures': total_lectures})
                
            else:
                print("No attendance data available.")
        else:
            print("No data found for the user.")

        cursor.close()
    else:
        print("No user_id in session.")

    return render_template('index.html', current_lecture=current_lecture, current_class=current_class, timing=timing, greeting=greeting, username=username, ausername=ausername, email=email, profile_photo=profile_photo, schedule=schedule, now=now)

@app.route('/attendance')
def attendance():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT email, profile_photo FROM user_data WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    return render_template('attendance.html', username=username,ausername=username, email = user_data[0], profile_photo=user_data[1])

@app.route('/stats')
def stats():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    username = session['username']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT email, profile_photo FROM user_data WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    return render_template('stats.html', username=username,ausername=username, email = user_data[0], profile_photo=user_data[1])

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    current_user_id = session['user_id']
    today = date.today()
    present_button = data.get('presentButton', False)
    leave_button = data.get('leaveButton', False)
    
    cursor.execute('SELECT PB_status, LB_status FROM attendance WHERE user_id = %s AND day = %s', (current_user_id, today))
    user_data = cursor.fetchone()
    if user_data:
        PB_status = user_data[0]
        LB_status = user_data[1]
    else:
        PB_status = 0
        LB_status = 0

    if present_button:
        if PB_status == 1:
            response_data = {'success': False, 'message': 'You have already marked your presence today.'}
            print("You have already marked your presence today.")
        else:
            attendance = 6
            absent = 0
            late = 0
            PB_status = 1
            LB_status = 0
            cursor.execute(
                'INSERT INTO attendance (day, present_lectures, absent_lectures, late_lectures, PB_status, LB_status, user_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                (today, attendance, absent, late, PB_status, LB_status, current_user_id))
            mysql.connection.commit()
            response_data = {'success': True, 'message': 'Presence marked successfully.'}
    elif leave_button:
        if PB_status == 0:
            response_data = {'success': False, 'message': 'You should be present to be abesent at some point 🤬'}
        elif LB_status == 1:
            response_data = {'success': False, 'message': 'You have already marked your leave today.'}
        else:
            attendance = 4
            absent = 2
            late = 0
            PB_status = 1
            LB_status = 1
            cursor.execute(
                'UPDATE attendance SET present_lectures = %s, absent_lectures = %s, late_lectures = %s, PB_status = %s, LB_status = %s WHERE user_id = %s AND day = %s',
                (attendance, absent, late, PB_status, LB_status, current_user_id, today)
            )
            mysql.connection.commit()
            response_data = {'success': True, 'message': 'Leaving marked successfully.'}
    else:
        response_data = {'success': False, 'message': 'Invalid request.'}

    cursor.close()
    return jsonify(response_data), 200  

@app.route('/c_attendance', methods=['GET', 'POST'])
def custom_attendance():
    data = request.get_json()
    response_data = ''
    cursor = mysql.connection.cursor()
    current_user_id = session['user_id']
    present = data.get('present', False)
    absent = data.get('absent', False)
    late = data.get('late', False)
    today = date.today()
    print(f"present:{present}")
    print(f"absent:{absent}")
    print(f"late:{late}")
    cursor.execute('UPDATE attendance SET present_lectures = %s, absent_lectures = %s, late_lectures = %s WHERE user_id = %s AND day = %s', (present, absent, late, current_user_id, today))
    mysql.connection.commit()
    cursor.close()
    response_data = 'Attendance registered successfully!'
    return jsonify(response_data), 200


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

@app.route('/clear')
def clear():
    session.clear()
    return redirect('/')

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
                return render_template('login.html', msg1=msg)
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
        cursor.execute('SELECT user_id, username, password FROM user_data WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account:
            user_id = account[0]
            username_from_db = account[1]
            hashed_password = account[2]
            
            if bcrypt.check_password_hash(hashed_password, password):
                session.permanent = True  # Set session as permanent
                session['logged_in'] = True
                session['username'] = username_from_db
                session['user_id'] = user_id  # Add user ID to session
                return redirect('/')
            else:
                msg = 'Incorrect password. Please try again.'
        else:
            msg = 'Username not found. Please try again.'

        cursor.close()

    return render_template('login.html', msg=msg)
    
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
                msg1 = 'Password successfully reset.'
                return render_template('login.html', msg1=msg1)
            except Exception as e:
                msg = 'Error resetting password: ' + str(e)
    return render_template('reset_password.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'logged_in' not in session:
        return redirect(url_for('login')) 

    username = session['username']
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
        # Handle profile photo update
        if 'profile_photo' in request.files:
            profile_photo = request.files['profile_photo']
            if profile_photo.filename != '':
                filename = secure_filename(profile_photo.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                profile_photo.save(filepath)
                
                # Update profile photo in database
                cursor.execute('UPDATE user_data SET profile_photo = %s WHERE username = %s', (filename, username))
                mysql.connection.commit()

        # Handle first name and last name update
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        if f_name and l_name:
            cursor.execute('UPDATE user_data SET f_name = %s, l_name = %s WHERE username = %s', (f_name, l_name, username))
            mysql.connection.commit()



        # Handle password update
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('c_new_password')

        if current_password and new_password and confirm_new_password:
            cursor.execute('SELECT password FROM user_data WHERE username = %s', (username,))
            db_password = cursor.fetchone()[0]

            if bcrypt.check_password_hash(db_password, current_password):
                hashed_new_password =   hash_password(new_password)  # Hash new password
                cursor.execute('UPDATE user_data SET password = %s WHERE username = %s', (hashed_new_password, username))
                mysql.connection.commit()
                flash('Password updated successfully', 'success')
            else:
                flash('Current password incorrect', 'error')
        else:
            flash('Please fill all password fields', 'error')

    # Fetch user data for displaying in the form
    cursor.execute('SELECT email, f_name, l_name, profile_photo FROM user_data WHERE username = %s', (username,))
    user_data = cursor.fetchone()
    cursor.close()

    f_name = user_data[1]
    print(f_name)
    if f_name == "Null" or f_name == None:
        f_name = ''

    l_name = user_data[2]
    print(l_name)
    if l_name == "Null" or l_name == None:
        l_name = ''

    print(f_name)
    print(l_name)
    
    
    # Render the profile page with user data
    return render_template('profile.html', username=username, email=user_data[0], f_name=f_name, l_name=l_name, profile_photo=user_data[3])

@app.route('/change_email', methods=['GET','POST'])
def change_email():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
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
                return render_template('new_email.html', msg=msg)
            else:
                msg = 'Failed to send OTP. Please try again later.'
        else:
            msg = 'Email not found in our records. Please check and try again.'
        cursor.close()
    return render_template('change_email.html',msg=msg)

@app.route('/new_email', methods=['GET', 'POST'])
def new_email():
    if 'logged_in' not in session:
        return redirect(url_for('login'))
    msg = ''
    
    if request.method == 'POST':
        new_email = request.form['new_email']
        
        # Check if the new email already exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_data WHERE email = %s', (new_email,))
        account = cursor.fetchone()
        
        if account:
            msg = 'Email already exists!'
        else:
            # Generate and send OTP to the new email
            otp = generate_otp()
            if send_email(new_email, otp):
                session['otp'] = otp  # Store the OTP in the session
                session['new_email'] = new_email  # Store the new email in the session
                msg = 'OTP has been sent to your new email. Please verify.'
                return render_template('verify_email.html', msg=msg)  # Redirect to OTP verification page
            else:
                msg = 'Failed to send OTP. Please try again.'
    
    return render_template('new_email.html', msg=msg)


@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    if 'logged_in' not in session:
       return redirect(url_for('login'))

    username = session.get('username')
    msg = ''
    
    if request.method == 'POST':
        otp = request.form['otp']
        
        # Verify OTP
        if otp == session.get('otp'):
            new_email = session.get('new_email')
            if new_email:
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE user_data SET email = %s WHERE username = %s', (new_email, username))
                mysql.connection.commit()
                cursor.close()
                msg = 'Email has been changed.'
                session.pop('otp', None)  # Clear the OTP from session
                session.pop('new_email', None)  # Clear the new email from session
                return redirect(url_for('profile'))
        else:
            msg = 'Invalid OTP. Please try again.'

    return render_template('verify_email.html', msg=msg)

@app.route('/XA', methods=['POST', 'GET'])
def XA():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT username, password FROM admin')
    account = cursor.fetchone()
    
    if account:
        username = account[0]
        password = account[1]
        print(username)
        print(password)

    if request.method == 'POST':
        Fusername = request.form.get('username')
        Fpassword = request.form.get('password')
        buttonResponse = request.form.get('buttonResponse')
        responseButton2 = request.form.get('responseButton2')
        
        # Check if this is an AJAX request for buttonResponse
        if buttonResponse is not None:
            print(buttonResponse)
            cursor.execute('UPDATE admin SET unit_status = %s', (buttonResponse,))
            mysql.connection.commit()  # Commit the transaction
            return jsonify({'message': 'Button response received', 'buttonResponse': buttonResponse})

        # Check if this is an AJAX request for responseButton2
        if responseButton2 is not None:
            print(responseButton2)
            cursor.execute('UPDATE admin SET unit_status = %s', (responseButton2,))
            mysql.connection.commit()  # Commit the transaction
            return jsonify({'message': 'Response button 2 received', 'responseButton2': responseButton2})

        # Regular authentication process
        print(Fusername)
        print(Fpassword)
        if Fusername == username and Fpassword == password:
            return render_template('XAB.html')
        cursor.close()
    return render_template('XA.html')


@app.route('/unit_test', methods=['POST','GET'])
def unit_test():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT unit_status FROM admin')
    account = cursor.fetchone()
    portal = account[0]
    print(portal)
    ETT = request.form.get('ETT')
    FA = request.form.get('FA')
    JAVA = request.form.get('JAVA')
    NSM = request.form.get('NSM')
    print(ETT, FA, JAVA, NSM)
    msg = "Submitted"
    return render_template('unit.html', portal=portal, msg=msg),  jsonify({'message': 'Data received successfully'})

if __name__ == '__main__':
    app.run(debug=True)
