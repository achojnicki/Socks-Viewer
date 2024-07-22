# Socks Viewer

Socks Viewer is a simple application that allows you to set up a transparent socks v5 proxy with ability to see the connections coming through the server.


## Usage

To Use socks viewer you need to install dependecies of this application. You can do this by doing:

```
pip3 install -r ./requirements.txt
```

Before you can start GUI of this app, you need to start a background processes. There are two of them to start and you need to start them in separate terminal windows. 

```
bash ./start_socketio.dispatcher.sh
```

```
bash ./start_socks_server.sh
```

To start gui simply use the BASH startup script(start_gui.sh)
```
bash ./start_gui.sh
```

You may need to change the configuration of the application. All the configuration is based on config files in the configs directory. In the default scenario socket server is listening at localhost on port 8080,  socketio dispatcher is listening on localhost on port 10013.

Application allows to use the socks_server and a socketio_dispatcher on separate machine than the gui. To achieve this approach you need to set up the socketio_dispatcher being accessable from the network(listening on the IP address instead of localhost) and have matching pair of host and port of the socketio entry in the configs.

Application(socks_server and a socketio_dispather ) do require an instance of a Redis server running on the machine.