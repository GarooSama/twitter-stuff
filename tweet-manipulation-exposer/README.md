# Summary
The script should be provided with Twitter & Imgur API keys in lines 16-25.
It will iterate through the replies of the tweet and match replies that contain specific keywords (blacklist.txt) OR the reply author has a high follower count.
Matched tweet details are saved into a generated CSV along with a screenshot link of it in case it gets deleted.
The use case of this script is very specific, and that is to expose tweet interaction manipulation in Saudi Twitter by user groups that reply to each other's ads.
# Usage
```powershell
> python exposer.py
```
# Limitation
There's no function provided by Twitter API to directly fetch replies to a tweet, so the script will search for ALL tweets replying to the tweet author and check if the reply is to the target tweet, and will stop when it encounters replies older than the target tweet. So, it will eventually run into an API rate limit if the tweet is old depending on the amount of all replies the author (including replies to other tweets) has gotten since the tweet.
