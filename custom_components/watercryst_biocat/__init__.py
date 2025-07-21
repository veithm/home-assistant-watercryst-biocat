from homeassistant.core import HomeAssistant, ServiceCall
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

    #
    # --- Service Handler (async wrapper calling sync functions) ---
    #
    async def handle_pause(call: ServiceCall) -> None:
        minutes = call.data.get("minutes", 60)
        await hass.async_add_executor_job(pause_protection, api_key, minutes)

    async def handle_unpause(call: ServiceCall) -> None:
        await hass.async_add_executor_job(unpause_protection, api_key)

    # Register services (store names so we can remove them on unload)
    hass.services.async_register(DOMAIN, "pause_protection", handle_pause)
    hass.services.async_register(DOMAIN, "unpause_protection", handle_unpause)

    # Keep track so we can cleanly remove on unload
    hass.data[DOMAIN][entry.entry_id + "_services"] = ("pause_protection", "unpause_protection")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
