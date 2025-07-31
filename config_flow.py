"""配置流处理"""
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN

class Opiz3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """处理配置流"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """处理用户初始步骤"""
        # 如果已经配置过，直接跳过
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        # 如果没有用户输入，显示表单
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema({})
            )

        # 创建配置条目
        return self.async_create_entry(
            title="Orange Pi Zero 3 Monitor",
            data={}
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """获取选项流"""
        return Opiz3OptionsFlow(config_entry)

class Opiz3OptionsFlow(config_entries.OptionsFlow):
    """处理选项流"""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """管理选项"""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({})
        )