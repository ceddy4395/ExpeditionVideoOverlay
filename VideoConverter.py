import math
import os
import sys

import cv2
import pandas as pd


def read_csv_file(csv_path):
    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        exit(1)

    df = df[(df['Lat'].notna()) & (df['Lon'].notna())]

    try:
        df['Utc'] = pd.to_datetime(df['Utc'], unit='d', origin='1899-12-30')
    except Exception as e:
        print(f"Error converting 'Utc' to datetime: {e}")
        exit(1)

    return df


data = read_csv_file(os.getenv("CSV_FILE"))
video_path = os.getenv("VIDEO_FILE")


def add_data_to_video(_video_path, _data):
    cap = cv2.VideoCapture(_video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a VideoWriter object to save the output video
    out = cv2.VideoWriter('output_video.mp4', fourcc, fps, (width, height))

    frame_index = 0
    sys.stdout.write(f"Processed {frame_index} / {frame_count}")
    sys.stdout.flush()
    while cap.isOpened() and frame_index <= frame_count:
        ret, frame = cap.read()
        if not ret:
            break

        def put_text(text, org):
            cv2.putText(frame, text, org, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                        cv2.LINE_AA)
        second = math.floor(frame_index / fps)
        # Example: Overlay data from the DataFrame on the frame
        if second < len(_data):
            row_data = _data.iloc[second]
            put_text(f"UTC: {row_data['Utc']}", [int(0.02*width), int(0.05*height)])
            put_text(f"BSP: {row_data['BSP']}", [int(0.02*width), int(0.1*height)])
            put_text(f"TWA: {row_data['TWA']}", [int(0.02*width), int(0.15*height)])

        # Write the frame with the overlay to the output video
        out.write(frame)

        frame_index += 1
        sys.stdout.write(f"\rProcessed {frame_index} / {frame_count}")
        sys.stdout.flush()

    # Release the video objects
    cap.release()
    out.release()

if __name__ == '__main__':
    add_data_to_video(video_path, data)
