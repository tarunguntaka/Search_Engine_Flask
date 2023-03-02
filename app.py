
#imports 
from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests 
import csv 
import time 
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd  
from google_scrapper import GoogleSearch
#------------------------------------------------------------------------------
app = Flask(__name__)

# A route to display the home page
@app.route("/")
def index():
    return render_template('index.html')

# A route to handle the search form submission
@app.route('/search', methods= ['POST'])
def search():
    # Get the search query and page number from the request form
    query = request.form['query']

    # Redirect to the results page with the search query and page number as parameters
    return redirect(url_for('results', query=query))

# A route to display the search results
@app.route('/results/<query>', methods = ['GET'])
def results(query):

    start = request.args.get('start')
    if start is None:
        start = 0
    else:
        start = int(start)

    
    g = GoogleSearch()
    df = g.search_google(query=query,start=start)
    df.to_csv('search_results_first10.csv', index=False)
    #num_results = len(df)
    #results = []
    
    #df1 = g.search_multiple_pages(query=query)
    #df1.to_csv('search_results_all.csv', index=False)
    
    #df_final = pd.concat([df,df1],axis=0)
    # for index, row in df_final.iterrows():
    #     result = {'title': row['title'], 'link': row['link']}
    #     results.append(result)
    
    return render_template('results.html', query=query, results=df,start=start)


#A route to update the click status of a search result
@app.route('/update_click_status', methods=['GET'])
def update_click_status():
    # Get the title and link of the search result from the request parameters
    title = request.args.get('title')
    link = request.args.get('link')

    # Get the current time before the user clicks on the link
    get_time = time.time()
    click_time = datetime.fromtimestamp(get_time).strftime('%H:%M:%S')

    # Open the CSV file in append mode
    with open('clicked_results.csv', 'a') as csvfile:
        # Create a writer object
        csv_writer = csv.writer(csvfile)

        # Write the title and link of the clicked search result to the CSV file
        csv_writer.writerow([title, link, click_time])

    # Return a success message as a JSON response
    return jsonify({'message': 'Successfully recorded clicked result'})



if __name__ =='__main__':
    app.run(port=4201, debug=True)
##--------------------------------------------------------------------------------------------