from lxml import html
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Creates a graph, called in the get_weather function at the end
def make_graph(weather, city):
    temprange = plt.axes()
    # Alpha gives transparency, lets you see if anything is being covered up
    temprange.bar([1.5, 2.5, 3.5, 4.5, 5.5], weather['Min'], width=0.5, alpha=0.4)
    # Deals with the issue of missing data, using an if statement
    if len(weather['Max']) == 4:
        temprange.bar([1, 2, 3, 4], weather['Max'], width=0.5, alpha=0.4)
    elif len(weather['Max']) == 5:
        temprange.bar([1, 2, 3, 4, 5], weather['Max'], width=0.5, alpha=0.4)
    # Labels the x axis with the days
    temprange.set_xticklabels(weather['Day'])
    # Sets the limits of the y axis, from the minimum or 0 (whatever is lower) to the maximum +1 (so that the maximum can be seen)
    temprange.set_ylim([min(weather['Min'].min(),0), weather['Max'].max()+1])
    temprange.set_ylabel('Temp in degrees')
    temprange.set_title('Weekly Temperature Fluctuations in ' + city[0])
    plt.show()

# Function to get the weather
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
        weather=-999*np.ones((5,3), dtype='object') # Deals with the missing data issue, sets any missing data as -999 so it can't be mixed up
        weather[:,0] = day
        # Note that this is different from the elif statement below: [1:,1] instead of [:,1]. Handling the missing data issue
        weather[1:,1] = [int(i) for i in maxs]
        weather[:,2] = [int(i) for i in mins]

    # If the length of max list is 5 (i.e. it's daytime) do this:
    elif len(maxs) == 5:
        weather=np.zeros((5,3), dtype='object')
        weather[:,0] = day
        weather[:,1] = [int(i) for i in maxs] # Converts data to an integer, similar to the below 0 function. Error runs without this line
        weather[:,2] = [int(i) for i in mins]

    # Masks any -999 in weather, fill value means to blank them out
    weather=np.ma.masked_array(weather, mask=(weather==-999), fill_value=0)
    # Print title
    print (city[0] + " five day forecast") # City is an array with one item, to get the city name as we want it we need city[0]
    # Print the data stuff
    print (weather)
    # Make a file
    root = "/home/grace/Desktop/Web Scraper Project/"
    weather = pd.DataFrame(weather, columns=['Day', 'Max', 'Min']) # Labels the columns
    filename = city[0] + ".csv"
    with open(root + filename, "a") as f:
        weather.to_csv(f, header=False) # Appending so that we can collect data over time
    #weather.to_csv(city[0] + ".csv") Magic one line code for making a csv file
    #make_graph(weather, city)


Eugene_url = 'http://www.bbc.co.uk/weather/5725846'
Sydney_url = 'http://www.bbc.co.uk/weather/2147714'
London_url = 'http://www.bbc.co.uk/weather/2643743'


get_weather(Eugene_url)
get_weather(Sydney_url)
get_weather(London_url)

# Function to show you any days where the temperature is below 0
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
        y = int(y) # Similar to the int(i) in get_weather function. Stops wrong datatypes causing errors
        if y <= 0:
            print (x, y)

# below_zero(Eugene_url)
# below_zero(Sydney_url)
# below_zero(London_url)
