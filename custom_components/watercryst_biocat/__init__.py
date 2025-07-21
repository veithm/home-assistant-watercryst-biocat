from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .coordinator import WatercrystDataUpdateCoordinator
from .api import pause_protection, unpause_protection

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    api_key = entry.data["api_key"]
    scan_interval = entry.data.get("scan_interval", 300)

    coordinator = WatercrystDataUpdateCoordinator(hass, api_key, scan_interval)
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    async def handle_pause(call: ServiceCall):
        minutes = call.data.get("minutes", 60)
        pause_protection(api_key, minutes)

    async def handle_unpause(call: ServiceCall):
        unpause_protection(api_key)

    hass.services.async_register(DOMAIN, "pause_protection", handle_pause)
    hass.services.async_register(DOMAIN, "unpause_protection", handle_unpause)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
