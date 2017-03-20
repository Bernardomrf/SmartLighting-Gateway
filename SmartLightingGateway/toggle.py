import uasyncio as asyncio


@asyncio.coroutine
def print_http_headers(url):
    reader, writer = yield from asyncio.open_connection(url, 12000)
    
    query = "GET / HTTP/1.0\r\n\r\n"
    yield from writer.awrite(query.encode('latin-1'))


url = "127.0.0.1"
loop = asyncio.get_event_loop()
#task = asyncio.async(print_http_headers(url))
#loop.run_until_complete(task)
loop.run_until_complete(print_http_headers(url))
loop.close()
