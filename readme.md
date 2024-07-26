# Socks Viewer

Socks Viewer is a simple application that allows you to set up a transparent socks v5 proxy with ability to see the connections coming through the proxy.


## Install

To use socks viewer you need to have installed: Python 3, and the dependency of this application. To install dependency do:

```
pip3 install -r ./requirements.txt
```

##

Before you can start GUI of this app, you need to start background processes. There are two of them and you need to start them in a separate terminal sessions. 

```
bash ./start_socketio_dispatcher.sh
```

```
bash ./start_socks_server.sh
```

To start gui simply use the BASH startup script
```
bash ./start_gui.sh
```

You may need to change the configuration of the application. All configuration is based in config files present in configs directory. In the default scenario socket server is listening on localhost at port 8080, socketio dispatcher is listening on localhost at port 10013.

Application allows to use the socks_server and socketio_dispatcher on separate machines than the gui. To achieve this approach you need to make sure that the socketio_dispatcher being accessable from the network(listening on the IP address instead of localhost and allowing traffic on the system firewall) and have matching pair of host and port in the socketio entry in the config files.

Applications (socks_server and a socketio_dispather) do require an instance of a Redis server running on the machine to be able to runs.