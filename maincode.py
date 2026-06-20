import tkinter as tk
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

ani = None  # it gives realtime animation

def run_simulation(v, angle_deg, g, x0, y0):
    global ani
    plt.close('all')

    if v == 0:
        messagebox.showerror("Error", "Velocity cannot be zero.")
        return

    if angle_deg < 0 or angle_deg > 90:
        messagebox.showerror("Error", "Angle must be between 0° and 90°.")
        return

    theta = np.radians(angle_deg)
    vx = abs(v) * np.cos(theta)
    if v < 0:  # negative velocity → left
        vx = -vx
    vy_initial = abs(v) * np.sin(theta)

    # realtime coordinates

    discriminant = vy_initial**2 + 2 * g * y0
    t_flight = (vy_initial + np.sqrt(discriminant)) / g if discriminant >=0 else 0.01
    t = np.linspace(0, t_flight, 300)

    # Trajectory Equations
    x = x0 + vx * t
    y = y0 + vy_initial * t - 0.5 * g * t**2

    # Find first index where y <= 0
    ground_idx = np.argmax(y <= 0)
    if ground_idx == 0:  # didn't cross ground
        ground_idx = len(t) - 1

    # It Only keeps frames until it hits the ground
    x = x[:ground_idx + 1]
    y = np.maximum(y[:ground_idx + 1], 0)
    t = t[:ground_idx + 1]

    # Plot setup
    fig, ax = plt.subplots()
    ax.set_title("Projectile Motion Simulation")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.grid(True)

    ax.set_xlim(min(x)-1, max(x)+1)
    ax.set_ylim(0, max(y)+2)

    # Trail line and projectile dot
    trail_line, = ax.plot([], [], 'b-', lw=2)
    dot, = ax.plot([], [], 'ro', markersize=8)

    # Landing marker [red marker]
    landing_marker, = ax.plot([], [], 'rx', markersize=10, markeredgewidth=2)

    info_text = ax.text(
        0.03, 0.95, "", transform=ax.transAxes, fontsize=10, va="top",
        bbox=dict(facecolor='white', alpha=0.7)
    )

    def update(frame):
        trail_line.set_data(x[:frame+1], y[:frame+1])
        dot.set_data([x[frame]], [y[frame]])

        # Show landing marker at last frame
        if frame == len(x) - 1:
            landing_marker.set_data([x[frame]], [y[frame]])

        vy = vy_initial - g * t[frame]

        info_text.set_text(
            f"t = {t[frame]:.2f} s\n"
            f"x = {x[frame]:.2f} m\n"
            f"y = {y[frame]:.2f} m\n"
            f"vx = {vx:.2f} m/s\n"
            f"vy = {vy:.2f} m/s"
        )

        return trail_line, dot, landing_marker, info_text

    ani = FuncAnimation(fig, update, frames=len(t), interval=20, repeat=False)
    plt.show(block=True)


def start_simulation():
    try:
        v = float(entry_velocity.get())
        angle = float(entry_angle.get())
        g = float(entry_gravity.get())
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())

        run_simulation(v, angle, g, x0, y0)

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")


# Its for GUI 
root = tk.Tk()
root.title("Projectile Motion Simulator")

tk.Label(root, text="Initial Velocity (m/s, negative = left):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_velocity = tk.Entry(root)
entry_velocity.grid(row=0, column=1)
entry_velocity.insert(0, "20")

tk.Label(root, text="Launch Angle (° 0-90):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_angle = tk.Entry(root)
entry_angle.grid(row=1, column=1)
entry_angle.insert(0, "45")

tk.Label(root, text="Gravity (m/s²):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
entry_gravity = tk.Entry(root)
entry_gravity.grid(row=2, column=1)
entry_gravity.insert(0, "9.8")

tk.Label(root, text="Initial X-coordinate:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
entry_x0 = tk.Entry(root)
entry_x0.grid(row=3, column=1)
entry_x0.insert(0, "0")

tk.Label(root, text="Initial Y-coordinate:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
entry_y0 = tk.Entry(root)
entry_y0.grid(row=4, column=1)
entry_y0.insert(0, "0")

tk.Button(root, text="Run Simulation", command=start_simulation, bg="#4CAF50", fg="white").grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()