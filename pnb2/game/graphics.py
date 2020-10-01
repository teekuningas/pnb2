""" Contains graphics implementations
"""
from glumpy import app
from glumpy import gl
from glumpy import glm
from glumpy import gloo

import numpy as np


vertex = """
uniform mat4   model;
uniform mat4   view;
uniform mat4   projection;
attribute vec3 position;
void main()
{
    gl_Position = projection * view * model * vec4(position,1.0);
}
"""

fragment = """
uniform vec4 color;
void main()
{
    gl_FragColor = color;
}
"""

class Engine:
    def __init__(self, window, backend):
        """
        """
        self.window = window
        self.backend = backend

        self.V = np.zeros(8, [("position", np.float32, 3)])
        self.V["position"] = [[ 1, 1, 1], [-1, 1, 1], [-1,-1, 1], [ 1,-1, 1],
                         [ 1,-1,-1], [ 1, 1,-1], [-1, 1,-1], [-1,-1,-1]]
        self.V = self.V.view(gloo.VertexBuffer)

        self.I = np.array([0,1,2, 0,2,3,  0,3,4, 0,4,5,  0,5,6, 0,6,1,
                      1,6,7, 1,7,2,  7,4,3, 7,3,2,  4,7,6, 4,6,5], dtype=np.uint32)
        self.I = self.I.view(gloo.IndexBuffer)

        self.cube = gloo.Program(vertex, fragment)
        self.cube.bind(self.V)

        model = np.eye(4, dtype=np.float32)
        self.cube['model'] = model

        self.window_closed = False

        self.on_draw = window.event(self.on_draw)
        self.on_resize = window.event(self.on_resize)
        self.on_init = window.event(self.on_init)
        self.on_close = window.event(self.on_close)

    def on_draw(self, dt):
        """
        """
        window = self.window
        window.clear()
        cube = self.cube
        cube['view'] = glm.translation(10, 0, -50)
        for player in self.game['players']:
            predicted_x = player['x'] + player['dx']*dt
            predicted_z = player['z'] + player['dz']*dt

            if player['team'] == 0:
                cube['color'] = [1, 0, 0, 1]
            else:
                cube['color'] = [0, 1, 0, 1]

            cube['view'] = glm.translation(predicted_x, predicted_z, -50)
            cube.draw(gl.GL_TRIANGLES, self.I)

    def on_resize(self, width, height):
        self.cube['projection'] = glm.perspective(45.0, width / float(height),
                                                  2.0, 100.0)

    def on_init(self):
        gl.glEnable(gl.GL_DEPTH_TEST)

    def on_close(self):
        self.window_closed = True

    def render(self, game, dt):
        self.game = game
        self.backend.process(dt)
        if self.window_closed:
            raise Exception('Window closed')

def render(engine, game, dt):
    """
    """
    engine.render(game, dt)


def initialize():
    """ 
    """

    window = app.Window(width=512, height=512, color=(0, 0, 0, 1))
    backend = app.__backend__

    engine = Engine(window, backend)

    return engine

