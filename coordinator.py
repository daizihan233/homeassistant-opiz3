import logging
import requests
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = 60  # 秒
MAX_FAILURES = 3      # 最大失败次数

class TemperatureCoordinator(DataUpdateCoordinator):
    """温度数据协调器"""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name="OPIZ3 Temperature Sensors",
            update_interval=UPDATE_INTERVAL,
        )
        self.fail_count = 0
        self.api_url = "http://127.0.0.1:8080/sensors/temperatures"
        self.timeout = 5  # 秒

    async def _async_update_data(self):
        """从API获取最新数据"""
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, self.api_url, {'timeout': self.timeout}
            )

            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    self.fail_count = 0
                    return data['data']
                else:
                    raise Exception(f"API error: {data.get('message')}")
            else:
                raise Exception(f"HTTP error: {response.status_code}")

        except Exception as e:
            self.fail_count += 1
            _LOGGER.warning("更新失败 (#%d): %s", self.fail_count, str(e))

            if self.fail_count >= MAX_FAILURES:
                _LOGGER.error("连续 %d 次更新失败，标记为离线", MAX_FAILURES)
                raise UpdateFailed("设备离线") from e

            return None