import pyaudio
import numpy as np
import win32gui
import win32con
import win32api
import win32ui
import math

# Initialize PyAudio
p = pyaudio.PyAudio()

# Define the format and channels
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# Create an overlay window
hwnd = win32gui.GetDesktopWindow()
hdc = win32gui.GetWindowDC(hwnd)
width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

# Define drawing parameters
sphere_radius = 100
arrow_length = 100
colors = {
    "front": (0, 255, 0),    # Green
    "rear": (255, 165, 0),   # Orange
    "left": (255, 0, 0),     # Red
    "right": (0, 0, 255),    # Blue
    "up": (255, 255, 0),     # Yellow
    "down": (0, 255, 255),   # Cyan
    "center": (192, 192, 192),# Grey
    "sphere": (0, 0, 0)      # Black
}

# Initialize smoothed values
smoothed_x = 0
smoothed_y = 0
smoothed_z = 0

# Define smoothing factor (between 0 and 1, where 1 means no smoothing)
smoothing_factor = 0.9

# Define the callback function
def callback(in_data, frame_count, time_info, status, *args):
    global smoothed_x, smoothed_y, smoothed_z
    try:
        audio_data = np.frombuffer(in_data, dtype=np.int16)
        left_channel = audio_data[0::2]
        right_channel = audio_data[1::2]
        
        left_intensity = np.mean(np.abs(left_channel))
        right_intensity = np.mean(np.abs(right_channel))
        
        # Simulate a front-rear channel and an up-down channel
        front_channel = (left_channel + right_channel) / 2
        rear_channel = front_channel * -1  # Invert the front channel to simulate the rear
        up_channel = front_channel * 0.5  # Simulate the up channel with lower intensity
        down_channel = front_channel * -0.5  # Simulate the down channel with lower inverted intensity
        
        front_intensity = np.mean(np.abs(front_channel))
        rear_intensity = np.mean(np.abs(rear_channel))
        up_intensity = np.mean(np.abs(up_channel))
        down_intensity = np.mean(np.abs(down_channel))
        
        x = (right_intensity - left_intensity) / max(left_intensity + right_intensity, 1)  # Avoid division by zero
        y = (front_intensity - rear_intensity) / max(front_intensity + rear_intensity, 1)  # Avoid division by zero
        z = (up_intensity - down_intensity) / max(up_intensity + down_intensity, 1)  # Avoid division by zero
        
        # Apply low-pass filter for smoothing
        smoothed_x = smoothed_x * smoothing_factor + x * (1 - smoothing_factor)
        smoothed_y = smoothed_y * smoothing_factor + y * (1 - smoothing_factor)
        smoothed_z = smoothed_z * smoothing_factor + z * (1 - smoothing_factor)
        
        # Calculate the 2D projection of the 3D vector
        projected_x = smoothed_x
        projected_y = smoothed_y - smoothed_z
        
        # Calculate the angle and radius for the arrow
        angle = math.atan2(projected_y, projected_x)
        radius = min(arrow_length, math.sqrt(projected_x ** 2 + projected_y ** 2) * arrow_length)
        
        # Clear previous drawings
        win32gui.InvalidateRect(hwnd, None, True)
        
        # Draw sphere
        hdcMem = win32ui.CreateDCFromHandle(hdc)
        brush = win32ui.CreateBrush(win32con.BS_SOLID, win32api.RGB(*colors["sphere"]), 0)
        old_brush = hdcMem.SelectObject(brush)
        hdcMem.Ellipse((width // 2 - sphere_radius, height // 2 - sphere_radius, width // 2 + sphere_radius, height // 2 + sphere_radius))
        
        # Determine the color based on direction
        if smoothed_x > 0.5:
            color = colors["right"]
        elif smoothed_x < -0.5:
            color = colors["left"]
        elif smoothed_y > 0.5:
            color = colors["front"]
        elif smoothed_y < -0.5:
            color = colors["rear"]
        elif smoothed_z > 0.5:
            color = colors["up"]
        elif smoothed_z < -0.5:
            color = colors["down"]
        else:
            color = colors["center"]
        
        # Draw arrow
        arrow_x = width // 2 + radius * math.cos(angle)
        arrow_y = height // 2 - radius * math.sin(angle)
        
        pen = win32ui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(*color))
        old_pen = hdcMem.SelectObject(pen)
        hdcMem.MoveTo((width // 2, height // 2))
        hdcMem.LineTo((int(arrow_x), int(arrow_y)))
        
        # Release resources
        hdcMem.SelectObject(old_pen)
        hdcMem.SelectObject(old_brush)
        win32ui.DeleteObject(pen.GetSafeHandle())
        win32ui.DeleteObject(brush.GetSafeHandle())
        hdcMem.DeleteDC()
        
    except Exception as e:
        print("Error in callback:", e)
    
    return (None, pyaudio.paContinue)

# Open stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                stream_callback=callback)

# Start the stream
stream.start_stream()

# Keep the script running
try:
    while stream is not None and stream.is_active():
        pass
except KeyboardInterrupt:
    pass

# Stop and close the stream
if stream is not None:
    stream.stop_stream()
    stream.close()

# Release the device context
win32gui.ReleaseDC(hwnd, hdc)

# Terminate PyAudio
p.terminate()
