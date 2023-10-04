import cv2
import numpy as np
import pyraw
import os 

def join_frames(frame1, frame2):
    # Create a new frame to hold the merged result
    merged_frame = np.maximum(frame1, frame2)
    return merged_frame

def get_filenames(directory_path):
    filenames = []
    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            filenames.append(filename)
    return filenames


directory_path = "D:\\Pulpit\\Detectron\\multiview_sequences\\L01\\15frames"
directory_path_bg = "D:\\Pulpit\\Detectron\\multiview_sequences\\L01\\15frames\\bg_d"
dest_path = "D:\\Pulpit\\Detectron\\multiview_sequences\\L01\\15frames\\full_depth"
filenames_p = get_filenames(directory_path)
filenames_bg = get_filenames(directory_path_bg)

full_path_p = []
full_path_bg = []

for filename in filenames_p:
        fp = os.path.join(directory_path, filename)
        full_path_p.append(fp)

for filename in filenames_bg:
        fp = os.path.join(directory_path_bg, filename)
        full_path_bg.append(fp)

for i in range(0, len(full_path_p)):
    NumFrames = pyraw.calcNumFramesInFile(1920, 1080, 16, pyraw.ePicType.YUV, 420, os.path.getsize(full_path_p[i]))
    ReaderBG = pyraw.xSeqYUV(1920, 1080, 16, 420)
    ReaderP = pyraw.xSeqYUV(1920, 1080, 16, 420)
    Writer = pyraw.xSeqYUV(1920, 1080, 16, 420)
    dest = os.path.join(dest_path, filenames_p[i])
    Writer.openFile(dest, pyraw.eMode.Write)
    ReaderBG.openFile(full_path_bg[i], pyraw.eMode.Read)
    ReaderP.openFile(full_path_p[i], pyraw.eMode.Read)
    BG_frame = ReaderBG.readPicYUV()
    for PicIdx in range(0, NumFrames):
         P_frame = ReaderP.readPicYUV()
         merged = join_frames(BG_frame, P_frame)
         Writer.writePicYUV(merged)
    Writer.closeFile()
    ReaderBG.closeFile()
    ReaderP.closeFile()


'''
# Ensure that both frame lists have the same length
num_frames = min(len(wp_frames), len(p_frames))
wp_frames = wp_frames[:num_frames]
p_frames = p_frames[:num_frames]

# Loop through the frames and merge them
for i in range(num_frames):
    merged_frame = join_frames(wp_frames[i], p_frames[i])

    # Write merged_frame into the output video
    full_depth.write(merged_frame)

# Release video capture and close output video writer
'''