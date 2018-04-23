import os
import time
import threading
import re
import queue
from slackclient import SlackClient


# constants
BREAK_TIME = 0.5
THREAD_NB = 4
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

def parse_bot_cmd(slack_events):
    """

        Parses a list of events coming from the Slack RTM API. If there is a 
        message, this function returns a tuple of message and channel.
        If its not found, then this function returns None, None.

        Args:
            slack_events: Content of the read channel

        Return:
            tuple: (Message content, channel)

    """
    for event in slack_events:
        if event["type"] == "message":
            return event["text"], event["channel"]
    return None, None

def handle_msg(msg, channel, slack_client, bot_id):
    """
        
        Depending on the bot_id, redirect the message received to the right
        method.

        Args:
            msg (string): Message sent by the user
            channel (string): Name of the channel where the message have been 
                              sent
            slack_client: Slack client
            bot_id (string): Bot ID 

        TODO
    """
    # # Default response is help text for the user
    # default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

    # # Finds and executes the given command, filling in response
    # response = None
    # # This is where you start to implement more commands!
    # if command.startswith(EXAMPLE_COMMAND):
    #     response = "Sure...write some more code then I can do that!"
    # if command.startswith("who are you ?"):
    #     response = bot_id

    response = "WHAT ? I'M NOT WORKING!"
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response
    )


def welcomer(q):
    """

    Welcomer : Treat all incomming requests from clients, and put it into the 
    queue, to be treated by worker. If no requests have been made in the last 
    loop, the thread go to sleep for 0.5 sec.

    Args :
        q (Queue) : Shared queue with the welcomer thread. Request are put
                        here.
    
    """
    # Get the workspaces to listen to
    workspaces = os.environ.get('SLACK_BOT_TOKEN').split(',')

    clients = {}
    connections = {}

    while True:
        client = False

        for ws in workspaces:
            # Initialization part
            if clients[ws] == None:
                clients[ws] = SlackClient(ws) 
            if connections[ws] == None:
                connections[ws] = clients[ws].rtm_connect(with_team_state=False)

            # Treatment
            if connections[ws]:
                # For user
                print("Bot connected to {} and running!".format(clients[ws]))

                # Get bot's ID with API
                bot_id = clients[ws].api_call("auth.test")["user_id"]

                # Get command if any
                msg, channel = parse_bot_cmd(clients[ws].rtm_read())

                if msg:
                    # If there is a command, put it into the queue !
                    request = [msg, channel, clients[ws], bot_id]
                    q.put(request)

                    # And remember that we treated a client
                    client = True
            else:
                print("Connection to {} failed.".format(clients[ws]))
        
        if not client:
            time.sleep(BREAK_TIME)
            



def worker(q):
    """

    Worker : look into the queue, and treat the request if there is any.

    Args :
        q (Queue) : Shared queue with the welcomer thread. Request are put
                        here.
    
    """
    while True:
        # Never stop to look into the queue and treat what's there
        msg, channel, client, bot_id = q.get()
        handle_msg(msg, channel, client, bot_id)
    


def main():
    """

    Main of the server. This main start workers threads and start the welcomer.

    """
    q = queue.Queue()
    t = []
    for i in range(THREAD_NB):
        t.append(threading.Thread(target=worker, args=(q,)))
    
    worker(q)

if __name__ == "__main__":
    main()
