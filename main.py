from flask import Flask, render_template
import datetime
import time

app = Flask(__name__)

@app.route('/')
def home():
    while True:
        current_time = datetime.datetime.now()
        if 5 <= current_time.hour < 12:
            greeting = "Good Morning!"
        elif 12 <= current_time.hour < 18:
            greeting = "Good Afternoon!"
        elif 18 <= current_time.hour < 22:
            greeting = "Good Evening!"
        else:
            greeting = "Good Night!"
        print(greeting)
        time.sleep(5)
        return render_template('index.html', greeting=greeting)

if __name__ == '__main__':
    app.run(debug=True)