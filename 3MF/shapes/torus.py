import numpy as np



def generate_torus(major_radius, minor_radius, u_steps, v_steps):
    u = np.linspace(0, 2 * np.pi, u_steps)
    v = np.linspace(0, 2 * np.pi, v_steps)
    u, v = np.meshgrid(u, v)
    x = (major_radius + minor_radius * np.cos(v)) * np.cos(u)
    y = (major_radius + minor_radius * np.cos(v)) * np.sin(u)
    z = minor_radius * np.sin(v)
    return x, y, z


if __name__ == "__main__":
    x, y, z = generate_torus(major_radius=1, minor_radius=0.5, u_steps=20, v_steps=20)
    print(x)
    print(y)
    print(z)

