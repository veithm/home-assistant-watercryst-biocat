from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN

SENSOR_TYPES = {
    "waterTemp": ("Wassertemperatur", "°C"),
    "pressure": ("Druck", "bar"),
    "flowRate": ("Durchfluss", "L/min"),
    "lastWaterTapVolume": ("Letzte Zapfmenge", "L"),
    "lastWaterTapDuration": ("Letzte Zapfdauer", "s"),
    "type": ("Datentyp", None),
}

async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]

    entities = [
        WatercrystSensor(coordinator, key, *SENSOR_TYPES.get(key, (key, None)))
        for key in coordinator.data
    ]
    async_add_entities(entities)

class WatercrystSensor(Entity):
    def __init__(self, coordinator, key, name, unit):
        self.coordinator = coordinator
        self.key = key
        self._name = name
        self._unit = unit
        self._attr_unique_id = f"watercryst_{key}"

    @property
    def name(self):
        return self._name

    @property
    def native_unit_of_measurement(self):
        return self._unit

    @property
    def state(self):
        return self.coordinator.data.get(self.key)

    async def async_update(self):
        await self.coordinator.async_request_refresh()
