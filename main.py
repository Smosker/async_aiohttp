import asyncio
import aiohttp


class Helper:
    def __init__(self, session, urls):
        self.url_objects = urls
        self.session = session

    async def fetch(self, request, url_object):
        async with self.session.request(**request) as response:
            result = await response.read()
            response.raise_for_status()

        return result, url_object

    async def get_result(self):
        result_obj = {}
        tasks = [
            self.fetch(request=request, url_object=url_object)
            for request, url_object in self.create_requests()
        ]
        for future in asyncio.as_completed(tasks):
            response, url_object = await future
            result_obj[url_object] = len(response)

        return result_obj

    def create_requests(self):
        requests = []
        for url_object in self.url_objects:
            request = self.create_request(url_object)
            requests.append((request, url_object))

        return requests

    def create_request(self, url_object, ):
        return dict(
            url=url_object,
            method='GET',
        )


async def run(urls):
    async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(
                verify_ssl=False,
            ),
    ) as session:
        helpers = [Helper(session=session, urls=urls)]

        result_obj = []
        tasks = [asyncio.ensure_future(helper.get_result())
                 for helper in helpers]

        for future in asyncio.as_completed(tasks):
            result = await future
            result_obj.append(result)

    return result_obj


loop = asyncio.get_event_loop()
result = loop.run_until_complete(run([
    'https://google.ru',
    'https://www.google.com/?gfe_rd=cr&dcr=0&ei=I5cNWr1lh7joBIbethg',
]))

print(result)
