import cv2 as cv
import numpy as np
import argparse

if __name__ != "__main__":
    exit()

parser = argparse.ArgumentParser("swap_time_space")
parser.add_argument("input", help="Video file to be transformed", type=str)
parser.add_argument("output", help="Output filename", type=str)
parser.add_argument("video_width", help="Maximum width of the output", type=int)
args = parser.parse_args()

cap = cv.VideoCapture(args.input)
if not cap.isOpened():
    print("invalid input file name")
    exit()

frame_dim = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
video_width = min(args.video_width, int(cap.get(cv.CAP_PROP_FRAME_COUNT)))
out_frames = list(
    map(lambda x: np.ndarray((frame_dim[0], video_width, 3), np.uint8), 
    range(frame_dim[1]))
)

def update_frames(frame, num):
    for x in range(frame.shape[1]):
        out_frame = out_frames[x]
        out_frame[:,num,:] = frame[:,x,:]

for i in range(video_width):
    ret, frame = cap.read()
    if not ret:
        break
    update_frames(frame, i)

out = cv.VideoWriter(args.output, cv.VideoWriter_fourcc(*'XVID'), 20, (video_width, frame_dim[0]), True)
for frame in out_frames:
    out.write(frame)

out.release()