from fastapi import FastAPI, Request
from monpi.health import get_curent_usage
import time
from . import health


class Monitor:
    def __init__(self, app: FastAPI, save_limit: int | None = None) -> None:
        self.app = app
        self.data = {}
        self.data_uid: int = 0
        self.save_limit: int = save_limit or 1000
        self.first_uid: int = self.data_uid

        @app.middleware("http")
        async def monitor_service(request: Request, call_next):
            start_time = time.perf_counter()
            data_dict = self.data[self.data_uid] = {}
            data_dict["url"] = request.url
            data_dict["client"] = request.client
            data_dict["method"] = request.method
            response = await call_next(request)
            end_time = time.perf_counter()
            data_dict["respone_time"] = end_time - start_time
            data_dict["status_code"] = response.status_code
            if (self.data_uid - self.first_uid) > self.save_limit:
                del data_dict[self.first_uid]
                self.first_uid += 1
            return response

        @app.get("/monitor/data")
        async def return_data():
            return self.data

        @app.get("/monitor/health")
        async def return_health():
            return await health.get_curent_usage()

        def current_stats():
            return self.data
