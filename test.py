import datetime

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