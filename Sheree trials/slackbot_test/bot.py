import ssl
import os
from pathlib import Path
from flask import Flask, request, Response
import slack
from dotenv import load_dotenv
import certifi
#event handler
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
app = Flask(__name__) #configures flask app
slack_event_adapter = SlackEventAdapter(os.environ['SLACK_SIGNING_SECRET'],'/slack/events',app)
#need more research into SSL
ssl_context = ssl.create_default_context(cafile=certifi.where())
client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context) 
#below gets us the user id of api
BOT_ID = client.api_call("auth.test")['user_id']
#recognises the message event
@slack_event_adapter.on('message')
#payload is the data on message that was sent


def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    found = False

    if BOT_ID != user_id:
        #if the acronym is found in text found = True




    
    
        if text == "BUTTONS":
            message_to_send = {"channel": channel_id, "blocks": [
            {
                "type": "section",
                "text": {
                        "type": "plain_text",
                        "text": "Block has been triggered.",
                        "emoji": True
                        }
                },
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "OK",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				}
			]
		}
	]
}
            client.chat_postMessage(**message_to_send)
        if " JS " in text or text == "JS":
            meaning = "JavaScript: JavaScript is a high-level programming language used for both client-side and server-side web development. "
            found = True
        elif "API" in text:
            meaning = "An Application Programming Interface (API) is a set of protocols, routines, and tools for building software applications."
            found = True
    if found == True:
        client.chat_postMessage(channel=channel_id, text=meaning)
#adds new endpoint
#if we want multiple methods is comma seperated
@app.route('/acro-add', methods=['POST'])

#200 us okay 404 but a positive

def acro_add():
    data = request.form
    channel_id = data.get('channel_name')
    client.chat_postMessage(channel=channel_id, text="Will one day add to our dictionary")
    return Response(), 200

#runs app on default port if we want to change the port app.run(debug=True, port=portnum)
if __name__ == "__main__":
    app.run(debug=True)
    