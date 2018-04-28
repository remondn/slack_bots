import re

MENTION_REGEX = "(.*)<@(|[WU].+?)>(.*)"

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
    print(matches)

    if not matches:
        return [None, None]

    match = matches[0]

    if match[2] is "do":
        return ["You can do it !", channel]
    elif match[0].upper() is "HEY":
        return ["Hey !", channel]        
    else:
        return ["Sorry, I'm a beginner, I know only one command : do", channel]


