import settings
import stopwords

import tweepy
import datetime
import time
import tldextract
import logging
import operator



#To turn off the log reports
logging.basicConfig()
 



auth 	= tweepy.OAuthHandler(settings.OAUTH_KEYS['consumer_key'], settings.OAUTH_KEYS['consumer_secret'])
api 	= tweepy.API(auth)






def FindLatestId():
	dateToday	= format(datetime.datetime.utcnow(), '%Y-%m-%d')
	results = tweepy.Cursor(api.search,q=searchTerm, since=dateToday, lang = "en").items(1)
	for result in results:
		startId	= result.id
		return startId





def GenReport(results):
	#New Time
	timeFiveBefore	= datetime.datetime.utcnow() - datetime.timedelta(minutes = 5)
	
	name 			= []
	urls 			= []
	all_domains 	= []
	word_list 		= []
	filtered_words 	= []

	sinceId			= 0
	for result in results:

		#The latest tweets ID, for the next API call
		if (result.id > sinceId):
			sinceId = result.id

		#Finding screen names of all those who tweeted
		name.append(result.user.screen_name)

		#All expanded urls in all the tweets
		for url in result.entities['urls']:
			urls.append(url['expanded_url'])

		#All words form all tweets except the function words
		word_list 	= result.text.encode("utf-8").split(" ")
		for word in word_list:
			if (word.upper() not in stopwords.stopwords):
				filtered_words.append(word)

		#If the search term falls out of time constraint, quit fetching old tweets
		if result.created_at < timeFiveBefore:
			break



	print "######-------REPORTS-------######"


	#-----------------UNIQUE NAMES---------------------------------------
	print "\n----------UNIQUE NAMES----------"
	uniq_name	= list(set(name))
	for x in uniq_name:
		print "{0:15}-{1:10}" .format(x , name.count(x))




	#-----------------UNIQUE URLS(bonus 1)----------------------------------------
	print "\n----------UNIQUE URL COUNT----------"
	print "\nNo. of links = %d" %(len(urls))

	for x in urls:
		tldExt 	= tldextract.extract(x)
		url 	= '.'.join(tldExt[1:])
		all_domains.append(url)
		uniq_urls 		= list(set(all_domains))
	uniq_urls_count 	= {url: all_domains.count(url) for url in uniq_urls }
	sorted_uniqUrls 	= sorted(uniq_urls_count.items(), key = operator.itemgetter(1), reverse = True)
	print "\nSorted Unique Urls:"
	for url in sorted_uniqUrls:
		print "{0:20} - {1:3}".format(url[0],url[1])

		

	#-----------------UNIQUE WORDS(bonus 2)---------------------------------------
	print "\n----------UNIQUE WORDS COUNT----------"
	uniq_words 			= list(set(filtered_words))
	uniq_WordCount_dict = {word: filtered_words.count(word) for word in uniq_words}
	sorted_uniqWord 	= sorted(uniq_WordCount_dict.items(), key = operator.itemgetter(1), reverse = True)
	for i in range(0,10):
		print "{0:20} - {1:3}".format(sorted_uniqWord[i][0], sorted_uniqWord[i][1])
	#-----------------START 1 MINUTE REPORTS-----------------------------
	print "\nWaiting For 1 minute"
	#Wait for one minute
	time.sleep(60)


	


#------------------------------------------------------------------------
#INITIAL STEPS-----------------------------------------------------------
#------------------------------------------------------------------------
searchTerm 	= raw_input("Enter the Search Term: ")

while True:
	try:
		startId		= FindLatestId()
		results 	= tweepy.Cursor(api.search,q=searchTerm, max_id=startId, lang = "en", include_entities = True).items()
		GenReport(results)

	except(KeyboardInterrupt):
		#Graceful exiting!
		print "Exiting program"
		time.sleep(1)
		break