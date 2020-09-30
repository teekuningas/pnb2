#PNB 2 coming...

## Installation on arch
### GLFW should be installed
pacman -S glfw
### Python and some packages should be installed
pacman -S python
pip install pyopengl
pip install glumpy
pip install keyboard
### Download package and enter the folder
git clone https://github.com/Teekuningas/pnb2
cd pnb2

### steamworks
Use steampak and steamworks 1.42, run steam within same terminal.

### Running the game
#### Run server
python run\_server.py
#### Run input client
sudo python run\_player\_client.py
### Run graphics client
python run\_graphics\_client.py
