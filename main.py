import random
from scapy.all import sniff, ARP
from string import ascii_uppercase
import requests
from twilio.rest import Client
from keys import TWILIO_ACCOUNT_SID
from keys import TWILIO_AUTH_TOKEN
from keys import MY_PHONE_NUMBER
from keys import JAKES_PHONE_NUMBER
from keys import DASH_BUTTON_MAC

url = 'http://www.nactem.ac.uk/software/acromine/dictionary.py'

# the_textinator = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_text(acr_info):
    message = (
        'ACRONYM FACTS: Did you know that '
        '"{}" most commonly means "{}" '
        'and has since {}?'.format(
            acr_info["acronym"],
            acr_info["definition"],
            acr_info["since"]
        )
    )

    print(message)
    # the_textinator.messages.create(
    #     to=JAKES_PHONE_NUMBER,
    #     from_=MY_PHONE_NUMBER,
    #     body=message
    # )


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


def arp_capture(pkt):
    if pkt[ARP].hwsrc == DASH_BUTTON_MAC:
        process_acronym()

if __name__ == '__main__':
    print(sniff(prn=arp_capture, filter="arp", store=0, count=0))
