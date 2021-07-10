from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2020-01-01&end_date=2021-06-30#panel')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('table', attrs={'class':'table table-striped text-sm text-lg-normal'})
row = table.find_all('tr')
row_length = len(row)


temp = [] #initiating a list 
for i in range(1, row_length):
    
    #get date 
    Date = row[i].find_all('th', attrs ={'class':'font-semibold text-center'})[0].text
    Date = Date.strip()
       
    #get volume
    Volume = row[i].find_all('td', attrs ={'class':'text-center'})[1].text
    Volume= Volume.strip()
    
    
    #scrapping process
    temp.append((Date, Volume))

temp = temp[::-1]

#change into dataframe
df = pd.DataFrame(temp, columns = ('Date','Volume'))

#insert data wrangling here
df['Volume'] = df['Volume'].str.replace(",","")
df['Volume'] = df['Volume'].str.replace("$","")

df['Date'] = df['Date'].astype('datetime64')
df['Volume'] = df['Volume'].astype('float64')
df = df.set_index('Date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["Volume"].mean().round(2)}' #be careful with the " and ' 
    #data_df = f'{DataFrame}'
	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result,
		
		)


if __name__ == "__main__": 
    app.run(debug=True)