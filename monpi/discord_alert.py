import asyncio
import httpx


async def send_dircord_alert(webhhok: str, message: str):
    async with httpx.AsyncClient(timeout=1.0) as client:
        try:
            await client.post(webhook, json={"content": message})
        except Exception as e:
            print("Error: ", str(e))
