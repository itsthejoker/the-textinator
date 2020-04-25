import random
import threading
import time
from string import ascii_uppercase

import requests
from keys import (
    DASH_BUTTON_MAC,
    MY_PHONE_NUMBER,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)
from keys import (
    MICHELLE,
    ME,
    ZACK,
    LILY
)
from leds import larson, rainbow, blink_message
from scapy.all import sniff, ARP
from twilio.rest import Client

all_phones = [ME, MICHELLE, ZACK, LILY]

url = 'http://www.nactem.ac.uk/software/acromine/dictionary.py'

the_textinator = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

stop_thread = False


def send_text(acr_info):
    message = (
        'ACRONYM FACTS: Did you know that "{}" in medicine most commonly means'
        ' "{}" and was first seen in {}?'.format(
            str(acr_info["acronym"]),
            str(acr_info["definition"]),
            str(acr_info["since"])
        )
    )

    stop_thread = False
    thread1 = threading.Thread(target=rainbow, args=(lambda: stop_thread,))
    thread1.start()

    message_failure = False

    for phone in all_phones:
        try:
            the_textinator.messages.create(
                to=phone,
                from_=MY_PHONE_NUMBER,
                body=message
            )
        except Exception as e:
            message_failure = True
            print("ERROR: {e}")
            pass

    print("Fact sent: '{}'".format(message))

    stop_thread = True
    thread1.join()  # stop the animation

    if message_failure:
        blink_message(success=False)
    else:
        blink_message(success=True)


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


def get_acronym_information():
    stop_thread = False
    thread1 = threading.Thread(target=larson, args=(lambda: stop_thread,))
    thread1.start()

    while True:
        acr = generate_acronym()
        result = get_meaning(acr)
        if result:
            stop_thread = True
            thread1.join()  # stop the animation
            return result
        else:
            time.sleep(1)


def arp_capture(pkt):
    if pkt[ARP].hwsrc == DASH_BUTTON_MAC:
        result = get_acronym_information()
        parsed_result = parse_acr_definitions(result)
        send_text(parsed_result)


if __name__ == '__main__':
    blink_message(success=True)
    # monitor the network until we see the Dash button get pressed, then fire
    # arp_capture, which triggers the acronym generation and text
    print(sniff(prn=arp_capture, filter="arp", store=0, count=0))
