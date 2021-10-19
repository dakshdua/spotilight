import spotipy
from spotipy.oauth2 import SpotifyOAuth
from urllib.request import urlopen
import io
from colorthief import ColorThief

class SpotifyColorGrabber:
    def __init__(self):
        # Initializes spotipy and handles auth flow
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-currently-playing'))
        self.prev_track_id = None
        self.cached_pallete = None

    def get_current_playing_track_colors(self):
        # Get current track information from the Spotify Web API
        current_track_call = self.sp.current_user_playing_track()

        # If there nothing or something other than a track is currently playing, return None
        if current_track_call is None or current_track_call['currently_playing_type'] != 'track':
            return None
        
        # If the current track has not changed, return a cached palette
        current_track = current_track_call['item']
        if current_track['id'] == self.prev_track_id:
            return self.cached_pallete
        else:
            # If there is more than one image, gets the second-smallest one, otherwise gets the only image
            allimages = current_track['album']['images']
            if len(allimages) > 1:
                imageurl = allimages[-2]['url']
            else:
                imageurl = allimages[-1]['url']
            
            # Gets image from URL and initializes ColorThief with it
            color_thief = ColorThief(io.BytesIO(urlopen(imageurl).read()))

            # Gets the pallete and adds the dominant color in the front
            pallete = color_thief.get_palette(quality=1)
            pallete.insert(0, color_thief.get_color(quality=1))

            # Cache current info and return
            self.prev_track_id = current_track['id']
            self.cached_pallete = pallete
            return pallete


if __name__ == "__main__":
    # If run alone, gets currently playing album art colors
    print('Current colors:', SpotifyColorGrabber().get_current_playing_track_colors())
