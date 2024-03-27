import asyncio
import os
import sys

from cody_agent_py.messaging import (
    _handle_server_respones,
    _hasResult,
    _send_jsonrpc_request,
    _show_last_message,
)

from .config import Config
from .server_info import ServerInfo

config = Config("")

message_id = 1


async def get_configs():
    return config


async def create_server_connection(
    configs: Config,
) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    config = configs
    if config.BINARY_PATH == "" or config.BINARY_PATH is None:
        print(
            "You need to specify the BINARY_PATH to an absolute path to the agent binary or to the index.js file. Exiting..."
        )
        sys.exit(1)
    os.environ["CODY_AGENT_DEBUG_REMOTE"] = str(config.USE_TCP).lower()
    process = await asyncio.create_subprocess_exec(
        "bin/agent" if config.USE_BINARY else "node",
        "jsonrpc" if config.USE_BINARY else f"{config.BINARY_PATH}/index.js",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        env=os.environ,
    )

    reader = None
    writer = None

    if not config.USE_TCP:
        print("--- stdio connection ---")
        reader = process.stdout
        writer = process.stdin

    else:
        print("--- TCP connection ---")
        while True:
            try:
                reader, writer = await asyncio.open_connection(*config.SERVER_ADDRESS)
                print(f"Connected to server: {config.SERVER_ADDRESS}\n")
                break
            except ConnectionRefusedError:
                await asyncio.sleep(0.1)  # Retry after a short delay

    return reader, writer, process


async def send_initialization_message(
    reader, writer, process, client_info
) -> ServerInfo:

    await _send_jsonrpc_request(
        writer, "initialize", client_info.model_dump(warnings=True)
    )
    async for response in _handle_server_respones(reader, process):
        if config.IS_DEBUGGING:
            print(f"Response: \n\n{response}\n")
        if response and await _hasResult(response):
            server_info: ServerInfo = ServerInfo.model_validate(response["result"])
            if config.IS_DEBUGGING:
                print(f"Server Info: {server_info}\n")
            return server_info


async def new_chat_session(reader, writer, process) -> str:
    await _send_jsonrpc_request(writer, "chat/new", None)
    async for response in _handle_server_respones(reader, process):
        if response and await _hasResult(response):
            result_id = response["result"]
            if config.IS_DEBUGGING:
                print(f"Result: \n\n{result_id}\n")
            return result_id


async def submit_chat_message(reader, writer, process, text, result_id):
    chat_message_request = {
        "id": f"{result_id}",
        "message": {
            "command": "submit",
            "text": text,
            "submitType": "user",
        },
    }
    await _send_jsonrpc_request(writer, "chat/submitMessage", chat_message_request)
    async for response in _handle_server_respones(reader, process):
        if response and await _hasResult(response):
            if config.IS_DEBUGGING:
                print(f"Result: \n\n{response}\n")
            await _show_last_message(response["result"])


async def cleanup_server_connection(writer, process):
    await _send_jsonrpc_request(writer, "exit", None)
    if process.returncode is None:
        process.terminate()
    await process.wait()