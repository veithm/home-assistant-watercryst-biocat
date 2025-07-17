import logging
from homeassistant.components.webhook import WebhookRequest
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def handle_webhook(hass, entry_id, request: WebhookRequest):
    try:
        data = await request.json()
        _LOGGER.debug("Received webhook data: %s", data)

        coordinator = hass.data[DOMAIN].get(entry_id)
        if coordinator:
            coordinator.data = data
            await coordinator.async_request_refresh()
        else:
            _LOGGER.warning("No coordinator for entry_id %s", entry_id)
    except Exception as e:
        _LOGGER.exception("Failed to handle webhook: %s", e)
