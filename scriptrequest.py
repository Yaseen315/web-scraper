from lxml import html
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def make_graph(weather, city):
    temprange = plt.axes()
    temprange.bar([1.5, 2.5, 3.5, 4.5, 5.5], weather['Min'], width=0.5, alpha=0.4)
    if len(weather['Max']) == 4:
        temprange.bar([1, 2, 3, 4], weather['Max'], width=0.5, alpha=0.4)
    elif len(weather['Max']) == 5:
        temprange.bar([1, 2, 3, 4, 5], weather['Max'], width=0.5, alpha=0.4)
    temprange.set_xticklabels(weather['Day'])
    temprange.set_ylim([min(weather['Min'].min(),0), weather['Max'].max()+1])
    temprange.set_ylabel('Temp in degrees')
    temprange.set_title('Weekly Temperature Fluctuations in ' + city[0])
    plt.show()

# Function for being lazy
def get_weather(url):
    page = requests.get(url)
    data = html.fromstring(page.content)

    # This is the city
    city = data.xpath('//*[@id="blq-content"]/div[1]/h1/span/text()')
    # This is the day
    day = data.xpath('//*[@id="blq-content"]/div[7]/div[2]/ul/li/a/div/h3/span/text()')
    # This is the maximum temp
    maxs = data.xpath('//*[@id="blq-content"]/div[7]/div[2]/ul/li/a/span[2]/span/span[1]/text()')
    # This is the minmium temp
    mins = data.xpath('//*[@id="blq-content"]/div[7]/div[2]/ul/li/a/span[3]/span/span[1]/text()')

    # If length of max list is 4 (i.e. it's nighttime) do this:
    if len(maxs) == 4:
        weather=-999*np.ones((5,3), dtype='object')
        weather[:,0] = day
        weather[1:,1] = [int(i) for i in maxs]
        weather[:,2] = [int(i) for i in mins]

    # If the length of max list is 5 (i.e. it's daytime) do this:
    elif len(maxs) == 5:
        weather=np.zeros((5,3), dtype='object')
        weather[:,0] = day
        weather[:,1] = [int(i) for i in maxs]
        weather[:,2] = [int(i) for i in mins]

    weather=np.ma.masked_array(weather, mask=(weather==-999), fill_value=0)
    # Print title
    print (city[0] + " five day forecast")
    # Print the data stuff
    print (weather)
    # Make a file
    weather = pd.DataFrame(weather, columns=['Day', 'Max', 'Min'])
    weather.to_csv(city[0] + ".csv")
    make_graph(weather, city)


Eugene_url = 'http://www.bbc.co.uk/weather/5725846'
Sydney_url = 'http://www.bbc.co.uk/weather/2147714'
London_url = 'http://www.bbc.co.uk/weather/2643743'


get_weather(Eugene_url)
get_weather(Sydney_url)
get_weather(London_url)

def below_zero(url):
    page = requests.get(url)
    data = html.fromstring(page.content)

    # This is the city
    city = data.xpath('//*[@id="blq-content"]/div[1]/h1/span/text()')
    # This is the day
    day = data.xpath('//*[@id="blq-content"]/div[7]/div[2]/ul/li/a/div/h3/span/text()')
    # This is the minmium temp
    min = data.xpath('//*[@id="blq-content"]/div[7]/div[2]/ul/li/a/span[3]/span/span[1]/text()')

    print (city[0] + " temperatures below 0 this week:")

    for x, y in zip(day, min):
        y = int(y)
        if y <= 0:
            print (x, y)

below_zero(Eugene_url)
below_zero(Sydney_url)
below_zero(London_url)
