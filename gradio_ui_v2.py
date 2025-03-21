import gradio as gr
import subprocess
import os
import shutil
from PIL import Image
import numpy as np

# Function to run face swap for a single video
def run_face_swap(input_image, target_video, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Save the uploaded image to disk
    input_image_path = os.path.join(output_folder, "input_image.jpg")
    image = Image.fromarray(input_image)  # Convert ndarray to PIL Image
    image.save(input_image_path)

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

    if process.returncode == 0:
        return output_file
    else:
        return f"Error: {process.stderr}"

# Function to run face swap for multiple videos
def run_face_swap_multiple(input_image, target_videos, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Save the uploaded image
    input_image_path = os.path.join(output_folder, "input_image.jpg")
    image = Image.fromarray(input_image)
    image.save(input_image_path)

    output_files = []
    for idx, target_video in enumerate(target_videos):
        # Define target video path
        target_video_path = target_video

        # Define output file path for each video
        output_file = os.path.join(output_folder, f"output_{idx+1}.mp4")

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

        if process.returncode == 0:
            output_files.append(output_file)
        else:
            output_files.append(f"Error processing {target_video}: {process.stderr}")

    return output_files

# Gradio UI setup
with gr.Blocks() as app:
    gr.Markdown("# 🎭 AI Face Swapper")

    with gr.Tab("Single Video Face Swap"):
        with gr.Row():
            image_input = gr.Image(label="Upload Face Image")
            video_input = gr.Video(label="Upload Target Video")
            output_folder_input = gr.Textbox(label="Output Folder Path", value="output_videos")

        run_button = gr.Button("Run Face Swap")
        output_video = gr.Video(label="Output Video")

        run_button.click(
            run_face_swap, 
            inputs=[image_input, video_input, output_folder_input], 
            outputs=output_video
        )

    with gr.Tab("Multiple Video Face Swap"):
        with gr.Row():
            multi_image_input = gr.Image(label="Upload Face Image")
            multi_video_input = gr.Files(label="Upload Multiple Target Videos", file_types=[".mp4"])  # Fixed Here
            multi_output_folder_input = gr.Textbox(label="Output Folder Path", value="output_videos")

        multi_run_button = gr.Button("Run Face Swap for All Videos")
        output_videos = gr.File(label="Processed Videos")

        multi_run_button.click(
            run_face_swap_multiple, 
            inputs=[multi_image_input, multi_video_input, multi_output_folder_input], 
            outputs=output_videos
        )

# Launch the Gradio app
if __name__ == "__main__":
    app.launch(share=True)
