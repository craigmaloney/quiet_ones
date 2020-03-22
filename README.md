# Quiet Ones

This script figures out which folks haven't posted or have only posted a few times on Slack.

## Permissions
This application requires the following permissions on Slack:

* channels:history
* channels:join
* channels:read
* users.profile:read
* users:read
* users:read.email

## Installation

* Create a virtual environment (`python3 -m venv venv && source venv/bin/activate` or equivalent)
* `pip install -r requirements.txt`
* Add the OAuth key to your environment:
    * in `bash`: `export SLACK_API_TOKEN=xoxb-abc-123...`
* Edit the `main.py` file to configure the `THRESHOLD` for how many messages a user should post to be considered not quiet (users under this threshold will be printed)
* Type `python main.py` to run the script. If everything is set up properly you should see users that have posted the `THRESHOLD` number of posts or less.

(This script based on previous work by [https://gist.github.com/demmer/617afb2575c445ba25afc432eb37583b](https://gist.github.com/demmer/617afb2575c445ba25afc432eb37583b))
