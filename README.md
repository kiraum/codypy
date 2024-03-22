# CodyAgentPy 🐍🤖

**This is a WIP (work-in-progress) project** 🚧👷‍♂️

CodyAgentPy is a Python script that establishes a connection to the Cody-Agent server from [Sourcegraph Cody](https://github.com/sourcegraph/cody) using JSON-RPC (Remote Procedure Call) protocol over a TCP connection. It allows sending and receiving JSON-RPC messages asynchronously. 📨📥

**Note: This project is currently in an experimental alpha stage. The API and functionality may change and break in future versions.** ⚠️🔧



## Features

- Connects to a server using TCP sockets
- Sends JSON-RPC messages to the server
- Receives and processes JSON-RPC messages from the server
- Handles connection errors and timeouts
- Extracts method and result from JSON-RPC responses
- Supports asynchronous communication using `asyncio` library

## Requirements

- Python 3.7+
- `asyncio` library

## Installation
### Linux

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/CodyAgentPy.git
   ```

2. Navigate to the project directory:
   ```
   cd CodyAgentPy
   ```

3. Ensure you have Python 3.7 or higher installed:
   ```
   python --version
   ```

4. The `asyncio` library is included in the Python standard library, so no additional installation is required.

You are now ready to use CodyAgentPy!


## Usage

1. Set the `SERVER_ADDRESS` variable to the desired server address and port.
2. Run the script using `python CodyAgentPy.py`.
3. The script will attempt to connect to the specified server.
4. If the connection is successful, it will send an initialization message to the server.
5. The script will then receive and process JSON-RPC messages from the server.
6. It will extract and display the method and result from the received messages.
7. The script will continue to receive messages until the server closes the connection or a timeout occurs.

## Example

```python
async def main():
    await connect_to_server()

if __name__ == "__main__":
    asyncio.run(main())
```

This example demonstrates how to use the `connect_to_server()` function to establish a connection to the server and process JSON-RPC messages.

## Roadmap

- [ ] Improve the parsing and handling of JSON-RPC responses in `receive_jsonrpc_messages()` function.
- [ ] Enhance the initialization message in `initializing_message()` function to include additional client information.
- [ ] Implement logging functionality to track client-server communication.
- [ ] Add configuration options for server address, port, and other settings.
- [ ] Develop unit tests for key functions in `CodyAgentPy.py`.
- [ ] Create documentation and examples for using the `CodyAgentPy` client library.


## License

Copyright notices for third-party code included are licensed under their respective licenses.

This project is licensed under the [MIT License](LICENSE).