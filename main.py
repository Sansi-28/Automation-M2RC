import subprocess
import os
import math
import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np

def select_input_file(input_file_var):
    """Select input video file."""
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=(("Video Files", "*.mp4;*.mkv;*.avi"), ("All Files", "*.*"))
    )
    input_file_var.set(file_path)

def select_output_folder(output_folder_var):
    """Select output folder for reels."""
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder_path)

def add_audio_to_video(video_file, audio_file, output_file):
    """Combine video and audio with optimal encoding."""
    command = [
        "ffmpeg",
        "-i", video_file,
        "-i", audio_file,
        "-c:v", "libx264",  # Widely supported H.264 video codec
        "-preset", "medium",  # Balanced encoding quality
        "-profile:v", "baseline",  # Maximum compatibility
        "-level", "3.0",  # Broad device support
        "-c:a", "aac",  # AAC audio codec
        "-b:a", "128k",  # Standard audio bitrate
        "-movflags", "+faststart",  # Web optimization
        output_file
    ]
    subprocess.run(command, check=True)

def add_text_overlay_with_audio(input_file, output_file, top_text, bottom_text, width, height, font_path="arial.ttf", font_size=80):
    """Add text overlay while preserving original audio."""
    temp_video_file = "temp_video.mp4"
    temp_audio_file = "temp_audio.aac"

    # Extract audio
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-vn",
        "-acodec", "aac",
        "-b:a", "128k",
        temp_audio_file
    ], check=True)

    # Add text overlay
    add_text_overlay(input_file, temp_video_file, top_text, bottom_text, width, height, font_path, font_size)

    # Combine video and audio
    add_audio_to_video(temp_video_file, temp_audio_file, output_file)

    # Cleanup
    os.remove(temp_video_file)
    os.remove(temp_audio_file)

def add_text_overlay(input_file, output_file, top_text, bottom_text, width, height, font_path="arial.ttf", font_size=50):
    """Add text overlay to video frames."""
    cap = cv2.VideoCapture(input_file)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        messagebox.showerror("Error", f"Font file not found: {font_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)

        # Top text positioning with outline
        top_text_bbox = draw.textbbox((0, 0), top_text, font=font)
        top_text_width = top_text_bbox[2] - top_text_bbox[0]
        top_text_x = (width - top_text_width) // 2
        top_text_y = 350

        # Bottom text positioning with outline
        bottom_text_bbox = draw.textbbox((0, 0), bottom_text, font=font)
        bottom_text_width = bottom_text_bbox[2] - bottom_text_bbox[0]
        bottom_text_x = (width - bottom_text_width) // 2
        bottom_text_y = height - 425

        # Text outline effect
        outline_positions = [
            (top_text_x-2, top_text_y-2),
            (top_text_x+2, top_text_y-2),
            (top_text_x-2, top_text_y+2),
            (top_text_x+2, top_text_y+2)
        ]
        
        # Draw outline
        for pos in outline_positions:
            draw.text(pos, top_text, font=font, fill="black")
            draw.text(pos, bottom_text, font=font, fill="black")
        
        # Draw main text
        draw.text((top_text_x, top_text_y), top_text, font=font, fill="white")
        draw.text((bottom_text_x, bottom_text_y), bottom_text, font=font, fill="white")

        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        out.write(frame)

    cap.release()
    out.release()

def create_reels(input_file, output_folder, movie_name, reel_duration=80):
    """Generate Instagram Reels-compatible video clips."""
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Fetch video duration
        duration_output = subprocess.check_output([
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ]).decode().strip()
        total_duration = float(duration_output)
    except Exception as e:
        messagebox.showerror("Error", f"Could not fetch video duration: {e}")
        return

    # Instagram Reels recommended dimensions
    target_width = 1080
    target_height = 1920

    num_reels = math.ceil(total_duration / reel_duration)

    for i in range(num_reels):
        start_time = i * reel_duration
        temp_output_file = os.path.join(output_folder, f"temp_reel_part_{i + 1}.mp4")
        final_output_file = os.path.join(output_folder, f"reel_part_{i + 1}.mp4")

        # Universal 9:16 conversion command
             # Universal 9:16 conversion command without zooming
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(start_time),
            "-t", str(reel_duration),
            "-vf", (
                "scale=iw*min(1080/iw\\,1920/ih):ih*min(1080/iw\\,1920/ih),"  # Fit video inside 1080x1920
                "pad=1080:1920:(1080-iw*min(1080/iw\\,1920/ih))/2:(1920-ih*min(1080/iw\\,1920/ih))/2"  # Add padding
            ),
            "-c:v", "libx264",
            "-preset", "medium",
            "-profile:v", "baseline",
            "-level", "3.0",
            "-crf", "23",  # High-quality, reasonable file size
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            "-f", "mp4",
            temp_output_file
        ]


        try:
            subprocess.run(command, check=True, capture_output=True)

            # Add text overlay with audio preservation
            top_text = movie_name
            bottom_text = f"Part {i + 1}"
            add_text_overlay_with_audio(temp_output_file, final_output_file, top_text, bottom_text, target_width, target_height)

            os.remove(temp_output_file)  # Clean temporary files

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Reel generation failed: {e}")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
            return

    messagebox.showinfo("Success", "Reels generated successfully!")

def start_processing(input_file_var, output_folder_var, movie_name_var, reel_duration_var):
    """Process the reel generation based on UI inputs."""
    input_file = input_file_var.get()
    output_folder = output_folder_var.get()
    movie_name = movie_name_var.get()
    try:
        reel_duration = int(reel_duration_var.get())
    except ValueError:
        messagebox.showerror("Error", "Reel duration must be a number.")
        return

    if not input_file or not output_folder or not movie_name:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    create_reels(input_file, output_folder, movie_name, reel_duration)

# Tkinter UI Setup
root = tk.Tk()
root.title("Movie to Reel Converter")

# Input file
tk.Label(root, text="Select Video File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
input_file_var = tk.StringVar()
tk.Entry(root, textvariable=input_file_var, width=50).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_input_file(input_file_var)).grid(row=0, column=2, padx=10, pady=5)

# Output folder
tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: select_output_folder(output_folder_var)).grid(row=1, column=2, padx=10, pady=5)

# Movie name
tk.Label(root, text="Movie Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
movie_name_var = tk.StringVar()
tk.Entry(root, textvariable=movie_name_var, width=50).grid(row=2, column=1, padx=10, pady=5)

# Reel duration
tk.Label(root, text="Reel Duration (seconds):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
reel_duration_var = tk.StringVar(value="80")
tk.Entry(root, textvariable=reel_duration_var, width=20).grid(row=3, column=1, padx=10, pady=5)

# Start button
tk.Button(root, text="Generate Reels", 
          command=lambda: start_processing(input_file_var, output_folder_var, movie_name_var, reel_duration_var)
         ).grid(row=4, column=0, columnspan=3, pady=20)

root.mainloop()