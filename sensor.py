from homeassistant.components.sensor import SensorEntity
from homeassistant.const import TEMP_CELSIUS
from .coordinator import TemperatureCoordinator

# 手册3.14节提到的传感器列表
SENSOR_TYPES = {
    "cpu_thermal": {
        "name": "CPU Temperature",
        "icon": "mdi:cpu-64-bit",
        "unit": TEMP_CELSIUS
    },
    "gpu_thermal": {
        "name": "GPU Temperature",
        "icon": "mdi:gpu",
        "unit": TEMP_CELSIUS
    },
    "ddr_thermal": {
        "name": "DDR Temperature",
        "icon": "mdi:memory",
        "unit": TEMP_CELSIUS
    },
    "ve_thermal": {
        "name": "VE Temperature",
        "icon": "mdi:video-3d",
        "unit": TEMP_CELSIUS
    }
}

async def async_setup_entry(hass, config_entry, async_add_entities):
    """设置传感器实体"""
    coordinator = TemperatureCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    entities = []
    for sensor_id, sensor_info in SENSOR_TYPES.items():
        entities.append(
            Opiz3TemperatureSensor(coordinator, sensor_id, sensor_info)
        )

    async_add_entities(entities)

class Opiz3TemperatureSensor(SensorEntity):
    """温度传感器实体"""

    def __init__(self, coordinator, sensor_id, sensor_info):
        self.coordinator = coordinator
        self.sensor_id = sensor_id
        self._attr_name = f"OPIZ3 {sensor_info['name']}"
        self._attr_unique_id = f"opiz3_{sensor_id}"
        self._attr_native_unit_of_measurement = sensor_info["unit"]
        self._attr_icon = sensor_info["icon"]

    @property
    def available(self):
        """实体是否可用"""
        return self.coordinator.last_update_success

    @property
    def native_value(self):
        """返回当前温度值"""
        data = self.coordinator.data
        if data and self.sensor_id in data:
            return data[self.sensor_id]["current"]
        return None

    @property
    def extra_state_attributes(self):
        """返回额外属性"""
        data = self.coordinator.data.get(self.sensor_id, {}) if self.coordinator.data else {}
        return {
            "high_temp": data.get("high"),
            "critical_temp": data.get("critical"),
            "last_updated": self.coordinator.last_update_time.isoformat()
        }

    async def async_added_to_hass(self):
        """注册更新回调"""
        self.async_on_remove(
            self.coordinator.async_add_listener(
                self.async_write_ha_state
            )
        )