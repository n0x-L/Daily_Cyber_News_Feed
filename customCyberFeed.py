""" 
Author: Amanda Leeson - Nov 2020
Project originally forked from: https://github.com/kotartemiy/pygooglenews

A custom cyber security news feed.

Default accepted topics are: 
world, nation, business, technology, entertainment
science, sports, health 
 
"""

from pygooglenews import GoogleNews
import smtplib

from datetime import datetime
from pytz import timezone

from email.mime.text import MIMEText

# Initiate Google News class to get access to all functions
gn = GoogleNews(lang = 'en', country = 'CA')

# For time conversion crap
mountain = timezone('America/Edmonton')
gmt = timezone('GMT')

# Initialize other vars
email_message = ''

# Some helpful functions
def print_titles(results):
	for x in results['entries']:
			print('\n' + x['title'])
	print('\n')

def print_published(results, email_message):
	# Used to help sort the results by date-time
	results_dict = {}

	# If we found at least 1 search result process the data
	if int(len(results['entries'])) > 0:
		email_message += 'Total results: ' + str(len(results['entries'])) + '\n'
		email_message += '-------------------------\n'

		# Iterate through the results
		for x in results['entries']:
			# Need to do GMT time conversions, moan.
			published = x['published']
			date_object = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z")

			loc_dt = gmt.localize(date_object)
			loc_dt = loc_dt.astimezone(mountain)
			published = loc_dt.strftime("%a, %d %b %Y %H:%M:%S")

			# Get the current result for title and link
			tmp_dict_entry = {'published' : published, 'title' : x['title'], 'link' : x['link']}

			# Append to dict by date/time object
			results_dict[date_object] = tmp_dict_entry	
		
	else:
		email_message += 'No results found\n'

	sorted_results = dict(sorted(results_dict.items()))
	
	# Create the email message sorted by earliest datetime to most recent
	for result in sorted_results.values():
        # Append results to email message
		email_message += '\n' + result['published'] + ' ' + result['title'] + ' ' + result['link'] + '\n'

	return email_message

# TODO: Need a more secure way of doing this. 
# Also noticed my Gmail app doesn't actually
# notify me when the email comes in.
def send_email(email_message):
	# connect with Google server
	smtp_ssl_host = 'smtp.gmail.com'
	smtp_ssl_port = 465
	# use username or email to log in
	username = '' # To be filled in
	password = '' # To be filled in

	from_addr = '' # To be filled in
	to_addrs = [''] # To be filled in

	# Email lib has diff templates
	# here use MIMEText to send only text
	message = MIMEText(email_message)
	currentDatetime = str(datetime.now())
	subject = currentDatetime + ' - Daily Cyber Security News Update'
	message['subject'] = subject
	message['from'] = from_addr
	message['to'] = ', '.join(to_addrs)

	# Connect using SSL
	server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)

	# Log in and send the message
	server.login(username, password)
	server.sendmail(from_addr, to_addrs, message.as_string())
	server.quit()

# Create the headlines, perform the search, and call the print_published
# function to parse the search results
headline_title = '\n####### Hacker Headline News #######\n'
hacking = gn.search('allintitle:cyber attack', when = '24h')
email_message += print_published(hacking, headline_title)

cves_title = '\n####### Tenable Top CVEs #######\n'
cves = gn.search('site:tenable.com intitle:critical intitle:cve', when = '30d')
email_message += print_published(cves, cves_title)

zero_day_title = '\n####### Zer0-Days #######\n'
zero_days = gn.search('intitle:zero-day + disclose + reveal', when = '24h')
email_message += print_published(zero_days, zero_day_title)

data_breaches_title = '\n####### Data Breaches #######\n'
data_breaches = gn.search('allintitle:data breach', when = '24h')
email_message += print_published(data_breaches, data_breaches_title)

ransomware_title = '\n####### Ransomware Attacks #######\n'
ransomware_attacks = gn.search('allintitle:ransomware attack', when = '24h')
email_message += print_published(ransomware_attacks, ransomware_title)

malware_title = '\n####### New Malware #######\n'
new_malware = gn.search('allintitle:new malware', when = '24h')
email_message += print_published(new_malware, malware_title)

ryuk_title = '\n#### Ryuk ###\n'
ryuk_update = gn.search('allintitle:ryuk attack', when = '24h')
email_message += print_published(ryuk_update, ryuk_title)

emotet_title = '\n#### Emotet ###\n'
emotet_update = gn.search('allintitle:emotet attack', when = '24h')
email_message += print_published(emotet_update, emotet_title)

ic_title = '\n####### instantcoffee #######\n'
instantcoffee = gn.search('intitle:instantcoffee', when = '24h')
email_message += print_published(instantcoffee, ic_title)

world_news_title = '\n####### Breaking News #######\n'
world_news = gn.search('breaking news -sports -thestreetjournal', when = '8h')
email_message += print_published(world_news, world_news_title)

# Print the message to be sent
#print(email_message)

# Send the email
send_email(email_message)

