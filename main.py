from flask import Flask, render_template
import datetime

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

