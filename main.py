import random
import time
from string import ascii_uppercase

import requests
from scapy.all import sniff, ARP
from twilio.rest import Client

from keys import DASH_BUTTON_MAC
from keys import JAKES_PHONE_NUMBER
from keys import MY_PHONE_NUMBER
from keys import TWILIO_ACCOUNT_SID
from keys import TWILIO_AUTH_TOKEN

url = 'http://www.nactem.ac.uk/software/acromine/dictionary.py'

the_textinator = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def convert_keys_to_string(dictionary):
    """
    Recursively converts dictionary keys to strings.
    Shamelessly borrowed from Stack Overflow.
    """
    if not isinstance(dictionary, dict):
        return dictionary
    return dict(
        (str(k), convert_keys_to_string(v)) for k, v in dictionary.items()
    )


def send_text(acr_info):
    acr_info = convert_keys_to_string(acr_info)
    message = (
        'ACRONYM FACTS: Did you know that '
        '"{}" most commonly means "{}" '
        'and has since {}?'.format(
            str(acr_info["acronym"]),
            str(acr_info["definition"]),
            str(acr_info["since"])
        )
    )

    print(message)
    the_textinator.messages.create(
        to=JAKES_PHONE_NUMBER,
        from_=MY_PHONE_NUMBER,
        body=message
    )


def generate_acronym():
    # randomly generated acronyms, hell yeah
    length = random.choice([2, 3, 4, 5])
    new_acronym = []
    for _ in range(length):
        new_acronym.append(random.choice(ascii_uppercase))

    return ''.join(new_acronym)


def get_meaning(acronym):
    # is this acronym real?
    result = requests.get(url, params={'sf': acronym})
    return result if result.json() else None


def parse_acr_definitions(acr):
    result = {
        'acronym': acr.json()[0]['sf'],
        'definition': acr.json()[0]['lfs'][0]['lf'],
        'since': acr.json()[0]['lfs'][0]['since']
    }
    return result


def process_acronym():
    # helper function to tie the process together
    while True:
        acr = generate_acronym()
        result = get_meaning(acr)
        # keep going until we generate a valid acronym
        if result:
            parsed_result = parse_acr_definitions(result)
            send_text(parsed_result)
            return
        else:
            time.sleep(1)


def arp_capture(pkt):
    if pkt[ARP].hwsrc == DASH_BUTTON_MAC:
        process_acronym()

if __name__ == '__main__':
    # monitor the network until we see the Dash button get pressed, then fire
    # arp_capture, which triggers the acronym generation and text
    print(sniff(prn=arp_capture, filter="arp", store=0, count=0))
