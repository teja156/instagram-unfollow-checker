from igramscraper.instagram import Instagram
from time import sleep
import os
from os import path
import datetime
import discord_webhook
import ast
import sys
from pytz import timezone

FOLLOWER_LIMIT = 10**6

#Your instagram bot account username
insta_username = ''

#Your instagram bot account password
insta_password = ''

#Username of the real instagram account which you want to monitor
username = ''

#Change this at your own risk
MINS_TO_SLEEP = 40

discord_webhook_url = ''


def check_unfollowers(current,old):
	return list(set(old) - set(current))

def check_followers(current,old):
	return list(set(current) - set(old))


def start():
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
			curr_time = datetime.datetime.now(timezone('Asia/Kolkata'))
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

				discord_webhook.send_msg(username,follower_change,followers,unfollowers,follow_count,unfollow_count,curr_time,discord_webhook_url)

				f = open("follower_list.txt","w")
				f.write(str(current_followers))
				f.close()

			

		except KeyboardInterrupt:
			print("Exiting...")
			sys.exit(0)
		except Exception as e:
			print(e)

		sleep(MINS_TO_SLEEP*60)


if __name__ == '__main__':
	if not os.path.exists('config_file.txt'):
		print("You have not configured your details yet.\nRun config.py first")
		sys.exit(0)

	f = open('config_file.txt','r')
	config = f.read()
	f.close()
	config = ast.literal_eval(config)
	insta_username = config['insta_username']
	insta_password = config['insta_password']
	username = config['username']
	discord_webhook_url = config['discord_webhook_url']

	start()








