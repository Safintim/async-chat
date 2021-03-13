import asyncio
from datetime import datetime

import aiofiles
import configargparse
from dotenv import load_dotenv

from tools import connect_socket

NUMBER_POSSIBLE_ATTEMPTS = 2
TIME_BETWEEN_ATTEMPTS = 3
FORMAT_TIME = '[%d.%m.%y %H:%M]'
TEMPLATE_MSG = '{0} {1}\n'

def get_datetime_now(format=FORMAT_TIME):
    return datetime.now().strftime(format)


async def write_message(file_obj, *template_params, template=TEMPLATE_MSG):
    await file_obj.write(template.format(*template_params))


async def wait_for_data(host, port, filepath):
    attempts_count = 0
    async with aiofiles.open(filepath, mode='a') as _file:
        async with connect_socket(host, port) as (reader, writer):
            try:
                await write_message(_file, get_datetime_now(), 'Установлено соединение')
                attempts_count = 0
                while True:
                    msg = await reader.readline()
                    await write_message(_file, get_datetime_now(), msg.decode().strip())
            except (ConnectionRefusedError, ConnectionResetError):
                current_datetime = get_datetime_now()
                attempts_count += 1
                await write_message(_file, current_datetime, 'Нет соединения. Повторная попытка.')
                if attempts_count >= NUMBER_POSSIBLE_ATTEMPTS:
                    message = 'Повторная попытка через {0} сек'.format(
                        TIME_BETWEEN_ATTEMPTS,
                    )
                    await write_message(_file, current_datetime, message)
                    await asyncio.sleep(TIME_BETWEEN_ATTEMPTS)


def create_parser():
    parser = configargparse.ArgParser()
    parser.add('-ht', '--host', env_var='HOST')
    parser.add('-p', '--port', env_var='READ_PORT')
    parser.add('-f', '--filepath', env_var='FILEPATH')
    return parser


if __name__ == '__main__':
    load_dotenv()
    parser = create_parser()
    namespace = parser.parse_args()
    asyncio.run(wait_for_data(
        namespace.host, namespace.port, namespace.filepath,
    ))
