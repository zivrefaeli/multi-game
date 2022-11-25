# Multi Game
A multiplayer game on LAN developed in Python with UI libraries.
<br />
Server is based on multithreading method. In future it will use _Select_ library.

## Demo
Two clients inside the server

![multi-game](/assets/demo.gif)

## Usage
Run the **main.py** file with a _Flag_ starts with - / --
| Server Flags | Client Flags |
| ------ | ------ |
| server | client |
| s | c |

Run server
```bash
python ./main.py -server
python ./main.py -s
```

Run client
```bash
python ./main.py -client
python ./main.py -c
```

## License
multi-game was created by Ziv Refaeli and released under the MIT license
