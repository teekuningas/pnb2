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
python -m pnb2.networking.server
#### Run client
python -m pnb2.networking.client
