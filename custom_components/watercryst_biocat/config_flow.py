import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_API_KEY, CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL

class WatercrystFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({
                    vol.Required(CONF_API_KEY): str,
                    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
                }),
            )
        return self.async_create_entry(title="Watercryst Biocat", data=user_input)
