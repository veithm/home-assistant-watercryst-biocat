import logging
from datetime import timedelta
import aiohttp
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class WatercrystDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key, scan_interval):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )
        self.api_key = api_key

    async def _async_update_data(self):
        headers = {"X-API-KEY": self.api_key}
        data = {}
        _LOGGER.error("using API KEY %s", self.api_key)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://appapi.watercryst.com/v1/measurements/direct", headers=headers) as resp1:
                if resp1.status != 200:
                    text = await resp1.text()
                    _LOGGER.error("Measurement API returned %s: %s", resp1.status, text)
                    raise Exception("Measurement API error")
                data.update(await resp1.json())

            async with session.get("https://appapi.watercryst.com/v1/state", headers=headers) as resp2:
                if resp2.status == 200:
                    state = await resp2.json()
                    data["online"] = state.get("online")
                    data["deviceMode"] = state.get("mode", {}).get("name")
                    data["mlState"] = state.get("mlState")

            async with session.get("https://appapi.watercryst.com/v1/statistics/cumulative/total", headers=headers) as resp3:
                if resp3.status == 200:
                    total = await resp3.text()
                    data["totalWaterConsumption"] = float(total)

        return data
