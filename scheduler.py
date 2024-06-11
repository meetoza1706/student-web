import datetime
import os
import time as tm

# Define the schedule
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
    "Saturday": {"time_slots": ["08:30 AM", "09:20 AM", "10:10 AM", "11:00 AM", "11:50 PM"],
                 "lectures": ["MS", "ADBMS", "WT-LAB", "WT-LAB", "end of day"],
                 "class_numbers": ["Class 31", "Class 32", "Class 33", "Class 34", ""]}
}

while True:
    current_time = datetime.datetime.now()
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_number = current_time.weekday()
    weekday_name = weekdays[weekday_number]

    os.system('cls' if os.name == 'nt' else 'clear')
    date = current_time.strftime("%d/%m/%y")
    time = current_time.strftime("%I:%M:%S %p").lstrip("0")
    print(f"Date: {date}")
    print(f"Time: {time}")
    print(weekday_name)

    schedule_info = schedule.get(weekday_name)
    if schedule_info:
        current_lecture = ""
        current_class = ""
        for i, time_slot in enumerate(schedule_info["time_slots"]):
            slot_time = datetime.datetime.strptime(time_slot, "%I:%M %p")
            slot_time = slot_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            if current_time >= slot_time:
                current_lecture = schedule_info["lectures"][i]
                current_class = schedule_info["class_numbers"][i]
        if current_lecture and current_lecture != "end of day": #most important thing
            print(f"Currently ongoing lecture: {current_lecture}")
            print(f"Class: {current_class}")
        else:
            print("No lecture currently ongoing")
    else:
        print("No schedule for today")

    tm.sleep(1)