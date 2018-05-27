import asyncio
import requests
import json
from aiohttp import ClientSession
from django.conf import settings
from channels.generic.http import AsyncHttpConsumer
from .constants import BLOGS


class NewsCollectorAsyncConsumer(AsyncHttpConsumer):

    async def handle(self, body):

        # Adapted from:
        # "Making 1 million requests with python-aiohttp"
        # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

        async def fetch(url, session):
            async with session.get(url) as response:
                return await response.read()

        async def run(blogs):
            tasks = []

            # Fetch all responses within one Client session,
            # keep connection alive for all requests.
            async with ClientSession() as session:
                for name, url in blogs.items():
                    print('Downloading "%s"' % name)
                    task = asyncio.ensure_future(fetch(url, session))
                    tasks.append(task)

                responses = await asyncio.gather(*tasks)
                # you now have all response bodies in this variable
                #print(responses)

            return responses

        # loop = asyncio.get_event_loop()
        # future = asyncio.ensure_future(run(BLOGS))
        # loop.run_until_complete(future)

        responses = await run(BLOGS)

        #data = dict([('???', r.decode('utf-8')) for r in responses])
        data = dict(zip(BLOGS.keys(), [r.decode('utf-8') for r in responses]))
        text = json.dumps(data)

        await self.send_response(200,
            text.encode(),
            headers=[
                ("Content-Type", "application/json"),
            ]
        )
