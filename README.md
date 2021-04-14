simple script to query indiegogo to check perk status and notify via slack webhook.

This script is designed to run as a AWS lambda function.

# Required configurations

```
API_KEY = '' # indiegogo API key
CAMPAIGN = '' # indiegogo campaign id
INDIEGOGO_USER = '' # indiegogo user name
INDIEGOGO_PASSWORD = '' # indiegogo password
SLACK_WEBHOOK = '' # slack webhook url
SLACK_CHANNEL = '' # slack channel for messaging
```
