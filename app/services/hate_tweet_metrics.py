from app.models import Tweets
from app import db

def metrics(acc_id):
    total_likes = Tweets.query.with_entities(
                    db.func.sum(Tweets.tweet_likes)
                ).filter(
                    Tweets.tweet_sentiment == 1,
                    Tweets.account_handler == acc_id  # Add this line to filter by account handler
                ).scalar()
    total_retweets = Tweets.query.with_entities(
                    db.func.sum(Tweets.tweet_retweets)
                ).filter(
                    Tweets.tweet_sentiment == 1,
                    Tweets.account_handler == acc_id  # Add this line to filter by account handler
                ).scalar()
    total_replies = Tweets.query.with_entities(
                    db.func.sum(Tweets.tweet_replies)
                ).filter(
                    Tweets.tweet_sentiment == 1,
                    Tweets.account_handler == acc_id  # Add this line to filter by account handler
                ).scalar()
    total_impressions = Tweets.query.with_entities(
                    db.func.sum(Tweets.tweet_impressions)
                ).filter(
                    Tweets.tweet_sentiment == 1,
                    Tweets.account_handler == acc_id  # Add this line to filter by account handler
                ).scalar()
    return {"likes":total_likes, "retweets":total_retweets, "replies":total_replies, "impressions":total_impressions}