import ssl
import os
import json
from pathlib import Path
from flask import Flask, request, Response
import slack
from dotenv import load_dotenv
import certifi
import shlex
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
@app.route('/acro-help', methods=['POST'])
def acro_help():
    data = request.form
    channel_id = data.get('channel_name')
    help_text = {
        'channel': data.get('user_id'),
        'blocks': [{
            'type': 'section',
            'text': {
                'type': "mrkdwn",
                'text': (
                    'How to use:\n\n'
                )
            }
        },
            {'type': 'divider'},
            {'type': 'section',
            'text': {
                'type': "mrkdwn",
                'text': (
                    '*/acro <acronym>*:\n\tTo view definition of <acronym>\n\n'
                    '*/acro-add <acronym><meaning>*\n\t to add definition in quotes\n\n'
                    '*/acro-del <acronym>*\n\t to remove definition also multiple\n\n'
                    '*/acro ChatGPT <acronym>*\n\t would one day link to ChatGPT'
                )
            }
            }
        ]
    }
    client.chat_postMessage(**help_text)
    return Response(), 200



@app.route('/acro', methods=['POST'])
def acro():
    data = request.form
    user_id = data.get('user_id')
    param = data.get('text')
    split_param = shlex.split(param)
    with open("./dict.json", "r") as jsonFile:
        data = json.load(jsonFile)
    for term in split_param:
        if term in data:
            client.chat_postMessage(channel=user_id, text=f"{term}: {data[term]}")
        else:
            client.chat_postMessage(channel=user_id, text=f"Could not find {term} in dictionary. Use /acro-add to add it to the dictionary.")
    return Response(), 200


@app.route('/acro-add', methods=['POST'])
def acro_add():
    data = request.form
    user_id = data.get('user_id')
    param = data.get('text')
    split_param = shlex.split(param)

    with open("./dict.json", "r") as jsonFile:
        data = json.load(jsonFile)
    data[split_param[0]] = split_param[1]
    with open("./dict.json", "w") as jsonFile:
        json.dump(data, jsonFile)

    client.chat_postMessage(channel=user_id, text=f"{split_param[0]} added")
    return Response(), 200

@app.route('/acro-del', methods=['POST'])
def acro_del():
    data = request.form
    user_id = data.get('user_id')
    param = data.get('text')
    split_param = shlex.split(param)

    with open("./dict.json", "r") as jsonFile:
        data = json.load(jsonFile)

    for term in split_param:
        if term in data:
            del data[term]
            with open("./dict.json", "w") as jsonFile:
                json.dump(data, jsonFile)
            client.chat_postMessage(channel=user_id, text=f"{term} deleted")
        else:
            client.chat_postMessage(channel=user_id, text=f"{term} does not exist in dictionary")

    return Response(), 200

#runs app on default port if we want to change the port app.run(debug=True, port=portnum)
if __name__ == "__main__":
    app.run(debug=True, port=5005)
