from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_session import Session
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta, date
import random
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import bcrypt
from flask_bcrypt import Bcrypt
from apscheduler.schedulers.background import BackgroundScheduler

cursor = mysql.connection.cursor()

# Fetch all user IDs
cursor.execute('SELECT user_id FROM user_data')
user_ids = [row[0] for row in cursor.fetchall()]

# Get today's date
today = datetime.now().strftime('%Y-%m-%d')

# Fetch user IDs present today
cursor.execute('SELECT DISTINCT user_id FROM attendance WHERE DATE(time) = %s', (today,))
present_user_ids = {row[0] for row in cursor.fetchall()}

# Find user IDs not present today
missing_user_ids = set(user_ids) - present_user_ids

# Print the list of missing user IDs
print(f"Missing user IDs: {missing_user_ids}")

cursor.close()