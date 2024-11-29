import subprocess
import os
import math
import cv2
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import numpy as np



def add_text_overlay(input_file, output_file, top_text, bottom_text, width, height, font_path="arial.ttf", font_size=50):
    cap = cv2.VideoCapture(input_file)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    # Load the font
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        messagebox.showerror("Error", f"Font file not found: {font_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame (OpenCV -> PIL)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        draw = ImageDraw.Draw(pil_image)

        # Add top text
        top_text_bbox = draw.textbbox((0, 0), top_text, font=font)
        top_text_width = top_text_bbox[2] - top_text_bbox[0]
        top_text_x = (width - top_text_width) // 2
        top_text_y = 300  # Top margin
        draw.text((top_text_x, top_text_y), top_text, font=font, fill="white")

        # Add bottom text
        bottom_text_bbox = draw.textbbox((0, 0), bottom_text, font=font)
        bottom_text_width = bottom_text_bbox[2] - bottom_text_bbox[0]
        bottom_text_x = (width - bottom_text_width) // 2
        bottom_text_y = height - 300  # Bottom margin
        draw.text((bottom_text_x, bottom_text_y), bottom_text, font=font, fill="white")

        # Convert the frame back (PIL -> OpenCV)
        frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

        out.write(frame)

    cap.release()
    out.release()



def create_reels(input_file, output_folder, movie_name, reel_duration=80):
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Get video duration
        duration_output = subprocess.check_output([
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            input_file
        ]).decode().strip()
        total_duration = float(duration_output)
        print(f"Total video duration: {total_duration:.2f} seconds")
    except Exception as e:
        print(f"Error fetching video duration: {e}")
        messagebox.showerror("Error", "Could not fetch video duration.")
        return

    num_reels = math.ceil(total_duration / reel_duration)

    for i in range(num_reels):
        start_time = i * reel_duration
        temp_output_file = os.path.join(output_folder, f"temp_reel_part_{i + 1}.mp4")
        final_output_file = os.path.join(output_folder, f"reel_part_{i + 1}.mp4")

        # Define the target 9:16 resolution
        target_width = 720  # Set width (you can adjust this)
        target_height = 1280  # Set height for 9:16 ratio

        # FFmpeg command to resize to 9:16 without zooming (padding to fit)
        command = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(start_time),
            "-t", str(reel_duration),
            "-vf", f"scale={target_width}:-1,pad={target_width}:{target_height}:0:(oh-ih)/2",  # Scale and pad
            "-c:v", "libx264",  # Video codec
            "-c:a", "aac",  # Audio codec
            "-strict", "experimental",  # To use AAC encoding
            temp_output_file
        ]

        print(f"Generating Reel {i + 1}/{num_reels}...")

        try:
            subprocess.run(command, check=True, capture_output=True)
            print(f"Temporary reel saved: {temp_output_file}")

            # Add text overlay
            top_text = movie_name
            bottom_text = f"Part {i + 1}"
            add_text_overlay(temp_output_file, final_output_file, top_text, bottom_text, target_width, target_height)

            os.remove(temp_output_file)  # Clean up temporary file
            print(f"Final reel saved: {final_output_file}")

        except subprocess.CalledProcessError as e:
            print(f"Error generating reel {i + 1}: {e}")
        except Exception as e:
            print(f"Error processing text overlay for reel {i + 1}: {e}")

    print("Reel generation completed!")
    messagebox.showinfo("Success", "Reel generation completed!")


def select_input_file():
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=(("Video Files", "*.mp4;*.mkv;*.avi"), ("All Files", "*.*"))
    )
    input_file_var.set(file_path)


def select_output_folder():
    folder_path = filedialog.askdirectory(title="Select Output Folder")
    output_folder_var.set(folder_path)


def start_processing():
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
tk.Button(root, text="Browse", command=select_input_file).grid(row=0, column=2, padx=10, pady=5)

# Output folder
tk.Label(root, text="Select Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
output_folder_var = tk.StringVar()
tk.Entry(root, textvariable=output_folder_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

# Movie name
tk.Label(root, text="Movie Name:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
movie_name_var = tk.StringVar()
tk.Entry(root, textvariable=movie_name_var, width=50).grid(row=2, column=1, padx=10, pady=5)

# Reel duration
tk.Label(root, text="Reel Duration (seconds):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
reel_duration_var = tk.StringVar(value="80")
tk.Entry(root, textvariable=reel_duration_var, width=20).grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Process button
tk.Button(root, text="Generate Reels", command=start_processing, bg="green", fg="white").grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
root.mainloop()
