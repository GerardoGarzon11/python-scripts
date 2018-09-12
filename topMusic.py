#! python3
#  topMusic.py

# TODO: Define method for requests
# TODO: Configuration file for fast load (not having to write username again and again)
# TODO: Clean code (it's messy)

from datetime import date
from datetime import timedelta
import calendar
import requests
import bs4

baseURL = "https://www.last.fm/user/"
selectionURL = {
	"artists": "/library/artists?from=",
	"albums": "/library/albums?from=",
	"tracks": "/library/tracks?from="
}
toURL = "&to="

timeRange = {
	"current": {
		"start": None,
		"end": None,
	},
	"previous": {
		"start": None,
		"end": None
	}
}

def getTimeRange(period):

	today = date.today()
	year = today.year

	if (period == 'W' or period == 'w'):
		weekStart = today - timedelta(today.weekday())
		timeRange['current']['start'] = today - timedelta(today.weekday())
		timeRange['current']['end'] = today + timedelta(6 - today.weekday())
		timeRange['previous']['start'] = weekStart - timedelta(7)
		timeRange['previous']['end'] = weekStart - timedelta(1)
	elif (period == 'M' or period == 'm'):
		first = today.replace(day = 1)
		lastMonth = (first - timedelta(days = 1)).replace(day = 1)
		timeRange['current']['start'] = str(year) + "-" + str(today.month) + "-01"
		timeRange['current']['end'] = str(year) + "-" + str(today.month) + "-" + str(calendar.monthrange(year, today.month)[1])
		timeRange['previous']['start'] = str(lastMonth.year) + "-" + str(lastMonth.month) + "-01"
		timeRange['previous']['end'] = str(lastMonth.year) + "-" + str(lastMonth.month) + "-" + str(calendar.monthrange(lastMonth.year, lastMonth.month)[1])
	else:
		timeRange['current']['start'] = str(year) + "-01-01"
		timeRange['current']['end'] = str(year) + "-12-31"
		timeRange['previous']['start'] = str(year - 1) + "-01-01"
		timeRange['previous']['end'] = str(year - 1) + "-12-31"

def getURL(username):
	return baseURL + username + selectionURL['artists'] + str(timeRange['current']['start']) + toURL + str(timeRange['current']['end'])

def performRequest(url):
	res = requests.get(url)
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text)
	chartlist = soup.select('#top-artists-section table tbody tr ')

	if len(chartlist) <= 10:
		rangeLength = len(chartlist)
	else:
		rangeLength = 10

	for x in range(0, rangeLength):
		print(str(x+1) + " - " + chartlist[x].select('.link-block-target')[0].getText())
		print("Plays: " + chartlist[x].select('.countbar-bar-value-wrapper')[0].getText().strip())

# TODO: Load configuration

print('Username:')
username = input()

print('Which period do you want to analyze? [W/M/Y]')
period = input()

getTimeRange(period)

# for week (get top 10)
# for month (get top 10)
# for year (get top 10)

url = getURL(username)
performRequest(url)
