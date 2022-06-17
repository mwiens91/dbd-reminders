[![Python version](https://img.shields.io/badge/python-3.9-blue.svg)](https://github.com/mwiens91/dbd-reminders)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# dbd-reminders

This app ships useful email reminders to [Dead by
Daylight](https://store.steampowered.com/app/381210/Dead_by_Daylight/)
players. It has two components: one is to email you when perks that you
care about are available in the [Shrine of
Secrets](https://deadbydaylight.fandom.com/wiki/Shrine_of_Secrets); the
other is to email you when new codes are available for free bloodpoints
or charms (these codes are pulled from the
[@DBDcodeReminder](https://twitter.com/DBDcodeReminder) Twitter
account).

This is written for Linux/Unix systems. I recommend running it every
24 hours on a cron job or having a script run it every 24 hours on
something like [PythonAnywhere](https://www.pythonanywhere.com). This
app remembers what codes or perks it has already notified about, so
there's no need to worry about spam messages.

If you want to get emails from this notifier but don't want to set
everything up, send me an email and I might be able to help you out.

## Installation

Just install the requirements with `pip`:

```
pip install -r requirements.txt
```

## Configuration

Configuration files something look like the following:

```yaml
# Twitter dev platform token
twitter-api-key: "p0gch4mp101fy451do9uod1s1x9i4a"
twitter-api-key-secret: "itqb0thqi5cek18ae6ekm7pbqvh63k"

# Gmail login info
gmail-email: "username@gmail.com"
gmail-app-password: "hunter2"

# Users: for the perk names consult
# https://deadbydaylight.fandom.com/wiki/Perks
users:
  - email: user1@email.com
    notify-about-codes: true
    perks-to-notify-about:
      - "Mettle of Man"
      - "Hex: Blood Favour"
  - email: user2@email.com
    notify-about-codes: false
    perks-to-notify-about:
      - "Barbecue & Chilli"
```

You need to set up a Twitter developer account to get a Twitter API key
and secret. This is simple to do. You also need to set up a Gmail
account from which to send emails. Note that you must use an "App
Password" in the above config file for this to work; using an ordinary
login password will not work.

For the `users` part of the above config, each user needs an email, a
flag to specify whether they care about receiving emails about codes,
and a list for what perks they want to be emailed about. Note that the
perk names should correspond to the names listed on [this wiki
page](https://deadbydaylight.fandom.com/wiki/Perks).

### Setting up a configuration file

dbd-reminders looks for a configuration file at the root of the
repository. Simply copy the example config file
[`config.yaml.example`](config.yaml.example) to `config.yaml` at the
root of the repository and fill out the details.

## Usage

Run dbd-reminders directly with
[run_dbdreminders.py](run_dbdreminders.py):

```
./run_dbdreminders.py
```
