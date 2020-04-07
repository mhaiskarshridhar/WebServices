from flask import Flask, render_template,request
import requests
import pandas as pd      

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/select",methods=['GET', 'POST'])
def country():
    if request.method == "POST":
        country = request.form.get('country')
        #return from API 1
        capital_city=get_capital(country)
        #return from API 2
        api_response=get_weather(capital_city)
        #API 3
        temperature=api_response['current']['temperature']
        city_name=api_response['location']['name']
       
        weather_description=api_response['current']['weather_descriptions']
        weather_description=weather_description[0]
        df = pd.read_csv('final_places.csv')
        if temperature <= 15 :
            if city_name=='Canberra':
                df2=df.loc[(df['City'] == 'Canberra') & (df['Season'] == 'Winter')]
                places2visit=df2['Place'][0]
                places2visit2=df2['Place2'][0]
            elif city_name=='Washington':
                df2=df.loc[(df['City'] == 'Washington') & (df['Season'] == 'Winter')]
                places2visit=df2['Place'][2]
                places2visit2=df2['Place2'][2]
            elif city_name=='Madrid':
                df2=df.loc[(df['City'] == 'Madrid') & (df['Season'] == 'Winter')]
                places2visit=df2['Place'][4]
                places2visit2=df2['Place2'][4]
        else:
            if city_name=='Canberra':   
                df2=df.loc[(df['City'] == 'Canberra') & (df['Season'] == 'Summer')]
                places2visit=df2['Place'][1]
                places2visit2=df2['Place2'][1]
            elif city_name=='Washington':
                df2=df.loc[(df['City'] == 'Washington') & (df['Season'] == 'Summer')]
                places2visit=df2['Place'][3]
                places2visit2=df2['Place2'][3]
            elif city_name=='Madrid':
                df2=df.loc[(df['City'] == 'Madrid') & (df['Season'] == 'Summer')]
                places2visit=df2['Place'][5]
                places2visit2=df2['Place2'][5]
    
        return render_template("graph.html",places2visit=places2visit,places2visit2=places2visit2,weather_description=weather_description)
#API 1
def get_capital(country):
    api_result = requests.get('http://restcountries.eu/rest/v2/name/'+country)
    api_response = api_result.json()
    capital_city=api_response[0]['capital']
    return capital_city
#API 2
def get_weather(capital_city):
    api_result = requests.get('http://api.weatherstack.com/current?access_key=07a27e7c5eac1a83378e327935d003bb&query='+capital_city)
    api_response = api_result.json()
    return api_response
                
if __name__ == "__main__":
    app.run(debug=False)
