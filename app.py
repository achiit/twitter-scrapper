

# from flask import Flask, request, jsonify
# from ntscraper import Nitter
# import pandas as pd

# app = Flask(__name__)

# scraper = Nitter()

# def get_tweets(name, modes, no):
#     tweets = scraper.get_tweets(name, mode = modes, number=no)
#     final_tweets = []
#     for x in tweets['tweets']:
#         data = [x['link'], x['text'],x['date'],x['stats']['likes'],x['stats']['comments']]
#         final_tweets.append(data)
#     dat= pd.DataFrame(final_tweets, columns =['twitter_link','text','date','likes','comments'])
#     return dat


# def get_profile_info(username):
#     return scraper.get_profile_info(username)

# @app.route('/tweets', methods=['POST'])
# def fetch_tweets():
#     data = request.json
#     username = data.get('username')
#     if not username:
#         return jsonify({'error': 'Username not provided in the request body'}), 400
#     mode = data.get('mode', 'user')
#     number = int(data.get('number', 5))
#     tweets_df = get_tweets(username, mode, number)
    
#     # Convert DataFrame to list of dictionaries
#     tweets_list = tweets_df.to_dict(orient='records')
    
#     return jsonify(tweets_list)


# @app.route('/profileimg', methods=['POST'])
# def get_image():
#     data = request.json
#     username = data.get('username')
#     if not username:
#         return jsonify({'error': 'Username not provided in the request body'}), 400
#     profile_info = get_profile_info(username)
#     return jsonify(profile_info['image'])


# @app.route('/profile', methods=['POST'])
# def fetch_profile():
#     data = request.json
#     username = data.get('username')
#     if not username:
#         return jsonify({'error': 'Username not provided in the request body'}), 400
#     profile_info = get_profile_info(username)
#     return jsonify(profile_info)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, jsonify, render_template, request
from ntscraper import Nitter
import pandas as pd
import gradio as gr

app = Flask(__name__)
scraper = Nitter()

def get_tweets(username, mode='user', number=5):
    tweets = scraper.get_tweets(username, mode=mode, number=number)
    final_tweets = []
    for tweet in tweets['tweets']:
        data = {
            'twitter_link': tweet['link'],
            'text': tweet['text'],
            'date': tweet['date'],
            'likes': tweet['stats']['likes'],
            'comments': tweet['stats']['comments']
        }
        final_tweets.append(data)
    return final_tweets

def get_profile_info(username):
    return scraper.get_profile_info(username)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tweets', methods=['POST'])
def fetch_tweets():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username not provided in the request body'}), 400
    mode = data.get('mode', 'user')
    number = int(data.get('number', 5))
    tweets = get_tweets(username, mode, number)
    return jsonify(tweets)

def predict(username, mode, number):
    tweets = get_tweets(username, mode, number)
    return pd.DataFrame(tweets)

iface = gr.Interface(fn=predict, inputs=["text", "text", "number"], outputs="dataframe")
iface.launch()
