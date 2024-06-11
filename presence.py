lectures = 0
breakleave = 0
present = 0

present = int(input("present or not: "))

if present == 1:
    present = True
    lectures += 6

elif present == 0:
    present = False
    lectures = 0

if present == True:
    breakleave = int(input("leaving after break?: "))

    if breakleave == 1:
        breakleave = True
        lectures -= 2

    elif breakleave == 0:
        breakleave = False

if present == True:
    present = "Present"
elif present == False:
    present = "Absent"
    
if breakleave == True:
    breakleave = "Left"
elif breakleave == False:
    breakleave = "Not left"
    
print(f"present: {present}")
print(f"breakleave: {breakleave}")
print(f"lectures: {lectures}")