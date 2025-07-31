import logging
import requests
import time
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
UPDATE_INTERVAL = timedelta(seconds=60)
MAX_FAILURES = 3

class TemperatureCoordinator(DataUpdateCoordinator):
    """温度数据协调器"""

    def __init__(self, hass):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=UPDATE_INTERVAL,
        )
        self.fail_count = 0
        self.api_url = "http://127.0.0.1:8080/sensors/temperatures"
        self.timeout = 5

    async def _async_update_data(self):
        """从API获取最新数据"""
        try:
            # 使用HA的异步执行器执行同步请求
            response = await self.hass.async_add_executor_job(
                self._fetch_data
            )

            if response.get('status') == 'success':
                self.fail_count = 0
                return response['data']
            else:
                raise UpdateFailed(f"API error: {response.get('message', 'Unknown error')}")

        except Exception as err:
            self.fail_count += 1
            self.logger.warning("更新失败 (#%d): %s", self.fail_count, str(err))

            if self.fail_count >= MAX_FAILURES:
                self.logger.error("连续 %d 次更新失败，标记为离线", MAX_FAILURES)
                raise UpdateFailed(f"设备离线: {str(err)}")

            return None

    def _fetch_data(self):
        """执行实际的HTTP请求"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as err:
            raise UpdateFailed(f"请求失败: {str(err)}")