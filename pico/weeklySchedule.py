import time
import json
import wifi
import socketpool
import ssl
import adafruit_requests

class uTime:
    def __init__(self, t_str):
        # t_str is a string that has the time as "9:30[]:00]"
        t = t_str.split(":")
        self.hr = int(t[0])
        self.min = int(t[1])
        self.totMins = self.hr * 60 + self.min
        if len(t) == 3:
            self.sec = int(t[2])
        else:
            self.sec = 0
        self.totSecs = self.totMins * 60 + self.sec

    def __str__(self):
        return f'{self.hr}:{str(self.min)}:{str(self.sec)}'

class period:
    def __init__(self, startTime, endTime, note=""):
        # enter start and end times as strings "00:00[:00]"
        self.startTime = uTime(startTime)
        self.endTime = uTime(endTime)
        self.note = note
        self.lengthInSeconds = self.endTime.totSecs - self.startTime.totSecs 

    def __str__(self):
        t = f'{self.startTime}-{self.endTime}'
        return t

class daySchedule:
    def __init__(self, dayName, periods):
        self.dayName = dayName
        self.periods = periods 

        # (todo) Check that periods do not overlap
    def findPeriod(self, t="00:00:00"):
        t = uTime(t)
        #p = -1
        if (t.totSecs < self.periods[0].startTime.totSecs):
            # before periods
            return period("00:00", f"{self.periods[0].startTime}")
        elif (t.totSecs >= self.periods[-1].endTime.totSecs):
            # after periods
            return period(f"{self.periods[-1].endTime}", "23:59:59")
        for i in range(len(self.periods)):
            # check if in a period
            if ((t.totSecs > self.periods[i].startTime.totSecs) and (t.totSecs <= self.periods[i].endTime.totSecs)):
                # p = i
                return self.periods[i]
            # check if in between periods:
            if ((t.totSecs > self.periods[i-1].endTime.totSecs) and (t.totSecs <= self.periods[i].startTime.totSecs)):
                return period(f'{self.periods[i-1].endTime}', f"{self.periods[i].startTime}")
        # if nothing found
        return None
    
def calcTime():
    localTime, today = getLocalTime()
    print(localTime, today)
    p = daySchedules[today].findPeriod(f'{localTime}')
    print(p)
    timeLeft = p.endTime.totSecs - localTime.totSecs 
    fracDone = (localTime.totSecs - p.startTime.totSecs) / timeLeft
    print(timeLeft, fracDone)
    return (timeLeft, p)
        

def getLocalTime():
    url = 'http://Onemint.local/makerspaceTime.php'
    try:
        response = requests.get(url)
        timeStr = response.text
        response.close()
        t = json.loads(timeStr)
        # lt = time.strptime(f'{t["tm_year"]+1900}', '%Y')
        lt = f'{t["tm_hour"]}:{t["tm_min"]}:{t["tm_sec"]}'
        return (uTime(lt), t['tm_wday'])
    except Exception as e:
        print("Error:\n", str(e))

# periods
m0 = period("8:00", "8:15", "Before Classes")
mm = period("8:15", "8:30", "Morning Meeting")
ma = period("8:15", "8:30", "Morning Advisory")
m1 = period("8:30", "9:25", "First Period")
m2 = period("9:30", "10:25", "Second Period")
m3 = period("10:30", "11:25", "Third Period")
em = period("11:30", "12:15", "Monring Elective")
lunch = period("12:15", "12:45", "Lunch")

a1 = period("12:45", "13:40", "First Afternoon Period")
a2 = period("13:45", "14:40", "Second Afternoon Period")
ea = period("14:45", "15:30", "Afternoon Elective")

tha = period("12:45", "12:55", "Afternoon Advisory (Thurs)")

fm = period("8:00", "9:15", "Faculty Meeting")
th1 = period("9:15", "9:55", "First Period (Thurs)")
th2 = period("10:00", "10:40", "Second Period (Thurs)")
th3 = period("10:45", "11:25", "Third Period (Thurs)")
thLong = period("13:00", "14:40", "Long Period (Thurs)")

# daily schedules
daySchedules = [
    daySchedule("Sunday", [m0, mm, m1, m2, m3, em, lunch, a1, a2, ea]),
    daySchedule("Monday", [m0, mm, m1, m2, m3, em, lunch, a1, a2, ea]),
    daySchedule("Tuesday", [m0, ma, m1, m2, m3, em, lunch, a1, a2, ea]),
    daySchedule("Wednesday", [m0, mm, m1, m2, m3, em, lunch, a1, a2, ea]),
    daySchedule("Thursday", [fm, th1, th2, th3, em, lunch, tha, thLong, ea]),
    daySchedule("Friday", [m0, mm, m1, m2, m3, em, lunch, a1, a2, ea]),
    daySchedule("Saturday", [m0, mm, m1, m2, m3, em, lunch, a1, a2, ea]),
]

print(daySchedules[1].dayName)
print(daySchedules[1].findPeriod("12:15:01"))

# connect to wifi
print("connecting")
wifi.radio.connect("Wifipower", "defacto1")
print("connected")
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
print("My IP address is", wifi.radio.ipv4_address)

while True:
    (secsToGo, currentPeriod) = calcTime()
    print(f"{currentPeriod.note}: {currentPeriod}")
    startTime = time.monotonic()
    dt = 0
    while (dt < secsToGo):
        frac = (secsToGo-dt) / currentPeriod.lengthInSeconds
        print(f'Seconds Left: {secsToGo-dt}/{currentPeriod.lengthInSeconds} | {frac*100}%')
        time.sleep(2)
        dt = (time.monotonic() - startTime)

