import re
import datetime
import time
from rich.table import Table
from rich.console import Console
from rich import box, print
from rich.prompt import Prompt

#current hours as seen in timeclock app
print('-' * 119)
CurrentHours = Prompt.ask("\r\n[green]What are your current total hours?[/green]")
CurrentTime = Prompt.ask("\r\n[green]When did you last clock in/out? [Use the format HH:MM, HHMM, or press enter to use the current time][/green]")
#no in/out time, defaults to current time
clocktime_color = "green"
clocktime_flag = ""

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
            print ("[red]--->>> Time formatting error, now using the current time <<<---[/red]")
            clocktime_color = "red"
            clocktime_flag = "*time input formatting error"
            CurrentTime = datetime.datetime.now()

MaxHours = Prompt.ask("\r\n[green]Type your maximum allowed hours this week[/green]", choices=["40", "80"])
Quit = 0

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

now = datetime.datetime.now()
nowtime = datetime.datetime.strftime(now, "%I:%M %p")
clocktime = datetime.datetime.strftime(CurrentTime, "%I:%M %p")

table = Table(title="[bold]\r\nTimeClock\r\n[/bold]", caption=f'\r\nTo reach your maximum hours, you should clock out at exactly: [bold yellow]{str(HoursLeft_Final2)}\r\n[/bold yellow]', show_lines=1)
table.add_column("Current Time", style="green", justify="center")
table.add_column("Last Time Clocked In/Out", style="green", justify="center")
table.add_column("Current Hours", style="green", justify="center")
table.add_column("Time Remaining", style="green", justify="center")
table.add_row(str(nowtime),  f"{str(clocktime)} {clocktime_flag}", str(CurrentHours), f"{str(hour1)}:{str(min1)}")

table2 = Table(title="[bold]\r\nTimeClock\r\n[/bold]", caption=f'\r\nTo reach your maximum hours, you should clock out at exactly: \r\n[bold yellow]{str(HoursLeft_Final2)}\r\n[/bold yellow]', show_lines=1)
table2.add_column("Current Time", style="green", justify="center")
table2.add_column("Last Time Clocked In/Out", style=clocktime_color, justify="center")
table2.add_column("Current Hours", style="green", justify="center")
table2.add_column("Time Remaining", style="green", justify="center")
table2.add_row(str(nowtime), f"{str(clocktime)} {clocktime_flag}", str(CurrentHours), f"{str(hour1)}:0{str(min1)}")

console = Console()

print('\n\n' + '-' * 119)
if min1 < 10:
    console.print(table2)
else:
    console.print(table)
print('\n' + '-' * 119)

Quit = Prompt.ask("Please type any key to close the program.", default=1)

if Quit != 0:
    quit()