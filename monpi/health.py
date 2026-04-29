import psutil
import os


async def get_curent_usage():
    usage_dict = {}
    usage_dict["status"] = "online"
    usage_dict["cpu"] = psutil.cpu_percent(interval=1)
    usage_dict["ram"] = psutil.virtual_memory().percent
    return usage_dict
