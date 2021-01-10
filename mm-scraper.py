import smtplib
import praw
import time
import os
from termcolor import colored
from dotenv import load_dotenv

# load .env vars
load_dotenv()

# SMS Details
FROM_ADDRESS = os.getenv('SMS_FROM_ADDRESS')
TO_ADDRESS = os.getenv('SMS_TO_ADDRESS')

# Reddit search terms case insensitive
SEARCH_STRINGS = ['Metropolis','Botanical', 'Latrialum','Firefly', 'Rudy', 'Zilents']

# Create reddit connection
reddit = praw.Reddit(client_id = os.getenv('REDDIT_CLIENT_ID'),
                     client_secret = os.getenv('REDDIT_CLIENT_SECRET'),
                     user_agent = os.getenv('REDDIT_USER_AGENT'))

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(os.getenv('MAIL_ADDRESS'), os.getenv('MAIL_PASSWORD'))

# Start streaming posts from subreddit
print('Starting Stream')
print('\n----------------------------\n')

# for submission in reddit.subreddit('mechmarket').stream.submissions(skip_existing=True):
for submission in reddit.subreddit('mechmarket').stream.submissions(skip_existing=False):
    # getting necessary details
    post_flair = submission.link_flair_text
    post_title = submission.title 
    post_content = submission.selftext
    post_url = submission.url
    post_author = submission.author
    current_time = time.strftime('%I:%M', time.localtime())

    # removeddit link and author link
    removeddit_url = post_url.replace('reddit', 'removeddit')
    author_url = 'https://www.reddit.com/user/' + str(post_author)

    # lowering all strings for use
    strings_lower = strings_lower = [string.lower() for string in SEARCH_STRINGS]

    # If a new post matches any search term in the title
    match = [term for term in strings_lower if term in post_title.lower().partition('[w]')[0]]
    if any(match):
        # display in console as green
        message_url = 'https://www.reddit.com/message/compose/?to=' + str(post_author) + '&subject=' + match[0] + '&message=' + 'Hey, ill buy ' + match[0] + '. Paypal is ' + os.getenv('PAYPAL_EMAIL')
        print(colored(post_flair, 'green'))
        print(colored(current_time, 'green'))
        print(colored(post_title, 'green'))
        print(colored(post_url, 'green'))
        print(colored(message_url,'green'))
        print(colored(removeddit_url, 'green'))
        print(colored(post_author, 'green'))
        print(colored(author_url, 'green'))
        print('\n----------------------------\n')

        # Construct message and send SMS
        message = ('From: %s\r\n' % FROM_ADDRESS
                  + 'To: %s\r\n' % TO_ADDRESS
                  + 'Subject: %s\r\n' % 'New Post Matching Search'
                  + '\r\n\n\n'
                  + '%s\r\n' % post_flair
                  + '%s\r\n' % post_title
                  + '\n%s\r\n' % post_url
                  + '\n%s\r\n' % message_url)
        try:
            server.sendmail(FROM_ADDRESS, TO_ADDRESS, message)
        except Exception as e:
            print('Failed to send message')
            print(e)

    else:
        # Display as default color
        print(post_flair)
        print(current_time)
        print(post_title)
        # print(post_url)
        print(removeddit_url)
        print(post_author)
        print('\n----------------------------\n')