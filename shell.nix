{ pkgs ? import <nixpkgs> {}, lib ? pkgs.lib }:

pkgs.mkShell rec {
  nativeBuildInputs = [ 
    pkgs.glfw 
    pkgs.freetype.out
    pkgs.python3
    pkgs.python39Packages.pip 
    pkgs.python39Packages.numpy
    pkgs.python39Packages.pynput
    pkgs.python39Packages.pyopengl
    pkgs.python39Packages.virtualenv
    pkgs.python39Packages.setuptools
  ];
 
  libPath = lib.makeLibraryPath nativeBuildInputs;
  shellHook = ''
    export LD_LIBRARY_PATH=$libPath:$LD_LIBRARY_PATH
    if [[ -d "venv" ]]
    then
      echo "venv exists already. Skipping creation."
    else
      echo "venv does not exist, creating.."
      python3 -m venv ./venv
    fi
    ./venv/bin/python3 -m pip install keyboard glumpy
  '';
}
