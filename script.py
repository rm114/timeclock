import re
import datetime
import time

#current hours as seen in timeclock app
CurrentHours = input("What are your current total hours?:")
CurrentTime = input("When did you last clock in/out? [Use the format HH:MM or press enter to use the current time]:")
#Preset max hours, can create and call from a seperate file if needed
MaxHours = 80

#no in/out time, defaults to current time
if len(CurrentTime) < 1:
    CurrentTime = datetime.datetime.now()

#in/out time provided, validates both HH:MM and HHMM
else:
    try:
        CurrentTime = datetime.datetime.strptime(CurrentTime, "%H:%M")
    except:
        try:
            CurrentTime = datetime.datetime.strptime(CurrentTime, "%H%M")
        except:
            print ("--->>> Time formatting error, now using the current time <<<---")
            CurrentTime = datetime.datetime.now()

#how many hours are left until reaching max hours, splits partial time (eg. 7.25hr)
HoursLeft_int = float(MaxHours) - float(CurrentHours)
Hours_array = str(HoursLeft_int).split(".")

HoursLeft_hour = int(Hours_array[0])
HoursLeft_min = int(Hours_array[1])

#converts partial time to minutes
if HoursLeft_min == 25:
    HoursLeft_min = 15
elif HoursLeft_min == 5:
    HoursLeft_min = 30
elif HoursLeft_min == 75:
    HoursLeft_min = 45
else:
    HoursLeft_min = 0
#converts hours to seconds
HoursLeft_hour_c = HoursLeft_hour * 3600
#converts minutes to seconds
HoursLeft_min_c = HoursLeft_min * 60

#converts hours, minutes, day, and seconds for the hour value
day_hour = HoursLeft_hour_c//86400
hour_hour = (HoursLeft_hour_c-(day_hour*86400))//3600 
min_hour = (HoursLeft_hour_c - ((day_hour*86400) + (hour_hour*3600)))//60 
seconds_hour = HoursLeft_hour_c - ((day_hour*86400) + (hour_hour*3600) + (min_hour*60)) 

#converts hours, minutes, day, and seconds for the minute value
day_min = HoursLeft_min_c//86400
hour_min = (HoursLeft_min_c-(day_min*86400))//3600 
min_min = (HoursLeft_min_c - ((day_min*86400) + (hour_min*3600)))//60 
seconds_min = HoursLeft_min_c - ((day_min*86400) + (hour_min*3600) + (min_min*60)) 

#adds the minute value to the hour value
hour1 = hour_hour + hour_min
min1 = min_hour + min_min
seconds1 = seconds_hour + seconds_min

#converts added value to a time value
HoursLeft_Final = CurrentTime + datetime.timedelta(hours=hour1, minutes=min1, seconds=seconds1)
#changes to 12 hr time (Future implementation of weekday, throws wrong date as the date is set to 1900)

HoursLeft_Final2 = datetime.datetime.strftime(HoursLeft_Final, "%I:%M %p")

print("------------------------------------------\n")

if min1 < 10:

    print("You have " + str(hour1) + ":0" + str(min1) + " hours of work remaining.")

    print("To reach your maximum hours, you should clock out at exactly: " + str(HoursLeft_Final2))

else:

    print("You have " + str(hour1) + ":" + str(min1) + " hours of work remaining.")

    print("To reach your maximum hours, you should clock out at exactly: " + str(HoursLeft_Final2))

print("\n------------------------------------------")

quit ()