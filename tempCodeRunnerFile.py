while True:
    current_time = datetime.datetime(2024, 6, 12, 8, 56, 0)  # Simulate time to 8:56 AM
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
        current_start_time = ""
        current_end_time = ""
        timing = ""
        for i, time_slot in enumerate(schedule_info["time_slots"]):
            slot_time = datetime.datetime.strptime(time_slot, "%I:%M %p")
            slot_time = slot_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            if current_time >= slot_time:
                current_lecture = schedule_info["lectures"][i]
                current_class = schedule_info["class_numbers"][i]
                if i == 0:
                    current_start_time = time_slot
                else:
                    current_start_time = schedule_info["time_slots"][i-1]
                if i == len(schedule_info["time_slots"]) - 1:
                    current_end_time = "End of day"
                else:
                    current_end_time = schedule_info["time_slots"][i]
                timing = f"{current_start_time} - {schedule_info['time_slots'][i+1]}"
        if current_lecture and current_lecture != "end of day": 
            print(f"Currently ongoing lecture: {current_lecture} ({timing})")
            print(f"Class: {current_class}")
        else:
            print("No lecture currently ongoing")
    else:
        print("No schedule for today")

    tm.sleep(1)