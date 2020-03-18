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


async def wait_for_data(host, port, filepath):
    attempts_count = 0
    async with aiofiles.open(filepath, mode='a') as _file:
        async with connect_socket(host, port) as (reader, writer):
            try:
                current_datetime = datetime.now().strftime(FORMAT_TIME)
                await _file.write(
                    TEMPLATE_MSG.format(
                        current_datetime, 'Установлено соединение',
                    ),
                )
                attempts_count = 0
                while True:
                    msg = await reader.readline()
                    current_datetime = datetime.now().strftime(FORMAT_TIME)
                    await _file.write(
                        TEMPLATE_MSG.format(
                            current_datetime, msg.decode().strip(),
                        ),
                    )
            except (ConnectionRefusedError, ConnectionResetError):
                current_datetime = datetime.now().strftime(FORMAT_TIME)
                attempts_count += 1
                await _file.write(TEMPLATE_MSG.format(
                    current_datetime, 'Нет соединения. Повторная попытка.',
                ))
                if attempts_count >= NUMBER_POSSIBLE_ATTEMPTS:
                    message = 'Повторная попытка через {0} сек'.format(
                        TIME_BETWEEN_ATTEMPTS,
                    )
                    await _file.write(
                        TEMPLATE_MSG.format(
                            current_datetime, message,
                        ),
                    )
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
