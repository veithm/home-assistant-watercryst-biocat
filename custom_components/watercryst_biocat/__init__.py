from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .coordinator import WatercrystDataUpdateCoordinator
from .webhook import handle_webhook
from homeassistant.components.webhook import async_register

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass, entry):
    api_key = entry.data["api_key"]
    scan_interval = entry.data.get("scan_interval", 300)

    coordinator = WatercrystDataUpdateCoordinator(hass, api_key, scan_interval)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    webhook_id = f"{DOMAIN}_{entry.entry_id}"
    async_register(
        hass,
        DOMAIN,
        "Watercryst Biocat",
        webhook_id,
        lambda hass, wid, req: hass.async_create_task(
            handle_webhook(hass, entry.entry_id, req)
        ),
    )

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True

async def async_unload_entry(hass, entry):
    from homeassistant.components.webhook import async_unregister
    async_unregister(hass, f"{DOMAIN}_{entry.entry_id}")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
