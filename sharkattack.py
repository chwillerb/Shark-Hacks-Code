import xml.etree.ElementTree as ET
import sqlite3
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from threading import Timer
import ssl
import cgi, cgitb
import requests
from urllib.request import Request
import pandas as pd
import numpy as np
import numpy
import matplotlib.pyplot as plt
import matplotlib
from scipy.optimize import curve_fit
from scipy import stats
import scipy
import sympy as sym
from flask import Flask
#!/usr/bin/python
import cgi, cgitb
# Create instance of FieldStorage
form = cgi.FieldStorage()

cgitb.enable()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#conn = sqlite3.connect('sharkdb.sqlite')
#cur = conn.cursor()
df1 = pd.DataFrame(columns=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], index=['California', 'North Carolina', 'Hawai', 'Maine', 'Florida'])

for f in ['California', 'North Carolina', 'Hawai', 'Maine', 'Florida']:
    temp = list()
    if f == 'California':
        y = 'CA'
    elif f == 'North Carolina':
        y = 'NC'
    elif f == 'Hawai':
        y = 'HI'
    elif f == 'Maine':
        y = 'ME'
    else:
        y = 'FL'

    try:
        c = f.split(' ')
        c = str(f[0] + '-' + f[1])
    except:
        f = str(f)
    url = 'https://www.weatherbase.com/weather/city.php3?c=US&s='+y+'&statename='+c+'-United-States-of-America'
    req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
    html = urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    tags = str(soup('td'))
    tagd = tags.split(' ')
    #count1 = tagd.index('Temperature') +5
    #count2 = tagd.index('class="datac">') - 2
    #print(count1,count2, '####################################')
    #tagd = tagd[count1:count2]
    for x in tagd:
        if x.startswith('class="datac"'):
            x = x.split('>')[1]
            y = x.split('<')[0]
            temp.append(y)
        else:
            p = 0
            #print(x, '#####################')
    temp = temp[1:13]
    df1.loc[f] = temp

#cur.execute('''INSERT OR IGNORE INTO SharkAttack (temp, location, month)
    #VALUES ( ?, ?, ? )''', ( temp, location, month) )
#conn.commit()

df = pd.read_csv('Shark Attack Data - Sheet1.csv')

#all cases + months
CAmonths = df.loc[0].dropna().index[1]
FLmonths = df.loc[1].dropna().index[0],df.loc[1].dropna().index[1],df.loc[1].dropna().index[2],df.loc[1].dropna().index[3],df.loc[1].dropna().index[4],df.loc[1].dropna().index[5],df.loc[1].dropna().index[6],df.loc[1].dropna().index[7],df.loc[1].dropna().index[6],df.loc[1].dropna().index[8]
HImonths = df.loc[2].dropna().index[1],df.loc[1].dropna().index[3],df.loc[1].dropna().index[4]
MEmonths = df.loc[3].dropna().index[1]
NCmonths = df.loc[4].dropna().index[1],df.loc[1].dropna().index[3],df.loc[1].dropna().index[4]

temps = float(df1[CAmonths][0]),float(df1[FLmonths[1]][4]),float(df1[FLmonths[2]][4]),float(df1[FLmonths[3]][4]),float(df1[FLmonths[4]][4]),float(df1[FLmonths[5]][4]),float(df1[FLmonths[6]][4]),float(df1[FLmonths[7]][4]),float(df1[FLmonths[8]][4]),float(df1[HImonths[0]][2]),float(df1[HImonths[1]][2]),float(df1[HImonths[2]][2]),float(df1[MEmonths][0]),float(df1[NCmonths[0]][1]),float(df1[NCmonths[1]][1]),float(df1[NCmonths[2]][1])
#           California                                           Florida                                                                                                                                                                                    North Carolina
months = int(str(df.loc[0].dropna()).split('\n')[2].split(' ')[18]), int(str(df.loc[1].dropna()).split('\n')[1].split(' ')[16]), int(str(df.loc[1].dropna()).split('\n')[2].split(' ')[16]), int(str(df.loc[1].dropna()).split('\n')[3].split(' ')[17]), int(str(df.loc[1].dropna()).split('\n')[4].split(' ')[17]), int(str(df.loc[1].dropna()).split('\n')[5].split(' ')[15]), int(str(df.loc[1].dropna()).split('\n')[6].split(' ')[12]),int(str(df.loc[1].dropna()).split('\n')[7].split(' ')[14]), int(str(df.loc[1].dropna()).split('\n')[8].split(' ')[13]),int(str(df.loc[2].dropna()).split('\n')[1].split(' ')[11]),int(str(df.loc[2].dropna()).split('\n')[2].split(' ')[15]),int(str(df.loc[2].dropna()).split('\n')[3].split(' ')[15]),int(str(df.loc[3].dropna()).split('\n')[1].split(' ')[14]),int(str(df.loc[4].dropna()).split('\n')[1].split(' ')[20]),int(str(df.loc[4].dropna()).split('\n')[2].split(' ')[23]), int(str(df.loc[4].dropna()).split('\n')[3].split(' ')[23])

bucket1 = list()#30-40
bucket2 = list()#60-70
bucket3 = list()#70-80
bucket4 = list()#80-90

for y in range(12):
    x = float(temp[y])
    p = int(months[y])
    if x >= 30 and x<40:
        bucket1.append(p)
    elif x >=60 and x<70:
        bucket2.append(p)
    elif x>=70 and x<80:
        bucket3.append(p)
    else:
        bucket4.append(p)
bucket1.append(int('1'))

app = Flask(__name__)

bucket1s = sum(bucket1)
bucket2s = sum(bucket2)
bucket3s = sum(bucket3)
bucket4s = sum(bucket4)

y = np.array([bucket1s,bucket2s,bucket3s,bucket4s])
x = np.array([37.5, 65, 75, 85])

plt.figure()
plt.scatter(temps, months, alpha=0.5, color='xkcd:lightish blue', label='raw data')
plt.scatter(x, y, alpha=0.5, s=40, c='r', label='10 degree brackets')
#scipy.optimize.curve_fit(lambda t,a,b: a+b*numpy.log(t),  x,  y)
font = {'size'  : 8}
plt.xlabel('Temperature (on land) during month of attack in Fahrenheit')
plt.ylabel('Number of shark attacks')
plt.title('Number of Shark Attack(s) Depending on Temperature')

def func(x, b, c, d):
    return b*x**2 +c*x + d

popt, pcov = curve_fit(func, x, y)

#print("b = %s, c = %s, d = %s" % (popt[0], popt[1], popt[2]))

xs = sym.Symbol('\lambda')
tex = sym.latex(func(xs,*popt)).replace('$', '')
formula = r'$f(\lambda)= %s$' %(tex)

plt.plot(x, func(x, *popt), label="Fitted Curve")

c = plt.gca().xaxis
for item in c.get_ticklabels():
    item.set_rotation(45)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.annotate('  unlucky', (40, 1), **font)
#form = cgi.FieldStorage()

# App config.

input1 = float(input('What is the air temperature at the time of visit in Fahrenheit? '))
b = float(popt[0])
c = float(popt[1])
d = float(popt[2])

#@app.route('/my-function')
def func1(first_name):
    point = b*input1**int(2) +c*input1 + d
    if input1 >= 35 and input1 < 100:
        print('At that temperature the US will have around '+str(round(point,2))+' shark attack(s) in the month.')
    elif input1 < 35:
        print('It is very unlikely that there will be a shark attack.')
    else:
        print('There is a low probabilty that there will be a shark attack.')
    return point
plt.legend(loc=2, title='Key')
func1(input1)
plt.show(block=True)
matplotlib.pyplot.show()
