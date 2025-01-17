import aiohttp
import json

async def request_generic(url, method='get', reqparams=None, data=None, header={}, auth=None, returntype='text'):
    async with aiohttp.ClientSession(auth=None, raise_for_status=True) as session:
        async with session.request(method.upper(), url, params=reqparams, data=data, headers=header, auth=auth) as resp:
            if returntype == 'text':
                return await resp.text()
            elif returntype == 'json':
                return json.loads(await resp.text())
            elif returntype == 'binary':
                return await resp.read()

async def request_json_post(url, data, auth=None, returntype='text'):
    async with aiohttp.ClientSession(auth=auth, raise_for_status=True) as session:
        async with session.post(url=url, json=data, auth=auth) as resp:
            if returntype == 'text':
                return await resp.text()
            elif returntype == 'json':
                return json.loads(await resp.text())
            elif returntype == 'binary':
                return await resp.read()