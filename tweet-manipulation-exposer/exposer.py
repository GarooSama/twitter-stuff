# The script should be provided with Twitter & Imgur API keys in lines 16-25, and a tweet URL in line 46.
# It will iterate through the replies of the tweet and match replies that contain specific keywords (blacklist.txt) OR the reply author has a high follower count.
# Matched tweet details are saved into a generated CSV along with a screenshot link of it in case it gets deleted.
# The use case of this script is very specific, and that is to expose tweet interaction manipulation in Saudi Twitter by user groups that reply to each other's ads.

import csv
import os
import time
import datetime
import tweepy
import asyncio
from tweetcapture import TweetCapture
from imgurpython import ImgurClient

######### Fill this section #########
# Twitter API
api_key = ""
api_secret = ""
access_token = ""
access_token_secret = ""
# Imgur API
client_id = ''
client_secret = ''
imgur_access_token = ''
refresh_token = ''

# create authentication for accessing Twitter
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)
# initialize Tweepy API
api = tweepy.API(auth)
# initialize Imgur API
imgur_client = ImgurClient(client_id, client_secret, imgur_access_token, refresh_token)
# create an object of TweetCapture to screenshot tweets
tweet_capture = TweetCapture()
# a variable as a template for reply URLs
link = 'https://twitter.com/'

  
# read and create a list of blacklisted words from a file
with open('blacklist.txt', 'r', encoding='UTF8') as f:
    blacklist  = [line.strip() for line in f]

# fetch the tweet from URL and proccess some variables
######### Fill this variable #########
tweet_url = ""
tweet_id = tweet_url.split('/')[-1]
tweet = api.get_status(tweet_id)
user_object = tweet.author 
user = user_object.screen_name

# variable for the screenshot file name
screenshot_file = 'screenshot.png'
# screenshot the reply
asyncio.run(tweet_capture.screenshot(tweet_url, screenshot_file, mode=3, night_mode=2))
# upload to imgur and parse the link
image = imgur_client.upload_from_path(screenshot_file, config=None, anon=True)
image_url = image["link"]
# delete the screenshot from disk
os.remove(screenshot_file)

# prepare CSV headers
header = ['User ID', 'Username', 'Display Name', 'Follower Count', 'Reply', 'Screenshot']

# prepare CSV file name variable
file = 'replies_to_'+ user + '_' + tweet_id + '.csv'

count = 0

# open the CSV file in the write mode
with open(file, 'w', encoding='UTF8', newline='') as f:
    # create the csv writer
    writer = csv.writer(f)
    # write wthe original tweet header
    writer.writerow(['Author User ID', 'Author Username', 'Author Display Name', 'Author Follower Count', 'Original Tweet'])
    # write the original tweet details
    writer.writerow([user_object.id_str, user, user_object.name, user_object.followers_count, tweet.text.replace("\n", " "), image_url])
    # write the replies header
    writer.writerow(header)
    # initalize a list for replies
    replies = []
    print('Iterating replies...')
    # start populating the list with replies to the user since the tweet time
    replies = tweepy.Cursor(api.search_tweets, q='to:{}'.format(user),
                                    since_id=tweet_id, tweet_mode='extended').items()
    while True:
        try:
            # move the cursor to the next reply
            reply = replies.next()
            time.sleep(5)
            count = count + 1
            print('Counter increased')
            # skip if the reply is to a deleted tweet
            if not hasattr(reply, 'in_reply_to_status_id_str'):
                continue
            # check if the reply is to the desired tweet
            if (reply.in_reply_to_status_id_str == tweet_id):
                # skip if the reply is by the author to him/herself
                if (reply.author.screen_name == user):
                    continue
                # check if the reply author has a high follower count
                if (reply.author.followers_count > 8000
                # or check if the reply is short and contains a word from the blacklist
                or (any(word in reply.full_text for word in blacklist)
                and len(reply.full_text) < 16)):
                    print('Reached reply number: ' + str(count))
                    reply_url = link + reply.author.screen_name + '/status/' + reply.id_str
                    # screenshot the reply
                    asyncio.run(tweet_capture.screenshot(reply_url, screenshot_file, mode=3, night_mode=2))
                    # upload to imgur and parse the link
                    image = imgur_client.upload_from_path(screenshot_file, config=None, anon=True)
                    image_url = image["link"]
                    # delete the screenshot from disk
                    os.remove(screenshot_file)
                    # write the reply details in the CSV file
                    data = [reply.author.id_str, reply.author.screen_name, reply.author.name, reply.author.followers_count, reply.full_text.replace("\n", " "), image_url]
                    writer.writerow(data)
        # raise an exception if the API rate limit reached
        except tweepy.TooManyRequests as e:
            print("Twitter API rate limit reached ".format(e))
            time.sleep(60)
            continue
        except tweepy.TweepyException as e:
            print("Tweepy error occured: {}".format(e))
            break
        # break condition if finished iterating all replies
        except StopIteration:
            # delete the screenshot from disk
            os.remove(screenshot_file)
            print('Finished successfully. Data written to: ' + file)
            break
        except Exception as e:
            print("Failed while fetching replies {}".format(e))
            break
