"""Orange Pi Zero 3 温度监控集成"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .coordinator import TemperatureCoordinator

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """设置集成入口"""
    # 创建协调器实例
    coordinator = TemperatureCoordinator(hass)

    # 确保第一次刷新成功
    await coordinator.async_config_entry_first_refresh()

    # 存储协调器
    hass.data.setdefault("opiz3_monitor", {})
    hass.data["opiz3_monitor"][entry.entry_id] = coordinator

    # 设置传感器平台
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载集成"""
    # 卸载传感器平台
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")

    # 移除协调器
    if unload_ok:
        hass.data["opiz3_monitor"].pop(entry.entry_id)

    return unload_ok