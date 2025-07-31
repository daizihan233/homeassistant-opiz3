import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, SENSOR_TYPES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """设置传感器实体"""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for sensor_id, sensor_info in SENSOR_TYPES.items():
        entities.append(
            Opiz3TemperatureSensor(coordinator, sensor_id, sensor_info)
        )

    async_add_entities(entities)

class Opiz3TemperatureSensor(CoordinatorEntity, SensorEntity):
    """温度传感器实体"""

    def __init__(self, coordinator, sensor_id, sensor_info):
        super().__init__(coordinator)
        self.sensor_id = sensor_id
        self._attr_name = f"OPIZ3 {sensor_info['name']}"
        self._attr_unique_id = f"opiz3_{sensor_id}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_icon = sensor_info["icon"]
        self._attr_device_class = sensor_info.get("device_class")

    @property
    def available(self):
        """实体是否可用"""
        return super().available and self.coordinator.data is not None

    @property
    def native_value(self):
        """返回当前温度值"""
        if self.coordinator.data and self.sensor_id in self.coordinator.data:
            return self.coordinator.data[self.sensor_id]["current"]
        return None

    @property
    def extra_state_attributes(self):
        """返回额外属性"""
        if not self.coordinator.data or self.sensor_id not in self.coordinator.data:
            return {}

        data = self.coordinator.data[self.sensor_id]
        return {
            "high_temp": data.get("high"),
            "critical_temp": data.get("critical"),
            "last_updated": self.coordinator.last_update_success_time.isoformat() if self.coordinator.last_update_success_time else None
        }