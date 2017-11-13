from requests_oauthlib import OAuth1Session
import tumblr_key
from datetime import datetime
import json
import csv

#Code below is drawn heavily from http://requests-oauthlib.readthedocs.io/en/latest/examples/tumblr.html and from 507 code: oauth1_twitter_caching.py


print('\n\n    *** NEW RUN ***\n')

key = tumblr_key.client_key # what Twitter calls Consumer Key
secret = tumblr_key.client_secret # What Twitter calls Consumer Secret
CACHE_FILE = "tumblr_cache.json"

# OAuth URLs given on the application page
request_token_url = 'http://www.tumblr.com/oauth/request_token'
authorization_base_url = 'http://www.tumblr.com/oauth/authorize'
access_token_url = 'http://www.tumblr.com/oauth/access_token'

now = datetime.now()

try:
    with open(CACHE_FILE, 'r') as cache_file:
        cache_json = cache_file.read()
        cache_diction = json.loads(cache_json)
except:
    cache_diction = {}


def check_cache(blogName, days):
    if blogName in cache_diction:
        cache_data = cache_diction[blogName]
        old_date = cache_data['date']
        if has_cache_expired(old_date, days) == False:
            data = cache_data
        else:
            data = None
    else:
        data = None
    return data


def has_cache_expired(old_date, days = 15):
    current = str(now.month)+str(now.day)
    delta = int(current) - int(old_date)
    if delta > int(days):
        result = True
    else:
        result = False
    return result


def token_request(blogName):
    tumblr = OAuth1Session(key, client_secret=secret, callback_uri='http://www.tumblr.com/dashboard')
    tumblr.fetch_request_token(request_token_url)

    # Link user to authorization page
    authorization_url = tumblr.authorization_url(authorization_base_url)
    print('Please go here and authorize:', authorization_url)

    # Get the verifier code from the URL
    redirect_response = input('\nPaste the full redirect URL here: ')
    tumblr.parse_authorization_response(redirect_response)

    # Fetch the access token
    tumblr.fetch_access_token(access_token_url)

    data = tumblr.get('https://api.tumblr.com/v2/blog/' + blogName + '.tumblr.com/info')
    cache_input(blogName, data)
    return


def cache_input(blogName, data):
    #print(data.text)
    data = json.loads(data.text)
    title = data['response']['blog']['title']
    posts = data['response']['blog']['total_posts']
    myData = {
    'title': title,
    'posts': posts
    }

    current = str(now.month)+str(now.day)
    cache_diction[blogName] = {
        'data': myData,
        'date': current
    }

    with open(blogName+'.csv', 'w') as c:
        writer = csv.writer(c)
        writer.writerow(str(cache_diction))

    with open(CACHE_FILE, 'w') as cache_file:
        cache_json = json.dumps(cache_diction)
        cache_file.write(cache_json)

    return



blogName = input('\nEnter the name of the Tumblr blog you would like to get posts from: ')
days = input('Enter the number of days needed since the previous search in order to conduct a new search: ')

if check_cache(blogName, days) == None:
    token_request(blogName)
else:
    print('The cache is up to date.')



# https://api.tumblr.com/v2/blog/peacecorps.tumblr.com/posts/text?
#api_key=fuiKNFp9vQFvjLNvx4sUwti4Yb5yGutBN4Xh10LXZhhRKjWlV4&notes_info=true
#https://api.tumblr.com/v2/blog/pitchersandpoets.tumblr.com/posts/photo?tag=new+york+yankees

# stockmarketeducation.tumblr.com

# chartsviewblog.tumblr.com
