import numpy as np


def generate_sphere(radius=1, u_steps=20, v_steps=20):
    u = np.linspace(0, 2 * np.pi, num=u_steps)
    v = np.linspace(0, np.pi, num=v_steps)
    u, v = np.meshgrid(u, v)

    x = radius * np.sin(v) * np.cos(u)
    y = radius * np.sin(v) * np.sin(u)
    z = radius * np.cos(v)

    return x, y, z