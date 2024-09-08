from flask import render_template, redirect, url_for,request
from app import app, db
from app.forms import AccountForm
from app.models import tokenizer,model,Account,Tweets
from app.services.preprocess import clean_data
from app.services.tweets_api import fetch
from app.services.user_id import user_id
from app.services.save_img import save_img
from app.services.explainable_ai import generate_lime_explanation,graph,create_line_graph
from app.services.hate_tweet_metrics import metrics
from datetime import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/account', methods=['GET', 'POST'])
def account():
    key="data"
    form = AccountForm()
    if form.validate_on_submit():
        acc_handler = form.account.data.lower().replace("@","")
        account_fetched = Account.query.filter_by(account_handler=acc_handler).first()
        if account_fetched:
            fetched_date = account_fetched.account_last_fetched
            current_date = datetime.today().date()
            date_diff = current_date - fetched_date
            if date_diff.days < 1:
                image_filename = f"{acc_handler}_graph.jpg"
                return redirect(url_for('display',acc_handler=acc_handler,acc_graph=image_filename))
        user_res = user_id(acc_handler)
        if key not in user_res:
            message = "This username doesn't exist, please insert a valid one"
            return render_template('account.html', message = message, form=form)
            
        user = user_res["data"]
        user_img = save_img(user["profile_image_url"],acc_handler)
        tweets = fetch(user["id"])
        if account_fetched:
            neutral_tweets = account_fetched.neutral_tweets
            hateful_tweets = account_fetched.hateful_tweets
        else:
            neutral_tweets = 0
            hateful_tweets = 0
        for tweet in tweets:
            tweet_exist = Tweets.query.filter_by(tweet_id=tweet["id"]).first()
            if tweet_exist:
                continue 
            cleaned_tweet= clean_data(tweet["text"])
            if cleaned_tweet == "":
                continue
            inputs = tokenizer(cleaned_tweet, return_tensors="pt")
            outputs = model(**inputs)
            predictions = outputs.logits.argmax(-1)
            if predictions == 0:
                neutral_tweets += 1
            else: 
                hateful_tweets += 1
                generate_lime_explanation(cleaned_tweet,tweet["id"])
            tweet_date = datetime.strptime(tweet["created_at"][:10], '%Y-%m-%d').date()
            add_tweet=Tweets(tweet_id=tweet["id"] ,tweet_date = tweet_date , tweet_likes=tweet["public_metrics"]["like_count"],
                            tweet_retweets=tweet["public_metrics"]["retweet_count"],tweet_replies=tweet["public_metrics"]["reply_count"],
                            tweet_impressions=tweet["public_metrics"]["impression_count"],
                            account_handler=acc_handler,tweet_text=tweet["text"],
                             cleaned_tweet=cleaned_tweet, tweet_sentiment=predictions.item())
            db.session.add(add_tweet)
            try:
                db.session.commit()
            except Exception as e: 
                print(e)
                db.session.rollback()
        
        total = (neutral_tweets+hateful_tweets)
        perc = (hateful_tweets/total) *100
        if perc > 10:
            account_profile = 'Hateful'
        else: 
            account_profile = 'Neutral'
        if account_fetched:
            account_fetched.neutral_tweets = neutral_tweets
            account_fetched.hateful_tweets = hateful_tweets
            account_fetched.account_classification = account_profile
            account_fetched.account_last_fetched = datetime.today().date()
            try:
                db.session.commit()
            except:
                db.session.rollback()
        else:
            account = Account(account_handler=acc_handler,account_last_fetched = datetime.today().date(),
                           account_name=user["name"],account_followers= user["public_metrics"]["followers_count"],
                           account_following=user["public_metrics"]["following_count"],neutral_tweets=neutral_tweets,
                           hateful_tweets=hateful_tweets, account_img=user_img, account_classification=account_profile)
            db.session.add(account)
            try:
                db.session.commit()
            except:
                db.session.rollback()
        return redirect(url_for('display',acc_handler=acc_handler))
    
    return render_template('account.html', title='Classification', form=form)


@app.route('/display', methods=['GET', 'POST'])
def display():
    acc_id = request.args.get('acc_handler')
    acc_graph = graph(acc_id)
    acc_line_graph = create_line_graph(acc_id)
    account = Account.query.get(acc_id)

    if account.hateful_tweets == 0:
        return render_template('display.html', account=account,acc_graph=acc_graph,acc_line_graph=acc_line_graph,hate_metrics = None)
    else:
        hate_metrics = metrics(acc_id)
        return render_template('display.html', account=account,acc_graph=acc_graph,acc_line_graph=acc_line_graph,hate_metrics = hate_metrics)



