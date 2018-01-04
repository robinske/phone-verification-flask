## Setup

Clone this repo, then run the following:

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

Create an Authy Application and grab your API Key
https://www.twilio.com/console/authy/applications

```
mv config.py.sample config.py
```

And update the API key with your application key
Create a secret key for managing sessions

## Running

```python verify.py```

navigate to [localhost:5000/phone_verification](localhost:5000/phone_verification) to try it out!
