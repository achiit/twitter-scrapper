# from ntscraper import Nitter
# import pandas as pd
# scraper = Nitter(0)
# def get_tweets(name, modes, no):
#     tweets = scraper.get_tweets(name, mode = modes, number=no)
#     final_tweets = []
#     for x in tweets['tweets']:
#         data = [x['link'], x['text'],x['date'],x['stats']['likes'],x['stats']['comments']]
#         final_tweets.append(data)
#     dat= pd.DataFrame(final_tweets, columns =['twitter_link','text','date','likes','comments'])
#     return dat
# # scraper = Nitter(log_level=1, skip_instance_check=False)
# bezos_information = scraper.get_profile_info("narendramodi")
# # tweets
# x=bezos_information['image']
# data = get_tweets('narendramodi','user',6)
# data.to_csv('tweets.csv')
# scraper.get_profile_info('BillGates')
# print(x)

from flask import Flask, request, jsonify
from ntscraper import Nitter
import pandas as pd

app = Flask(__name__)

scraper = Nitter()

def get_tweets(name, modes, no):
    tweets = scraper.get_tweets(name, mode = modes, number=no)
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'],x['date'],x['stats']['likes'],x['stats']['comments']]
        final_tweets.append(data)
    dat= pd.DataFrame(final_tweets, columns =['twitter_link','text','date','likes','comments'])
    return dat


def get_profile_info(username):
    return scraper.get_profile_info(username)

@app.route('/tweets', methods=['POST'])
def fetch_tweets():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username not provided in the request body'}), 400
    mode = data.get('mode', 'user')
    number = int(data.get('number', 5))
    tweets_df = get_tweets(username, mode, number)
    
    # Convert DataFrame to list of dictionaries
    tweets_list = tweets_df.to_dict(orient='records')
    
    return jsonify(tweets_list)


@app.route('/profileimg', methods=['POST'])
def get_image():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username not provided in the request body'}), 400
    profile_info = get_profile_info(username)
    return jsonify(profile_info['image'])


@app.route('/profile', methods=['POST'])
def fetch_profile():
    data = request.json
    username = data.get('username')
    if not username:
        return jsonify({'error': 'Username not provided in the request body'}), 400
    profile_info = get_profile_info(username)
    return jsonify(profile_info)

if __name__ == '__main__':
    app.run(debug=True)
