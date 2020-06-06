from igramscraper.instagram import Instagram
from time import sleep
from os import path
import datetime
import discord_webhook
import ast
import sys


FOLLOWER_LIMIT = 10000000
insta_username = 'teja.py'
insta_password = '3pCLqbjD8gcYW49znq'
username = 'teja.techraj'
MINS_TO_SLEEP = 55



def check_unfollowers(current,old):
	return list(set(old) - set(current))

def check_followers(current,old):
	return list(set(current) - set(old))


while True:
	try:
		print("iter")
		instagram = Instagram()
		instagram.with_credentials(insta_username, insta_password)
		instagram.login(force=False,two_step_verificator=True)
		sleep(2) # Delay to mimic user

		followers = []
		account = instagram.get_account(username)
		sleep(1)
		curr_time = datetime.datetime.now()
		curr_time = curr_time.strftime("%b %d, %Y - %H:%M:%S")
		followers = instagram.get_followers(account.identifier, FOLLOWER_LIMIT, 100, delayed=True) # Get 150 followers of 'kevin', 100 a time with random delay between requests
		# print(followers)

		current_followers = []

		for follower in followers['accounts']:
			current_followers.append(follower.username)

		del followers

		if not path.exists("follower_list.txt"):
			f = open("follower_list.txt","w")
			f.write(str(current_followers))
			f.close()
		else:
			f = open("follower_list.txt","r+")
			old_followers = f.read()
			f.close()
			old_followers = ast.literal_eval(old_followers)

			unfollowers = check_unfollowers(current_followers,old_followers)
			followers = check_followers(current_followers,old_followers)

			follower_change  = len(current_followers)-len(old_followers)

			follow_count = len(followers)
			unfollow_count = len(unfollowers)

			discord_webhook.send_msg(username,follower_change,followers,unfollowers,follow_count,unfollow_count,curr_time)

			f = open("follower_list.txt","w")
			f.write(str(current_followers))
			f.close()

		

	except KeyboardInterrupt:
		print("Exiting...")
		sys.exit(0)
	except Exception as e:
		print(e)
		
	sleep(MINS_TO_SLEEP*60)






