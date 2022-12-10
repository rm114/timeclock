import re
import datetime
import time
CurrentHours = input("What are your current total hours?")
CurrentTime = input("When did you last clock in/out? [Use the format HHMM or press enter to use the current time]")
#MaxHours = input("What are your maximum hours?")
MaxHours = 80

try:
    CurrentTime = datetime.datetime.strptime(CurrentTime, "%H%M")
except:
    print ("Time formatting error, now using the current time.")
    CurrentTime = datetime.datetime.now()

HoursLeft_int = float(MaxHours) - float(CurrentHours)
Hours_array = str(HoursLeft_int).split(".")

HoursLeft_hour = int(Hours_array[0])
HoursLeft_min = int(Hours_array[1])

if HoursLeft_min == 25:
    HoursLeft_min = 15
elif HoursLeft_min == 5:
    HoursLeft_min = 30
elif HoursLeft_min == 75:
    HoursLeft_min = 45
else:
    HoursLeft_min = 0

HoursLeft_hour_c = HoursLeft_hour * 3600
HoursLeft_min_c = HoursLeft_min * 60

day_hour = HoursLeft_hour_c//86400
hour_hour = (HoursLeft_hour_c-(day_hour*86400))//3600 
min_hour = (HoursLeft_hour_c - ((day_hour*86400) + (hour_hour*3600)))//60 
seconds_hour = HoursLeft_hour_c - ((day_hour*86400) + (hour_hour*3600) + (min_hour*60)) 

day_min = HoursLeft_min_c//86400
hour_min = (HoursLeft_min_c-(day_min*86400))//3600 
min_min = (HoursLeft_min_c - ((day_min*86400) + (hour_min*3600)))//60 
seconds_min = HoursLeft_min_c - ((day_min*86400) + (hour_min*3600) + (min_min*60)) 

hour1 = hour_hour + hour_min
min1 = min_hour + min_min
seconds1 = seconds_hour + seconds_min

HoursLeft = datetime.time(hour1, min1, seconds1)

HoursLeft_Final = CurrentTime + datetime.timedelta(hours=hour1, minutes=min1, seconds=seconds1)
HoursLeft_Final2 = datetime.datetime.strftime(HoursLeft_Final, "%I:%M %p")

print("------------------------------------------")

if min1 < 10:

    print("You have " + str(hour1) + ": 0" + str(min1) + " hours of work remaining.")

    print("To reach your maximum hours, you should clock out at exactly: " + str(HoursLeft_Final2))

    print("------------------------------------------")

else:
    print("You have " + str(hour1) + ":" + str(min1) + " hours of work remaining.")

    print("To reach your maximum hours, you should clock out at exactly: " + str(HoursLeft_Final2))

    print("------------------------------------------")

quit ()