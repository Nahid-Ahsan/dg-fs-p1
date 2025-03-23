import gradio as gr
import subprocess
import os


def face_swap(image, videos, output_dir):
    outputs = []

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    for video in videos:
        video_name = os.path.basename(video)
        output_video = os.path.join(output_dir, f"swapped_{video_name}")

        command = [
            "python", "run.py",
            "-s", image,
            "-t", video,
            "-o", output_video,
            "--frame-processor", "face_swapper",
            "--keep-fps",
            "--skip-audio",
            "--many-faces",
            "--temp-frame-format", "png",
            "--output-video-quality", "35",
            "--execution-provider", "cpu",
            "--execution-threads", "4"
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
        gr.Image(type="filepath", label="Input Face Image"),
        gr.File(file_count="multiple", file_types=["video"], label="Input Videos"),
        gr.Textbox(label="Output Directory", placeholder="Enter path to save swapped videos")
    ],
    outputs=gr.Textbox(label="Processing Results"),
    title="Batch Video Face Swapper",
    description="Upload one face image and multiple videos. Outputs saved to specified directory."
)

iface.launch(debug=True)
