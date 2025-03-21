#!/usr/bin/env python3

from roop import core

if __name__ == '__main__':
    core.run()


#  python run.py -s image.jpg -t target_video.mp4 -o output.mp4 --frame-processor face_swapper --keep-fps --skip-audio --many-faces --temp-frame-format png --output-video-quality 35 --execution-provider cpu --execution-threads 4