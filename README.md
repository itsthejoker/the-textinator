# The Textinator

There are few things that are truly as fun on this earth as sending stupid things to your friends. This entire project exists to send stupid things to my best friend, Jake B.

Triggered by your standard everyday [Amazon Dash button](www.amazon.com/Dash-Buttons/b?ie=UTF8&node=10667898011), this script generates random acronyms and then runs them through [Acromine](http://www.nactem.ac.uk/software/acromine/), a service provided by the National Centre for Text Mining that contains every acronym in [MEDLINE](https://en.wikipedia.org/wiki/MEDLINE) databases (compiled by the United States Library of Medicine). Once a valid acronym is generated, the most common usage of that acronym is then formatted into a text message and sent to the target phone number via [Twilio](https://www.twilio.com).

###Process:

- Press Amazon Dash Button
- MAC address of the button is pulled from the initial request to start the process
- Repeat until a valid acronym is found:
  - Generate a random acronym between 2 and 5 characters long
  - Send acronym to Acromine to see if it's valid
  - if it is valid, continue
  - if it is not valid, wait a second to respect the API and try again with a new acronym
- Pull the most common meaning from the results
- format it into the string "ACRONYM FACTS: Did you know that "{}" most commonly means "{}" and has since {}?"
- send as text message to Jake

# FAQ

_Why?_ Why not?

_But Joe, aren't you afraid he'll find this?_ Well, that's why I'm putting it online. The point isn't to annoy him to the point of vexation; the point is to have a little fun and maybe make him say "What the hell is this?" a few times. Besides, his wife is in on it and has been since the beginning.

If he finds this, then that just means he was curious enough to look for it, and I'm okay with that!

_You know this is dumb, right?_ Yeah, totally. That's the point.

## Other

I'll update this if / when he figures it out.
