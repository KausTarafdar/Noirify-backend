
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import cv2

def process_frame(frame):
    """Convert a single frame to grayscale."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def video_to_bw(input_video_path: str, output_video_path: str) -> None:
    """
    Converts a video to black and white while preserving the original audio.

    Args:
        input_video_path (str): Path to the input video file.
        output_video_path (str): Path to save the final black-and-white video with audio.

    Raises:
        FileNotFoundError: If the input video does not exist.
        RuntimeError: If video or audio processing fails.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"Input video file '{input_video_path}' not found.")

    temp_bw_video_path = f"{output_video_path}_temp.mp4"
    temp_audio_path = f"{output_video_path}_audio.aac"

    try:
        extract_audio_command = [
            "ffmpeg", "-y", "-i", input_video_path, "-q:a", "0", "-map", "a", temp_audio_path
        ]
        subprocess.run(extract_audio_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video file for processing.")

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_bw_video_path, fourcc, fps, (frame_width, frame_height), isColor=False)

    def process_frame(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    try:
        with ThreadPoolExecutor() as executor:
            while True:
                frames = []
                for _ in range(10):
                    ret, frame = cap.read()
                    if not ret:
                        break
                    frames.append(frame)

                if not frames:
                    break

                gray_frames = list(executor.map(process_frame, frames))
                for gray_frame in gray_frames:
                    out.write(gray_frame)
    finally:
        cap.release()
        out.release()

    # Merge audio and video using FFmpeg
    try:
        merge_command = [
            "ffmpeg", "-y", "-i", temp_bw_video_path, "-i", temp_audio_path,
            "-c:v", "copy", "-c:a", "aac", output_video_path
        ]
        subprocess.run(merge_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to merge audio with video: {e.stderr.decode()}")

    os.remove(temp_bw_video_path)
    os.remove(temp_audio_path)

    return output_video_path
