"""
Amazon lambda function to check indiegogo perk status
and send notifications based on availability
"""

import requests
import json

BASE_URL = 'https://api.indiegogo.com/2'
API_KEY = '' # indiegogo API key
CAMPAIGN = '' # indiegogo campaign id
INDIEGOGO_USER = '' # indiegogo user name
INDIEGOGO_PASSWORD = '' # indiegogo password
SLACK_WEBHOOK = '' # slack webhook url
SLACK_CHANNEL = '' # slack channel for messaging

def get_perks_info(token, campaign_id):
	""" query indiegogo for perk info and result all perks in json """
	payload = {'api_token': API_KEY,
	'access_token': token,
	}
	# spoof header since indiegogo seems to be blocking python requests user agent.
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	resp = requests.get(
		'{base}/campaigns/{ident}/perks.json'.format(base=BASE_URL,
			ident=campaign_id),
		params=payload,
		headers=headers)
	if not resp:
		print(resp.status_code)
		slack(str(resp.status_code) + " encountered attempting to fetch perks")
	result = json.loads(resp.text)
	return result['response']

def slack(message):
	""" use slack webhook to send arbitrary message to user/channel """
	result = requests.post(SLACK_WEBHOOK, json={"channel": SLACK_CHANNEL,
		"username": "checker", 
		"text": message, 
		"icon_emoji": ":coffee:"})
	print(result)


def authenticate(email, password):
	""" get an access token via indiegogo auth api """
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
	result = requests.post("https://auth.indiegogo.com/oauth/token", json={"grant_type":"password","credential_type":"email","email":email,"password":password})
	if not result:
		print(result.status_code)
		slack(str(result.status_code) + " encountered attempting to authenticate")
	return json.loads(result.text)["access_token"]

def lambda_handler(event, context):\
	""" amazon lambda entry point """
	try:
		token = authenticate(INDIEGOGO_USER, INDIEGOGO_PASSWORD)
		perks = get_perks_info(token, CAMPAIGN)
		for perk in perks:
			avail = perk["number_available"]
			claimed = perk["number_claimed"]
			stock = avail - claimed
			label = perk["label"]
			if stock > 0:
				message = f"{label} - {claimed}/{avail} - {stock} available!"
				print(message)
				slack(message)
			else:
				message = f"{label} - {claimed}/{avail} - no stock.."
				print(message)
	except Exception as e:
		slack(str(e))
		raise e