# Automation - M2RS

This Python application converts a video file into multiple Instagram-style reels, complete with text overlays for movie titles and part numbers. The application uses Tkinter for the graphical user interface (GUI) and FFmpeg for video processing.

## Features
- Split a movie into reels of specified duration.
- Add custom top and bottom text overlays.
- Automatically resize and pad videos to a 9:16 aspect ratio.
- Simple GUI for user interaction.

## Requirements
- Python 3.x
- FFmpeg installed and available in the system PATH.
- Required Python packages:
  - `opencv-python`
  - `tkinter`

## How to Use

### Step 1: Install Dependencies
Install the required Python packages:
```bash
pip install opencv-python
```

Ensure FFmpeg is installed on your system. You can download it from [FFmpeg's official website](https://ffmpeg.org/) and add it to your PATH.

### Step 2: Run the Application
Execute the script:
```bash
python movie_to_reel_converter.py
```

### Step 3: Use the GUI
1. **Select Video File:** Browse and select the video file you want to convert.
2. **Select Output Folder:** Choose a directory to save the generated reels.
3. **Enter Movie Name:** Provide the title of the movie to appear as the top text overlay.
4. **Set Reel Duration:** Specify the duration (in seconds) for each reel.
5. **Generate Reels:** Click the "Generate Reels" button to start processing.

### Output
The application generates reels in the specified output folder with the following naming convention:
```
reel_part_1.mp4
reel_part_2.mp4
...
```
Each reel includes:
- Top text: The movie name.
- Bottom text: Part number.

## Code Structure
### Key Functions
- **`add_text_overlay`:** Adds text overlays to the video.
- **`create_reels`:** Splits the video into parts and applies the required formatting and overlays.
- **`select_input_file`:** Opens a file dialog for selecting the video.
- **`select_output_folder`:** Opens a dialog to choose the output folder.
- **`start_processing`:** Validates inputs and initiates reel generation.

### GUI Design
The GUI is built using Tkinter, featuring:
- Input fields for video file, output folder, movie name, and reel duration.
- Buttons for file/folder selection and processing.
- Informative error and success messages.

## Troubleshooting
### Common Issues
- **FFmpeg not found:** Ensure FFmpeg is installed and added to the system PATH.
- **Invalid video file:** Use supported formats such as `.mp4`, `.mkv`, or `.avi`.
- **Reel duration not a number:** Enter a valid numeric value for the duration.

### Logs
Console logs provide progress updates and error messages to help debug issues.

## License
This project is open-source and available under the MIT License.

## Acknowledgments
- FFmpeg: For video processing capabilities.
- OpenCV: For adding text overlays to frames.

---

Feel free to customize the script and adapt it for your needs!

