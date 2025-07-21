from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .coordinator import WatercrystDataUpdateCoordinator

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up integration"""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Watercryst Biocat from a config entry."""
    api_key = entry.data["api_key"]
    scan_interval = entry.data.get("scan_interval", 300)

    coordinator = WatercrystDataUpdateCoordinator(hass, api_key, scan_interval)
    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    # Plattformen (z. B. sensor) laden
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
