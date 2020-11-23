import matplotlib.pyplot as plt
import sqlite3
import datetime
import numpy as np
import scipy.interpolate
import pytz
from collections import Counter


def msgtime_hour(data):
    dates = []
    for date in data:
        datestring = date[0]
        try:
            dt = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            dt = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        dt = utc.localize(dt)
        datetime_est = dt.astimezone(est)
        dates.append(datetime_est)

    hours = [date.hour for date in dates]
    cnt = Counter(hours)
    x = [x for x in range(0, 24)]
    y = [cnt[i]/len(hours) for i in x]
    x_new = np.linspace(0, 23, 300)
    spl = scipy.interpolate.make_interp_spline(x, y, k=5)
    smooth = spl(x_new)

    return x, y


conn = sqlite3.connect('messages.db')
c = conn.cursor()

utc = pytz.utc
est = pytz.timezone('US/Eastern')


users = [168175298913894401, 169148751565422592, 185548835118907393, 169136494747844608, 144966476846071817,
         761773584623861760
]
names = ['Jordy', 'Robert', 'Ian', 'Vince', ' Tyler', 'Tocci']
colors = ['red', 'green', 'blue', 'black', 'cyan', 'brown']
i = 0
for uid in users:
    #plt.bar(x, y, align='center', tick_label=[str(x) for x in range(0, 24)], color='cadetblue', edgecolor='black',
    #       linewidth=.7)
    c.execute('SELECT created_at FROM messages WHERE is_bot=0 AND author_id=?', (uid,))
    data = c.fetchall()

    (x, y) = msgtime_hour(data)
    line = plt.plot(x, y, color=colors[i], marker='o', label=names[i])
    i += 1

plt.xlabel('Hour (EST)')
plt.ylabel('Messages Sent')
plt.title(f'Discord Message Send Frequency')
plt.legend()
plt.show()

