from os import initgroups
from fastapi import FastAPI, Request, HTTPException
from monpi.health import get_curent_usage
import time
from . import health
from monpi.discord_alert import send_dircord_alert


class Monitor:
    def __init__(
        self,
        app: FastAPI,
        save_limit: int | None = None,
        aleart: bool = False,
        discord_webhook: str | None = None,
    ):
        """
        Middleware intercepts every request and response, track and alert via discord messages
        """
        self.app = app
        self.data = {}
        self.data_uid: int = 0
        self.save_limit: int = save_limit or 100
        self.first_uid: int = self.data_uid
        self.error: int = 0
        self.discord_webhook = discord_webhook
        if aleart and not discord_webhook:
            raise ValueError("Please Provide Discord Webhook If Set Alert as True")

        @app.middleware("http")
        async def monitor_service(request: Request, call_next):
            start_time = time.perf_counter()
            data_dict = self.data[self.data_uid] = {}
            data_dict["url"] = request.url
            data_dict["method"] = request.method
            try:
                response = await call_next(request)
                end_time = time.perf_counter()
                data_dict["response_time"] = end_time - start_time
                data_dict["status_code"] = response.status_code
                if (self.data_uid - self.first_uid) > self.save_limit:
                    del data_dict[self.first_uid]
                    self.first_uid += 1
                print(response.status_code)
                if response.status_code >= 500 and aleart:
                    await send_dircord_alert(
                        self.discord_webhook,
                        f"""Error:- Status Code : {response.status_code}, \
                                            url : {data_dict["url"]},\
                                            Response Time: {data_dict["response_time"]},
                                            Response Status: {response.status_code}\
                                            Method: {data_dict["method"]}, \
                                            Resources: {await get_curent_usage()}""",
                    )
                return response
                self.data_uid += 1
            except Exception as e:
                end_time = time.perf_counter()
                data_dict["response_time"] = end_time - start_time
                if (self.data_uid - self.first_uid) > self.save_limit:
                    del data_dict[self.first_uid]
                    self.first_uid += 1
                if aleart:
                    await send_dircord_alert(
                        self.discord_webhook,
                        f"""Error Status Code : 500, \
                                            Url : {data_dict["url"]},\
                                            Response Time: {data_dict["response_time"]}, \
                                            Method: {data_dict["method"]},\
                                            Exception: {str(e)}, \
                                            Resources: {await get_curent_usage()}""",
                    )
                self.data_uid += 1
                raise HTTPException(
                    status_code=500, detail=f"Something went wrong : {str(e)}"
                )

        @app.get("/monitor/data")
        async def return_data():
            return self.data

        @app.get("/monitor/health")
        async def return_health():
            return await health.get_curent_usage()

        def current_stats():
            return self.data
