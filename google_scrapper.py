import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 

class GoogleSearch:
    def __init__(self):
        self.base_url = "https://google.com/search"
        self.results_df = pd.DataFrame()

    def search_google(self, query, start=0):
        query = query.replace(' ', '+')
        url = f"{self.base_url}?q={query}&start={start}"
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        headers = {"user-agent": user_agent}
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:           
            soup = BeautifulSoup(response.content, "html.parser")
            results = []
            def_click= False
            for i, g in enumerate(soup.find_all('div', class_='yuRUbf')):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    if i < len(results):
                        results[i]['title'] = title
                        results[i]['link'] = link
                    else:
                        results.append({'title': title, 'link': link, 'Click_Status': def_click})
            for i, g in enumerate(soup.find_all('div', class_='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc lEBKkf')):
                span_elements = g.find_all('span')
                if span_elements:
                    description =' '.join([span.text for span in span_elements]) 
                    if i < len(results):
                        results[i]['description'] = description
                    else:
                        results.append({'description': description})
                else:
                    description = ' '
                    if i < len(results):
                        results[i]['description'] = description
                    else:
                        results.append({'description': description})

            df = pd.DataFrame(results)
            df['Click_Status']=False
            if start == 0:
                self.results_df = df
            else:
                self.results_df = self.results_df.append(df, ignore_index=True)

            #self.results_df.to_csv('search_results.csv', index=False)
            return self.results_df
        else:
            return pd.DataFrame()

    def search_multiple_pages(self, query):
        dfs = pd.DataFrame()
        for start in range(0, 50, 10):
            df = self.search_google(query, start=start)
            dfs = pd.concat([df,dfs],axis=0)
            time.sleep(0.2)
        return dfs.drop_duplicates()


# g = GoogleSearch()

# df = g.search_google(query="ai",start=20)
# df.to_csv('first20.csv', index=False)

# df2 = g.search_multiple_pages(query="machine learning")
# df2.to_csv('ml.csv', index=False)