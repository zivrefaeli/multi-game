# Multi Game
A multiplayer game on LAN developed in Python with UI libraries.
<br />
The server is based on multithreading. In the future it will use the _Select_ library.

## Demo
For example, two clients inside a server

![multi-game](/assets/demo.gif)

## Usage
Run the **main.py** file with a _Flag_ starts with - / -- / empty
| Server Flags | Client Flags |
| ------ | ------ |
| server | client |
| s | c |

Start a server
```bash
python ./main.py --server
```

Run a client
```bash
python ./main.py --client
```

## License
multi-game was created by Ziv Refaeli and released under the [MIT license](https://github.com/zivrefaeli/multi-game/blob/master/LICENCE)
