from dadjokes import Dadjoke
import discord
from discord.ext import commands
import requests

import geocoder
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


def distance_between(start, end):
    geolocator = Nominatim(user_agent="geolocation")

    location1 = geolocator.geocode(start)
    location1coords = (location1.latitude, location1.longitude)

    location2 = geolocator.geocode(end)
    location2coords = (location2.latitude, location2.longitude)

    geodistance = geodesic(location1coords, location2coords).miles
    return round(geodistance, 2)


def checkanagram(stringa, stringb):
    stringa = str(stringa).lower()
    stringb = str(stringb).lower()

    stringa = str(stringa[3:int(len(stringa) - 4)])
    stringb = str(stringb[3:int(len(stringb) - 4)])

    condition = ""

    stringa = sorted(stringa)
    stringb = sorted(stringb)

    
    if(len(stringa) != len(stringb)):
        condition = "FALSE"
    else:
        if(stringa.sort() == stringb.sort()):
            condition = "TRUE"

    return condition


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.messages = True
    intents.guilds = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    DISCORD_TOKEN = "MTE1NDE3NzY0NDYwMzEyNTg4Mg.GMaBrS.G-gP7okwo62JwxsRvxkXIFSDOFyIRdTxAUJZ0g" 
    API_KEY = "a11d4dfebd37aad46090286fdfff81ac" #API KEY FOR WEATHER
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    string1 = []
    string2 = []


    @bot.event
    async def on_ready():
        guild_count = len(bot.guilds)
        print(f"{bot.user} has connected to discord!")
        print(f"Bot is in " + str(guild_count) + " servers")

    @bot.command()
    async def joke(message):
        dadjoke = Dadjoke()
        await message.reply(dadjoke.joke)

    @bot.command()
    async def weather(message, *, city: str):
        complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        y = x["main"]
        current_temperature = y["temp"]
        current_temperature_farrenheit = str(round((current_temperature - 273.15) * 9/5 + 32))
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        await message.send(f"Weather in {city}\n Description\n {weather_description}\n Temperature(F)\n {current_temperature_farrenheit}\n Humidity(%)\n {current_humidity}\n Atmospheric Pressure(hPa)\n {current_pressure}")

    @bot.command()
    async def mylocation(message):
        mylocation = geocoder.ip("me")
        await message.send(f"Your current location is nearby the coordinates {mylocation.latlng}")
        await message.send(f"https://www.openstreetmap.org/search?query=%5B{mylocation.lat}%2C%20{mylocation.lng}%5D#map=19/{mylocation.lat}/{mylocation.lng}")
    
    @bot.command()
    async def distance(message, location1, location2):
        await message.send(f"the distance between {location1} and {location2} is {distance_between(location1,location2)} miles")

    @bot.command()
    async def stringa(message, *stringa):
        string1.append(stringa)
        await message.send(f"The first string is {stringa}")

    @bot.command()
    async def stringb(message, *stringb):
        string2.append(stringb)
        await message.send(f"The second string is {stringb}")

    @bot.command()
    async def isanagram(message):
        await message.send(f"it is {checkanagram(string1,string2)} that {string1} is an anagram of {string2}")



    bot.run(DISCORD_TOKEN)

main()