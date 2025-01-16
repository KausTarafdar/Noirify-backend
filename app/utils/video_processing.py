import os
from pathlib import Path
import subprocess
import uuid
import cv2

BASE_DIR = Path(__file__).parents[2]
UPLOAD_DIR = "uploads"

async def video_to_bw(input_video_path: str, output_video_path: str) -> str:
    """
    Converts a video to black and white while preserving the original audio.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Input video file '{input_video_path}' not found.")

    try:
        # Ensure the output path is unique
        if os.path.exists(output_video_path):
            output_video_path = f"{os.path.splitext(output_video_path)[0]}_{uuid.uuid4().hex}.mp4"

        # Extract audio
        temp_audio_path = f"{output_video_path}_audio.aac"
        extract_audio_command = [
            "ffmpeg", "-y", "-i", input_video_path, "-q:a", "0", "-map", "a", temp_audio_path
        ]
        subprocess.run(extract_audio_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        # Process video to grayscale
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise RuntimeError("Failed to open video file for processing.")

        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height), isColor=False)

        def process_frame(frame):
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray_frame = process_frame(frame)
            out.write(gray_frame)

        cap.release()
        out.release()

        # Merge audio and video
        final_out_video_path = f"{os.path.splitext(output_video_path)[0]}_bw_{uuid.uuid4().hex[:6]}.mp4"
        merge_command = [
            "ffmpeg", "-y", "-i", output_video_path, "-i", temp_audio_path,
            "-c:v", "copy", "-c:a", "aac", "-vcodec", "libx264",
            final_out_video_path
        ]
        subprocess.run(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

        os.remove(temp_audio_path)
        os.remove(output_video_path)

        return final_out_video_path

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg command failed: {e.stderr.decode()}")

    except Exception as e:
        raise RuntimeError(f"An error occurred: {str(e)}")