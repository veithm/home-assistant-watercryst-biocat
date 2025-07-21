from .const import DOMAIN
from .coordinator import WatercrystDataUpdateCoordinator

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    api_key = entry.data["api_key"]
    scan_interval = entry.data["scan_interval"]

    coordinator = WatercrystDataUpdateCoordinator(hass, api_key, scan_interval)
    await coordinator.async_refresh()

    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
