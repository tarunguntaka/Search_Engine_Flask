import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class relevantlink:
    def __init__(self, data_path):
        self.df = pd.read_csv(data_path)
        self.link_features = ['title', 'description']
        self.result_df = None
        self.df = self._tweak_df(self.df)
        
        self.clicked_links = self.df[self.df['Click_Status'] == True]
        self.non_clicked_links = self.df[self.df['Click_Status']== False]
        
        self.vectorizer = TfidfVectorizer()
        
    def _tweak_df(self, df):
        #cols = ['title', 'link', 'Click_Status', 'description', 'Click_Time']
        return (
            df
            .astype({'title':'string','link':'string','description':'string'})
            .drop(columns=['Click_Time'])
            #.info()
        )

    def _find_similar_links(self):
        
        
        clicked_vectors = self.vectorizer.fit_transform(self.clicked_links[self.link_features].apply(lambda x: ' '.join(x), axis=1))
        non_clicked_vectors= self.vectorizer.transform(self.non_clicked_links[self.link_features].apply(lambda x: ' '.join(x), axis=1))
        
        similarity_scores = cosine_similarity(clicked_vectors, non_clicked_vectors)
        
        top_indices = similarity_scores.argsort()[:, ::-1][:, :10]
        top_links = self.non_clicked_links.iloc[top_indices.flatten()][['title', 'link', 'description']].reset_index(drop=True)
        
        self.result_df = top_links.head(10)

        return self.result_df
    
    
# rl = relevantlink('search_results_machine learning.csv')
# print(rl.clicked_links)
# result_df = rl._find_similar_links()
# print(result_df)