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
#adds new endpoint


#200 us okay 404 but a positive
@app.route('/acro', methods=['POST'])
def acro():
    data = request.form
    channel_id = data.get('channel_name')
    client.chat_postMessage(channel=channel_id, text="/acro <acronym> to view definition\n/acro add <acronym><meaning> to add definition\n/acro delete <acronym> to remove definition\n/acro ChatGPT <acronym> would one day link to ChatGPT")
    return Response(), 200


@app.route('/acro-add', methods=['POST'])
def acro_add():
    data = request.form
    channel_id = data.get('channel_name')
    client.chat_postMessage(channel=channel_id, text="Will one day add to our dictionary")
    return Response(), 200

#runs app on default port if we want to change the port app.run(debug=True, port=portnum)
if __name__ == "__main__":
    app.run(debug=True)
    