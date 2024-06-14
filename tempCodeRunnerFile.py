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
