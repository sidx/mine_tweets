First install all libraries and dependencies
    sudo easy_install pip
    sudo apt-get install python-dev libffi-dev libssl-dev
    pip install tweepy
    pip install tldextract

Log in to your twitter account and go to dev.twitter.com

Create app

Generate ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY and CONSUMER_KEY_SECRET

Add these values in marked locations in settings.py

Run "sudo python app.py"
