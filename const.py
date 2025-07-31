"""常量定义"""
DOMAIN = "opiz3_monitor"

# 温度传感器定义
SENSOR_TYPES = {
    "cpu_thermal": {
        "name": "CPU Temperature",
        "icon": "mdi:cpu-64-bit",
        "unit": "°C",
        "device_class": "temperature"
    },
    "gpu_thermal": {
        "name": "GPU Temperature",
        "icon": "mdi:gpu",
        "unit": "°C",
        "device_class": "temperature"
    },
    "ddr_thermal": {
        "name": "DDR Temperature",
        "icon": "mdi:memory",
        "unit": "°C",
        "device_class": "temperature"
    },
    "ve_thermal": {
        "name": "VE Temperature",
        "icon": "mdi:video-3d",
        "unit": "°C",
        "device_class": "temperature"
    }
}