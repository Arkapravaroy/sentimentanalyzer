#!/usr/bin/env python
import flask
from flask import Flask, jsonify, abort, make_response, request, render_template
import json
import pickle
import re
import tweepy
from textblob import TextBlob
import warnings
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import regularizers
def clean_tweet(tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
def get_tweet_sentiment(tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        testtweet=clean_tweet(tweet)
        analysis = model.predict(testtweet)
        # analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return ['positive',float(analysis.sentiment.polarity)]
        elif analysis.sentiment.polarity == 0:
            return ['neutral',float(analysis.sentiment.polarity)]
        else:
            return ['negative',float(analysis.sentiment.polarity)]



@app.route('/result',methods = ['POST'])
def execute_xgboost():
    input_map = dict(request.form.to_dict())
    search_query=input_map['Enter the input text']
    print('calling sentence analyzer')
    sentiment_metadata=get_tweet_sentiment(search_query)
    final_dic={}
    final_dic["Sentiment detected"]=sentiment_metadata[0]
    final_dic["Confidence score"]=sentiment_metadata[1]
    final_dic["Algorithm Used"]="MODEL"
    #final_dic = flask.Response(json.dumps(final_dic))
    print(final_dic)
    return render_template("result.html",result=final_dic)



@app.errorhandler(404)
def not_found(error):
    resp = flask.Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/',methods=['GET', 'POST'])
def index():
    return (render_template('index.html'))

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)
