import gradio as gr
import subprocess
import os

def face_swap(image, videos, output_dir="/output_folder"):
    outputs = []
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for video_file in videos:
        # video_file is a `_TemporaryFileWrapper`. Grab its name attribute:
        video_path = video_file.name
        video_name = os.path.basename(video_path)
        output_video = os.path.join(output_dir, f"swapped_{video_name}")

        command = [
            "python", "run.py",
            "-s", image,              # Here `image` is okay because gr.Image(type="filepath") returns a string path
            "-t", video_path,         # Pass the string path from video_file.name
            "-o", output_video,
            "--frame-processor", "face_swapper",
            "--keep-fps",
            "--skip-audio",
            "--many-faces",
            "--temp-frame-format", "png",
            "--output-video-quality", "35",
            "--execution-provider", "cpu",
            "--execution-threads", "8"
        ]

        try:
            subprocess.run(command, check=True)
            outputs.append(f"Success: {output_video}")
        except subprocess.CalledProcessError as e:
            outputs.append(f"Error processing {video_name}: {str(e)}")

    return "\n".join(outputs)


iface = gr.Interface(
    fn=face_swap,
    inputs=[
        # type="filepath" is fine for the image; it directly returns the image path as a string
        gr.Image(type="filepath", label="Input Face Image"),
        # This returns _TemporaryFileWrapper objects, so we use `.name` in the function
        gr.File(file_count="multiple", file_types=["video"], label="Input Videos"),
    ],
    outputs=gr.Textbox(label="Processing Results"),
    title="Batch Video Face Swapper",
    description="Upload one face image and multiple videos. Outputs saved to specified directory.",
    flagging_dir="/tmp/flagged",
)

iface.launch(debug=True)
