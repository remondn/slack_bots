import re

MENTION_REGEX = "(.*)<@(.+?)>(.*)"

def handle_msg(msg, channel):
    """
        
        Main method for handling the message for Starter bot

        Args:
            msg (string): Message sent by the user
            channel (string): Name of the channel where the message have been 
                              sent

        Return:
            message (string): Message the bot need to send
            channel (string): Name of the channel where the message needs to be sent

    """
    print("In the handle message of Starter Bot")
    matches = re.compile(MENTION_REGEX).findall(msg)
    print("msg = {}, channel = {}, regex = {}".format(msg, channel, matches))

    if not matches:
        return [None, None]

    match = matches[0]
    print("MATCH = |{}|{}|".format(match[0].upper().strip(), match[2].strip()))
    print("bool = {}".format(match[2].strip() is "do"))

    if match[2].strip() is "do":
        return ["You can do it !", channel]
    elif match[0].upper().strip() is "HEY":
        return ["Hey !", channel]        
    else:
        return ["Sorry, I'm a beginner, I know only one command : do", channel]


