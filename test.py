# from datetime import date

# day_name = date.today`  ().strftime('%A')
# print(day_name)

from datetime import datetime

# Simulating Sunday, July 21, 2024
simulated_date = datetime.now()
day_name = simulated_date.strftime('%A')
if day_name != "Sunday":
    print("working")
else:
    print("Not working")