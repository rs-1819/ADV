# Audio Directional Visualization

This Python project visualizes the direction of audio input in real-time using PyAudio and Windows GDI. It displays an overlay window on the desktop, showing a sphere and an arrow indicating the direction of the audio source.

## Requirements

- Python 3.x
- PyAudio
- NumPy
- pywin32

## Installation

```
TODO
```

## Usage

Run the script to start the audio visualization:

```
python main.py
```

The script will open an overlay window on the desktop, displaying a sphere and an arrow. The arrow will point in the direction of the audio source based on the intensity differences between the left and right channels, as well as simulated front-rear and up-down channels.

To stop the visualization, press `Ctrl+C` in the terminal or close the Python process.

## How It Works

1. The script initializes PyAudio and sets up the audio format, channels, and rate.

2. It creates an overlay window using the Windows GDI functions provided by the `pywin32` library.

3. The `callback` function is defined as the stream callback for PyAudio. It is called whenever new audio data is available.

4. Inside the callback function:
   - The audio data is converted to a NumPy array.
   - The left and right channel intensities are calculated.
   - Simulated front-rear and up-down channels are created based on the left and right channels.
   - The intensities of the simulated channels are calculated.
   - The x, y, and z coordinates are determined based on the intensity differences between the channels.
   - A low-pass filter is applied to smooth the coordinates.
   - The 2D projection of the 3D vector is calculated.
   - The angle and radius for the arrow are determined based on the projected coordinates.
   - The previous drawings are cleared.
   - The sphere is drawn using Windows GDI functions.
   - The color of the arrow is determined based on the direction of the audio source.
   - The arrow is drawn using Windows GDI functions.

5. The script opens an audio stream with the specified format, channels, rate, and callback function.

6. The stream is started, and the script enters a loop to keep it running until interrupted.

7. When the script is stopped or interrupted, the stream is closed, the device context is released, and PyAudio is terminated.

## Customization

You can customize the visualization by modifying the following parameters in the script:

- `sphere_radius`: The radius of the sphere in pixels.
- `arrow_length`: The maximum length of the arrow in pixels.
- `colors`: A dictionary mapping directions to RGB color tuples.
- `smoothing_factor`: The smoothing factor for the low-pass filter (between 0 and 1, where 1 means no smoothing).

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- PyAudio: https://people.csail.mit.edu/hubert/pyaudio/
- pywin32: https://github.com/mhammond/pywin32

If you have any questions or suggestions, please open an issue or submit a pull request.
