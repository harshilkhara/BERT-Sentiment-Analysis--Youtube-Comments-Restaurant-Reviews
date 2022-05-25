# -*- coding: utf-8 -*-
"""Sentiment Analysis-YouTube comments & Restaurant Reviews.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sP0A8FdmGstxBVG_mc94dXTuART3gAhx
"""

pip install transformers

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import requests
from bs4 import BeautifulSoup
import re

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tokens = tokenizer.encode('It was okayish', return_tensors='pt')
result = model(tokens)
result
result.logits
int(torch.argmax(result.logits))+1

# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = ""

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey= DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        order="relevance",
        videoId="pfqtj3aFBtI"
    )
    response = request.execute()
    return response
  


result=main()
#print(result['pageInfo']['totalResults'])
x=(result['pageInfo']['totalResults'])
result1=[]
for i in range(x):
  result1.append(str(result['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']) )
print(result1)

import numpy as np
import pandas as pd

df = pd.DataFrame(np.array(result1), columns=['reviews'])

df

def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits))+1

sentiment_score(df['reviews'].iloc[0])

df['sentiment'] = df['reviews'].apply(lambda x: sentiment_score(x[:512]))

df

average_sentiment=(sum(df['sentiment']))/(len(df['sentiment']))

average_sentiment

r = requests.get('https://www.yelp.com/biz/social-brew-cafe-pyrmont')
soup = BeautifulSoup(r.text, 'html.parser')
regex = re.compile('.*comment.*')
results = soup.find_all('p', {'class':regex})
reviews1 = [result.text for result in results]

df1 = pd.DataFrame(np.array(reviews1), columns=['reviews'])
df1['reviews'].iloc[0]
def sentiment_score(review):
    tokens = tokenizer.encode(review, return_tensors='pt')
    result = model(tokens)
    return int(torch.argmax(result.logits))+1

sentiment_score(df1['reviews'].iloc[1])

df1['sentiment'] = df1['reviews'].apply(lambda x: sentiment_score(x[:512]))

df1

average_sentiment1=(sum(df1['sentiment']))/(len(df1['sentiment']))

average_sentiment1