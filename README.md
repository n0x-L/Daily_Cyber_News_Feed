# Daily_Cyber_News_Feed
This simple Python script is set up with custom search queries to grab data on recent cyber-related events and attacks. It uses the kotartemiy/pygooglenews repository and a simple Gmail SMTP function to query the data and to send an email after the data has been parsed and formatted.

For the data formatting I created functionality to convert the GMT time to Mountain time, feel free to change this timezone variable at the top of the script to match your own. Might add command-line arguments to set this (or choose not to set it at all in case you want GMT time) in the future.

I've also formatted the data to show the most recent updates at the bottom of the list so that the updates read in ascending order of time published, and to include the related link in case you want to explore an article further.

Personally I set up a crontab job in order to automatically get the email every morning:
https://www.jcchouinard.com/python-automation-with-cron-on-mac/

In the future I'd like to implement a more secure way of setting up the email function and for storing credentials. For now you'll likely have to turn off the setting for blocking insecure apps in your Gmail app so that you can send an email from your script (even though its using SSL).
To mitigate the risk I created a Gmail account for this specific purpose so as not to open a primary email account to the risk.

I plan on updating the search queries as I find more relevant or interesting content to be notified on!

It also includes a "breaking news" section at the very end that you can get rid of if you're only looking for cyber content.

Cheers-
