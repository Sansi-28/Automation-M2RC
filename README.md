# Automation-M2RC

A Python-based tool to convert movies into Instagram Reel-compatible videos with customizable text overlays and preserved audio. This tool allows users to split a movie into multiple reels, add top and bottom text, and ensure compatibility with Instagram's recommended dimensions.

## Features

- **Split Videos into Reels**: Automatically split input videos into segments of specified durations.
- **Text Overlays**: Add custom top and bottom text to each reel segment with centered alignment and outlined text for better visibility.
- **Audio Preservation**: Retain the original audio while processing the video.
- **Instagram Compatibility**: Ensure the video is resized and padded to 1080x1920 resolution.
- **User-Friendly UI**: Built using Tkinter for an intuitive graphical interface.
- **Error Handling**: Provides clear error messages for missing files or invalid inputs.
- **Temporary File Cleanup**: Automatically removes intermediate files after processing.

## Prerequisites

### Python Dependencies
Install the required Python libraries:
```bash
pip install pillow opencv-python-headless numpy

## Requirements

### Python Dependencies
Install the required Python libraries:
```bash
pip install pillow opencv-python-headless numpy
```

### External Tools
- **FFmpeg** and **FFprobe**: Required for video processing. Ensure they are installed and available in your system's PATH.
  - [Download FFmpeg](https://ffmpeg.org/download.html)

### Font File
A valid `.ttf` font file (e.g., `arial.ttf`) is needed for text overlays. The default font path in the code is `arial.ttf`.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Sansi-28/Automation-M2RC.git
   cd Automation-M2RC
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure `ffmpeg` and `ffprobe` are installed on your system and accessible from the command line.

---

## Usage

### Running the Application
1. Run the main script:
   ```bash
   python main.py
   ```

2. Use the graphical interface to:
   - Select a video file as the input.
   - Choose an output folder to save the reels.
   - Enter the movie name (displayed as top text).
   - Specify the reel duration (default is 80 seconds).

3. Click the "Generate Reels" button. The tool will:
   - Split the video into reels of the specified duration.
   - Resize and pad the video to 1080x1920 resolution.
   - Add text overlays for each segment.
   - Retain the original audio.

### Output
- The reels will be saved in the selected output folder.
- Each reel will include:
  - **Top text**: The movie name.
  - **Bottom text**: Reel part number (e.g., "Part 1").

---

## Example Workflow

1. Open the tool.
2. Select `movie.mp4` as the input video.
3. Choose an output folder (e.g., `./output/`).
4. Enter the movie name as `My Movie`.
5. Set the reel duration to `80` seconds.
6. Click **Generate Reels**.
7. The tool splits `movie.mp4` into multiple reels (e.g., `reel_part_1.mp4`, `reel_part_2.mp4`) and saves them in the `./output/` folder.

---

## Troubleshooting

1. **FFmpeg/FFprobe Not Found**:
   - Ensure FFmpeg is installed and added to your system's PATH. Test it by running `ffmpeg -version` in the terminal.

2. **Font Not Found**:
   - Make sure the `.ttf` font file exists and the `font_path` in the script points to it.

3. **Slow Processing**:
   - Video processing speed depends on your system's resources. For faster processing, ensure the system has sufficient RAM and CPU power.

---

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, please open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FFmpeg](https://ffmpeg.org/) for the powerful video processing tools.
- [Pillow](https://python-pillow.org/) for text and image manipulation.
- [OpenCV](https://opencv.org/) for video frame handling.
- The Python community for their excellent resources.