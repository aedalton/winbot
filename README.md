# winbot

A quick slackbot for the `#winning` channel. The Salesforce Bot Integration alerts the channel when an Opportunity has been won, but the team needs additional behavior to happen following this alert. Currently, this bot tries to find a user id based on the plaintext name sent in the alert. If found, the bot DMs a form link to the Owner of the Opportunity won.
