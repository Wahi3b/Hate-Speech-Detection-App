from datetime import date
from app import db
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained('./roBERTa-model')
model = AutoModelForSequenceClassification.from_pretrained('./roBERTa-model')

class Account(db.Model):
    __tablename__ = 'accounts'
    account_handler = db.Column(db.String,primary_key=True, nullable=False, unique=True)
    account_last_fetched = db.Column(db.Date,nullable=False) 
    account_name = db.Column(db.String, nullable=False)
    account_followers = db.Column(db.Integer, nullable=False)
    account_following = db.Column(db.Integer, nullable=False)
    neutral_tweets = db.Column(db.Integer, nullable=False)
    hateful_tweets = db.Column(db.Integer, nullable=False)
    account_classification = db.Column(db.String(32), nullable=False)
    account_img = db.Column(db.String, nullable=False)
    tweets = db.relationship('Tweets', backref='account', lazy='dynamic')

class Tweets(db.Model):
    __tablename__ = 'tweets'
    tweet_id = db.Column(db.Integer, primary_key=True)
    tweet_date = db.Column(db.DateTime,nullable=False)  
    tweet_likes = db.Column(db.Integer,nullable=False)
    tweet_retweets = db.Column(db.Integer, nullable=False)
    tweet_replies = db.Column(db.Integer, nullable=False)
    tweet_impressions = db.Column(db.Integer, nullable=False)
    account_handler = db.Column(db.String, db.ForeignKey('accounts.account_handler'), nullable=False)
    tweet_text = db.Column(db.Text, nullable=False)
    cleaned_tweet = db.Column(db.Text, nullable=False)
    tweet_sentiment = db.Column(db.Integer, nullable=False)
    words = db.relationship('Explainable', backref='explainable', lazy='dynamic')

class Explainable(db.Model):
    __tablename__ = 'explainable'
    word_id = db.Column(db.Integer, primary_key=True)  
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.tweet_id'), nullable=False) 
    tweet_word = db.Column(db.Text, nullable=False)
    word_probability = db.Column(db.Integer, nullable=False)
    
   





