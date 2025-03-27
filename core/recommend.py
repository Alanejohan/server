#importing the required libraries
import os
import nltk
nltk.download('wordnet')
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from ast import literal_eval


#importing the scrapped dataset
data = pd.read_csv(os.getcwd() + '/clean-dataset.csv')
#dropping the columns that will not be used for the recommendation
data.drop(labels=['Phone_Number', 'Addresss', 'Num_rating', 'Rating', 'Price', 'Website_URL', 'Latitudes', 'Longitudes', 'Image_URL',],axis=1,inplace=True)
#creating a tag that will be used to create the natural language processing model
data['Tag'] = data['Title'] + data['Cleaned Addresss'] + data['Cleaned Category'] + data['Description']


def hello():    
    print("HEAD", data.head())

#creating the function to take in the category and the description of the loction and comparing it to our categories
#and data tag to find the place that matches the most our specified description.
def recommend_place(categories, description):
    # 
    train_data = data
    #converting all our tags to lowercase letters to ensure the query is accurate
    train_data['Tag'] = data['Tag'].str.lower()
    train_data['Category'] = data['Category'].str.lower()
    # 
    description = description.lower()
    word_tokenize(description)
    stop_words = stopwords.words('english') #removing stop words from dataset e.g I, the
    lemm = WordNetLemmatizer()
    filtered  = {word for word in description if not word in stop_words} #
    filtered_set = set()
    for fs in filtered:
        filtered_set.add(lemm.lemmatize(fs)) #lemmatize each english word so it can be seen as an english word

    cat = train_data[train_data['Category']==categories.lower()]
    cat = cat.set_index(np.arange(cat.shape[0]))
    list1 = []; list2 = []; cos = [];
    for i in range(cat.shape[0]):
        temp_token = word_tokenize(cat["Tag"][i])
        temp_set = [word for word in temp_token if not word in stop_words]
        temp2_set = set()
        for s in temp_set:
            temp2_set.add(lemm.lemmatize(s))
        vector = temp2_set.intersection(filtered_set)
        cos.append(len(vector))
    cat['similarity']=cos
    cat = cat.sort_values(by='similarity', ascending=False)
    cat.drop_duplicates(subset='Title', keep='first', inplace=True)
    cat.sort_values('Rating Count', ascending=False, inplace=True)
    cat.reset_index(inplace=True)
    return cat[["Title", "Rating Count", "Category", "Business Id"]].head(12)



