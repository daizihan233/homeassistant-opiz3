"""Orange Pi Zero 3 温度监控集成"""
from .coordinator import TemperatureCoordinator

async def async_setup_entry(hass, entry):
    """设置集成入口"""
    coordinator = TemperatureCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault("opiz3_monitor", {})[entry.entry_id] = coordinator
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return True