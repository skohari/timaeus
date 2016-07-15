from datetime import datetime, timedelta, time, date
import time
from apscheduler.scheduler import Scheduler
import requests
from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
from subprocess import call
from subprocess import check_output
import logging
logging.basicConfig()
sched = Scheduler()
sched.daemonic = False
sched.start()

edate = '25AUG2016'
todayc = datetime.today()
cmon = todayc.month
nthu = todayc
while todayc.month == cmon:
    todayc += timedelta(days=1)
    cthu = todayc
cthu += timedelta(days=-1)
nstart = cthu + timedelta(days=1)
nmon = nstart.month
nthu = nstart
while nstart.month == nmon:
    if nstart.weekday()==3: #this is Thursday 
        nthu = nstart
    nstart += timedelta(days=1)
dd = nthu.strftime("%d%b%Y")
edate = dd.upper()
print (edate)

OpenNifty = 7212
def job_fnF():
    url = 'https://www1.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTIDX&symbol=NIFTY&date=' + edate
    response = requests.get(url)
    resp = response.content
    soup = BeautifulSoup(resp)
    table1 = soup.find('table')
    niftyrow = []
    for row1 in table1.findAll('b'):
        text1 = row1.text.replace('style','')
        niftyrow.append(text1)
    niftyval = int(text1[5:10]) + 2
    callstrk = int(round(niftyval, -2)) + 300
    putstrk = callstrk - 700
    callstring = "%d.00" %callstrk
    for row1 in soup.find_all('tr'):
        cells = row1.find_all('td')
        for cell in cells:
            value = cell.string
            if value == callstring:
                celln = 0
                for cell in cells:
                    celln = celln + 1
                    value = cell.string
                    if celln == 10:
                        #print CallPrice
    putstring = "%d.00" %putstrk
    for row1 in soup.find_all('tr'):
        cells = row1.find_all('td')
        for cell in cells:
            value = cell.string
            if value == putstring:
                celln = 0
                for cell in cells:
                    celln = celln + 1
                    value = cell.string
                    if celln == 14:
                        PutPrice = value
                        #print PutPrice
    indtime= datetime.now() + timedelta(hours=5, minutes=30)
    ddtime = '{:%D:%H:%M:%S}'.format(indtime)
#    print "Nifty", niftyval, "Calls",callstrk, "Puts",putstrk, datetime.now(), PutPrice, OpenNifty
    msg = "New: Sell Calls %d , Puts %d , Thanks! "  %(callstrk, putstrk)
    check_output(["yowsup-cli", "demos", "-M","-c", "config", "-s", "919820697677-1456799885@g.us",  "F%s" % msg])
    check_output(["yowsup-cli", "demos", "-M","-c", "config", "-s", "4915780443995-1458243917@g.us", "F%s" % msg])
#    check_output(["yowsup-cli", "demos", "-M","-c", "config", "-s", "919820697677",  "F%s" % msg])

#sched.add_cron_job(job_fnF, second='05')
sched.add_cron_job(job_fnF, month='1-12', day_of_week='0-4', hour='09', minute='45',  second='05')

