# Run Instructions

## What Folder to choose
All runnable files are python and are stored in:
`client_server-py`

Note: `client_server-cpp` are old files and should be disreguarded, just for historical documentation

## Neccessary version and libraries

### Python 3.10
Server was developed on python 3.10 and is the recommended version to use
To install type (installation for debian based systems using apt-get):
`sudo apt install software-properties-common -y`
`sudo add-apt-repository ppa:deadsnakes/ppa`
`sudo apt install python3.10`

For a direct install not using apt, python 3.10 can be downloaded from:
`https://www.python.org/downloads/release/python-3100/`

### Curses
SHould be included in linux and mac versions of python, but if not you can try
`python -m pip install windows-curses`

## How to run

To Run the Server type:
`python3.10 hangman-server.py [server-port]`

To Run the Client type:
`python3.10 hangman-client.py [server-ip] [server-port]`

