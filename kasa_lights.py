import asyncio
from typing import Iterable, List
from kasa import Discover

class KasaLights:
    def __init__(self, bulbs: List):
        self.bulbs = bulbs

    # Because init cannot be async, use a static factory method here
    @staticmethod
    async def make(aliases: Iterable = None, **kwargs):
        # Finds all TPLink Kasa Smart Devices based on input
        devices = dict(await Discover.discover(**kwargs)).values()

        if aliases is None:
            # Filters the found devices by bulbs which have the ability to set color
            bulbs = list(filter(lambda device : device.is_bulb and device.is_color, devices))
        else:
            # Only gets bulbs that match an input alias (may be useful if you only want to control some bulbs)
            aliases = set(aliases)
            bulbs = list(filter(lambda device : device.is_bulb and device.is_color and device.alias in aliases, devices))

        if (len(bulbs) == 0):
            # Fails fast if no bulbs are found
            raise Exception('Unable to find any Kasa bulbs')
        return KasaLights(bulbs)

    async def update(self):
        # Updates all bulbs concurrently
        return await asyncio.gather(*[bulb.update() for bulb in self.bulbs])

    async def set_color(self, *args, **kwargs):
        # Sets color for all bulbs concurrently
        return await asyncio.gather(*[bulb.set_hsv(*args, **kwargs) for bulb in self.bulbs])

    def get_avg_brightness(self):
        # Sets color for all bulbs concurrently
        return sum(bulb.brightness for bulb in self.bulbs)/float(len(self.bulbs))
