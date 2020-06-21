from bs4 import BeautifulSoup
import requests
import ast
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates

website = requests.get(
    'https://www.data.gov.qa/api/records/1.0/search/?dataset=covid-19-cases-in-qatar&q=&rows=150&sort=date&facet=date').text
text = BeautifulSoup(website, 'lxml')
text = ast.literal_eval(text.html.body.p.text)
text = text['records']

date = []
y = []

for i in range(len(text)):
    data = text[i]['fields']
    date.append(datetime.datetime.strptime(data['date'], '%Y-%m-%d'))
    # y.append(data['number_of_new_positive_cases_in_last_24_hrs'])
    y.append(data['total_number_of_positive_cases_to_date'])

date.reverse()
y.reverse()

x = mdates.date2num(date)

# 3 day moving average
x1 = []
y1 = []
for i in range(len(y)):
    if i > 1:
        avg = (int(y[i]) + int(y[i - 1]) + int(y[i - 2])) / 3
        x1.append(x[i])
        y1.append(avg)


def logistic(t, a, b, c):
    return c / (1 + a * np.exp(-b * t))


p0 = [920, 0.077, 102000]
bounds = ([0, 0, 100000], [10000000000, 0.5, 2000000])
print(p0)

(a, b, c), cov = curve_fit(logistic, x, y, bounds=bounds, p0=p0)


def logistic(t):
    return c / (1 + a * np.exp(-b * t))


# lengthen time series
x_longertime = np.array(range(737484, 738000))

plt.scatter(x, y)
# plt.plot(x1, y1)
plt.plot(x_longertime, logistic(x_longertime - 737483))
plt.xlabel("Date")
plt.ylabel("Total cases")
# plt.ylim(0,100000)
plt.xlim(737484, 737650)
plt.legend(['Forecast', 'Actual data'])
# plt.yscale("log")
print(mdates.num2date(737650))