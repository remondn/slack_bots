import os
import time
import _thread
import re
from slackclient import SlackClient


# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_commands(slack_events, bot_id):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == bot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel, slack_client, bot_id):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    if command.startswith("who are you ?"):
        response = bot_id

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )

def main_loop(slack_client):
    if slack_client.rtm_connect(with_team_state=False):
        print("Bot connected to {} and running!".format(slack_client))
        # Read bot's user ID by calling Web API method `auth.test`
        bot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read(), 
                bot_id)
            if command:
                handle_command(command, channel, slack_client, bot_id)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection to {} failed. Exception traceback printed above." \
            .format(slack_client))

if __name__ == "__main__":
    # Get workspaces auth 
    workspaces = os.environ.get('SLACK_BOT_TOKEN').split(',')

    # instantiate Slack client for each workspace
    slack_clients = []
    for ws in workspaces:
        if ws == workspaces[-1]:
            # If it's the last workspace to start a thread, start the main one
            main_loop(SlackClient(ws))
        else:
            thread.start_new_thread( main_loop, (SlackClient(ws)) )
