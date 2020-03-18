import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def connect_socket(host, port):
    reader, writer = await asyncio.open_connection(
            host=host, port=port,
    )
    try:
        yield reader, writer
    finally:
        writer.close()
