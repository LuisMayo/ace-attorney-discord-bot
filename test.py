import re

if __name__ == "__main__":
    emoji = "bonjour <:issou:501044386746990596>"
    if(re.search("<:\w{2,32}:\d{18}>", emoji)):
        print("true")
    else:
        print("false")
    print(emoji)
    emoji = re.sub(r'<:\w{2,32}:\d{18}>', '(emoji)', emoji)
    print(emoji)
