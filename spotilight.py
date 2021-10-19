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
        # Gets loop start time to prevent overpolling Spotify Web API
        start_time = time.time()

        # Gets color pallete for current album art
        color_pallete = spotify_color_grabber.get_current_playing_track_colors()

        if color_pallete is None:
            time.sleep(10)
            continue
        
        # Updates light info (need it so brightness is updated if changed manually)
        await lights.update()

        # Takes top color and converts it from RGB to HSV
        color_rgb = tuple(val/255.0 for val in color_pallete[0])
        color_hsv_norm = colorsys.rgb_to_hsv(*color_rgb)

        # Denormalize returned hue and saturation (but keep current brightness)
        color_hsv = (round(color_hsv_norm[0] * 360), round(color_hsv_norm[1] * 100), round(lights.get_avg_brightness()))

        # Sets light color if it is different from previous one
        if color_hsv != prev_color:
            # print('setting lights to:', color_hsv)
            prev_color = color_hsv
            await lights.set_color(*color_hsv, transition=1000)

        # Waits to make sure that there is at least half a second of poll time
        time.sleep(max(0.5 - (time.time() - start_time), 0))

if __name__ == "__main__":
    asyncio.run(driver())
