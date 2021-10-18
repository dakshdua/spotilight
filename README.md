# Spotilight

## What is it?
Spotilight is a small Python program that gets the dominant color from the currently playing Spotify song's album art and sets smart light bulbs to that color. It is currently set up to work with TPLink Kasa Smart Bulbs.

## Setup
First, set up your bulbs by following the default instructions that they arrived with.
Then, install the requirements for Spotilight by running `pip install -r requirements.txt`
Next make a .env file or set environment variables for the system that match:
```shell
SPOTIPY_CLIENT_ID='your-client-id-here'
SPOTIPY_CLIENT_SECRET='your-client-secret-here'
SPOTIPY_REDIRECT_URI='your-redirect-uri-of-choice-here'
```

You can get a client ID and secret by going to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and creating an app. Make sure that you go to the app settings and add your `SPOTIPY_REDIRECT_URI` environment variable as a Redirect URI.

There is also support for an optional environment variable to set the target IP address that should be broadcast to 
```shell
TARGET='target-ip-address'
```

## To Run
You can simply run `python3 spotilight.py` in your shell of choice! If this is your first time, you will need to authorize your instance of the Spotilight app to access your user data so it can get the currently playing track.

## Credits
Credit to the [python-kasa](https://github.com/python-kasa/python-kasa), [spotipy](https://github.com/plamere/spotipy), and [colorthief](https://github.com/fengsp/color-thief-py) repositories for the orignal work that made this possible.