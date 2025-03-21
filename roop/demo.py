import os
import sys
import gradio as gr
import shutil
import onnxruntime
import tensorflow
import globals
import metadata
from predictor import predict_image, predict_video
from processors.frame.core import get_frame_processors_modules
from utilities import (
    has_image_extension, is_image, is_video, detect_fps, create_video, extract_frames, 
    get_temp_frame_paths, restore_audio, create_temp, move_temp, clean_temp, normalize_output_path
)

def setup_environment():
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def process_media(source_path, target_path, output_path, frame_processor=['face_swapper'], keep_fps=False, keep_frames=False, skip_audio=False, many_faces=False):
    globals.source_path = source_path
    globals.target_path = target_path
    globals.output_path = normalize_output_path(source_path, target_path, output_path)
    globals.frame_processors = frame_processor
    globals.keep_fps = keep_fps
    globals.keep_frames = keep_frames
    globals.skip_audio = skip_audio
    globals.many_faces = many_faces
    
    for frame_processor in get_frame_processors_modules(globals.frame_processors):
        if not frame_processor.pre_start():
            return "Error: Frame processor pre-start failed."
    
    if has_image_extension(target_path):
        if predict_image(target_path):
            shutil.copy2(target_path, globals.output_path)
            for frame_processor in get_frame_processors_modules(globals.frame_processors):
                frame_processor.process_image(source_path, globals.output_path, globals.output_path)
                frame_processor.post_process()
            return globals.output_path if is_image(target_path) else "Processing to image failed."
    
    if predict_video(target_path):
        return "Error: Video processing failed."
    
    create_temp(target_path)
    fps = detect_fps(target_path) if keep_fps else 30
    extract_frames(target_path, fps)
    temp_frame_paths = get_temp_frame_paths(target_path)
    
    if not temp_frame_paths:
        return "Error: Frames not found."
    
    for frame_processor in get_frame_processors_modules(globals.frame_processors):
        frame_processor.process_video(source_path, temp_frame_paths)
        frame_processor.post_process()
    
    create_video(target_path, fps)
    if not skip_audio:
        restore_audio(target_path, globals.output_path)
    else:
        move_temp(target_path, globals.output_path)
    
    clean_temp(target_path)
    return globals.output_path if is_video(target_path) else "Processing to video failed."

def gradio_interface(source, target, output):
    output_file = process_media(source, target, output)
    return output_file

iface = gr.Interface(
    fn=gradio_interface,
    inputs=[gr.File(label="Source Image"), gr.File(label="Target Image/Video"), gr.Textbox(label="Output Path")],
    outputs=gr.File(label="Processed Output"),
    title="Roop AI Face Swapper Service",
    description="Upload a source image and a target image/video to perform AI-based face swapping."
)

if __name__ == "__main__":
    setup_environment()
    iface.launch()