from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class WatercrystDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api_key, scan_interval):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=None
        )
        self.api_key = api_key
        self.data = {}

    async def _async_update_data(self):
        return self.data
