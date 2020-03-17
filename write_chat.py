import asyncio
import logging
import json

import configargparse
from dotenv import load_dotenv


logger = logging.getLogger('sender')


def processing_message(msg):
    msg, *_ = msg.decode().split('\n')
    msg = json.loads(msg)
    return msg


async def write(writer, msg):
    writer.write(msg.encode())
    writer.write('\n\n'.encode())


async def authorise(reader, writer, token):
    await write(writer, token)
    logger.debug(token)

    message = await reader.readline()
    message = processing_message(message)
    logger.debug(message)

    return bool(message)


async def register(reader, writer):
    nickname = input('Enter preferred nickname below: \n')

    await write(writer, nickname)
    logger.debug(nickname)

    message = await reader.readline()
    logger.debug(message)

    message = await reader.readline()
    logger.debug(message)

    message = processing_message(message)
    logger.debug(message)

    return message.get('account_hash')


async def submit_message(writer, message):
    await write(writer, message)
    logger.debug(message)


async def write_to_chat(host, port, token, message):
    reader, writer = await asyncio.open_connection(
            host=host, port=port,
    )

    response = await reader.readline()
    logger.debug(response.decode())

    if not await authorise(reader, writer, token):
        logger.debug('Неизвестный токен. Проверьте его или зарегистрируйте заново.')
        token = await register(reader, writer)
        logger.debug('Новый токен: {}'.format(token))
        writer.close()

    await submit_message(writer, message)
    writer.close()


def create_parser():
    parser = configargparse.ArgParser()
    parser.add('-ht', '--host', env_var='HOST')
    parser.add('-p', '--port', env_var='WRITE_PORT')
    parser.add('-m', '--message', env_var='MESSAGE')
    parser.add('-t', '--token', env_var='TOKEN')
    return parser


if __name__ == '__main__':
    load_dotenv()

    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    parser = create_parser()
    namespace = parser.parse_args()

    asyncio.run(write_to_chat(
        host=namespace.host,
        port=5050,
        token=namespace.token,
        message=namespace.message
    ))
