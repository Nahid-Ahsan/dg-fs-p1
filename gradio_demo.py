import gradio as gr
import subprocess
import os
import shutil
from PIL import Image
import numpy as np

# Function to run face swap
def run_face_swap(input_image, target_video):
    # Create output folder if it doesn't exist
    output_folder = "output_videos"
    os.makedirs(output_folder, exist_ok=True)

    # Save the uploaded image to disk using PIL
    input_image_path = "input_image.jpg"
    image = Image.fromarray(input_image)  # Convert ndarray to PIL Image
    image.save(input_image_path)  # Save the image

    # Define the target video path
    target_video_path = target_video  # `target_video` is already a string path

    # Define output file path
    output_file = os.path.join(output_folder, "output.mp4")

    # Command to execute face swap
    command = [
        "python", "run.py",
        "-s", input_image_path,
        "-t", target_video_path,
        "-o", output_file,
        "--frame-processor", "face_swapper",
        "--keep-fps",
        "--skip-audio",
        "--many-faces",
        "--temp-frame-format", "png",
        "--output-video-quality", "35",
        "--execution-provider", "cpu",
        "--execution-threads", "4"
    ]

    # Run the command
    process = subprocess.run(command, capture_output=True, text=True)

    # Check if the process was successful
    if process.returncode == 0:
        return output_file
    else:
        return f"Error: {process.stderr}"

# Gradio UI setup
iface = gr.Interface(
    fn=run_face_swap,
    inputs=[
        gr.Image(label="Upload Face Image"),
        gr.Video(label="Upload Target Video")
    ],
    outputs=gr.Video(label="Output Video"),
    title="AI Face Swapper",
    description="Upload an image and a video to swap faces automatically."
)

# Run Gradio app
if __name__ == "__main__":
    iface.launch()
