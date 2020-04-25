# The Textinator

There are few things that are truly as fun on this earth as sending stupid things to your friends. This entire project exists to send stupid things to my best friends, Jake and Michelle B.

Triggered by your standard everyday [Amazon Dash button](www.amazon.com/Dash-Buttons/b?ie=UTF8&node=10667898011), this script generates random acronyms and then runs them through [Acromine](http://www.nactem.ac.uk/software/acromine/), a service provided by the National Centre for Text Mining that contains every acronym in [MEDLINE](https://en.wikipedia.org/wiki/MEDLINE) databases (compiled by the United States Library of Medicine). Once a valid acronym is generated, the most common usage of that acronym is then formatted into a text message and sent to the target phone number via [Twilio](https://www.twilio.com).

Now updated to require the [Pimoroni Blinkt!](https://shop.pimoroni.com/products/blinkt) -- blinky status lights update based on what's happening!

I originally wrote this in 2017 and deployed it for my friend Jake. Now it's three years later and we're in the middle of a global pandemic. His wife, Michelle, is stuck at home... so it's time to revisit the TEXTINATOR.

### Process:

- Press Amazon Dash Button
- MAC address of the button is pulled from the initial request to start the process
- Repeat until a valid acronym is found:
  - Generate a random acronym between 2 and 5 characters long
  - Send acronym to Acromine to see if it's valid
  - if it is valid, continue
  - if it is not valid, wait a second to respect the API and try again with a new acronym
- Pull the most common meaning from the results
- format it into the string "ACRONYM FACTS: Did you know that "{}" in medicine most commonly means "{}" and was first seen in {}?"
- send as text message to ~~Jake~~ Michelle

### Installation

Clone the repo to a raspberry pi with the blinkt connected. Requires Python3.8. Doublecheck the following files to make sure that there aren't any changes needed (in things like the path or whatnot).

```bash
cd the-textinator
virtualenv .venv
poetry install
sudo cp textinator.service /etc/systemd/system/textinator.service
sudo systemctl enable textinator.service
```

# FAQ

_Why?_ Why not?

_But Joe, aren't you afraid he'll find this?_ Well, that's why I'm putting it online. The point isn't to annoy him to the point of vexation; the point is to have a little fun and maybe make him say "What the hell is this?" a few times. Besides, his wife is in on it and has been since the beginning.

If he finds this, then that just means he was curious enough to look for it, and I'm okay with that!

_You know this is dumb, right?_ Yeah, totally. That's the point.

## Other

The system is currently running on a Raspberry Pi 3 in my office, and the Dash button is for buying Play-Doh. This is 100% worth the cost.


Edit: It's his anniversary today, and I decided to bring it to a close by texting him something in the same format as the automated texts. It went over very well, and all is good. Another project complete :)
