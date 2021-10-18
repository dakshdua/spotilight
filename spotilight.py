import asyncio
from dotenv import load_dotenv
from kasa_lights import KasaLights
from spotify_color_grabber import SpotifyColorGrabber
import sys
import time
import colorsys
import os

async def driver():
    # Prevents false errors from appearing on Windows
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Loads from .env file if exists, does nothing if not
    load_dotenv()

    # Initializes SpotifyColorGrabber (may lead to Auth flow if first time)
    spotify_color_grabber = SpotifyColorGrabber()

    # Makes KasaLights
    target = os.environ.get('TARGET')
    if target is None:
        lights = await KasaLights.make()
    else:
        lights = await KasaLights.make(target=target)

    prev_color = None
    while True:
        # Gets color pallete for current album art
        color_pallete = spotify_color_grabber.get_current_playing_track_colors()

        if color_pallete is None:
            time.sleep(10)
            continue
        
        # Takes top color and converts it from RGB to HSV
        color_rgb = tuple(val/255.0 for val in color_pallete[0])
        hsv_denorm = (360, 100, 100)
        color_hsv_norm = colorsys.rgb_to_hsv(*color_rgb)
        color_hsv = tuple(round(val * mult) for val, mult in zip(color_hsv_norm, hsv_denorm))

        # Sets light color if it is different from previous one
        if color_hsv != prev_color:
            # print('setting lights to:', color_hsv)
            prev_color = color_hsv
            await lights.set_color(*color_hsv, transition=2_000)

        # Waits 2 seconds before polling Spotify API to see if track is different
        time.sleep(2)

if __name__ == "__main__":
    asyncio.run(driver())
