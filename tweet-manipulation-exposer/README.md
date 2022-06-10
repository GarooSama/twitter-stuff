# Summary
The script should be provided with Twitter & Imgur API keys in lines 16-25, and a tweet URL in line 46.
It will iterate through the replies of the tweet and match replies that contain specific keywords (blacklist.txt) OR the reply author has a high follower count.
Matched tweet details are saved into a generated CSV along with a screenshot link of it in case it gets deleted.
The use case of this script is very specific, and that is to expose tweet interaction manipulation in Saudi Twitter by user groups that reply to each other's ads.
# Limitation
There's no function provided by Twitter API to directly fetch replies for a tweet, so the script will search for all tweets replying to the tweet author and check if the reply is to the targer tweet, and will stop when it reached replies older than the targer tweet. So, it will run into an API rate limit if the tweet is old depending on the amount of the replies the author has gotten since the tweet.
