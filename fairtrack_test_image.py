import argparse
import os
import sys
from ultralytics import YOLO
import numpy as np
import supervision as sv
import cv2
from supervision.draw.color import ColorPalette
from bytetracker import detections2boxes, match_detections_with_tracks, BYTETrackerArgs
from ByteTrack.yolox.tracker.byte_tracker import BYTETracker
from polygons.polygon1 import normalized_polygon1
from polygons.polygon2 import normalized_polygon2
from polygons.polygon3 import normalized_polygon3
from polygons.polygon4 import normalized_polygon4

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

HOME = os.path.dirname(__file__)

print(HOME)

def parse_args():
    parser = argparse.ArgumentParser(description="Insect Tracking Script")
    parser.add_argument("source_image", help="Path to the source video file")
    parser.add_argument("target_image", nargs="?", default=None, help="Path to save the tracked video)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

# Set default target image path if not provided
    if args.target_image is None:

         # Extract the filename from the source image path
        source_image_filename = os.path.basename(args.source_image)

        # Remove the file extension (e.g., ".jpg") if present
        source_image_name, _ = os.path.splitext(source_image_filename)
                                                 
        args.target_image = os.path.join(HOME, "runs", f"{source_image_name}_test.jpg")

    SOURCE_IMAGE_PATH = args.source_image
    TARGET_IMAGE_PATH = args.target_image


model = YOLO(f"{HOME}/weights/1_class/best.pt")
model.fuse()

CLASS_NAMES_DICT = model.model.names

# create BYTETracker instance
byte_tracker = BYTETracker(BYTETrackerArgs())

# Folder target directory
target_directory = os.path.dirname(TARGET_IMAGE_PATH)
image_size = cv2.imread(SOURCE_IMAGE_PATH)

# Get the height and width using numpy.shape
image_height, image_width, _ = image_size.shape

scaled_polygon1 = normalized_polygon1 * np.array([image_width, image_height])
scaled_polygon2 = normalized_polygon2 * np.array([image_width, image_height])
scaled_polygon3 = normalized_polygon3 * np.array([image_width, image_height])
scaled_polygon4 = normalized_polygon4 * np.array([image_width, image_height])

entrance_polygon = scaled_polygon1
inside_polygon1 = np.concatenate([scaled_polygon2, scaled_polygon1[::-1]])
inside_polygon2 = np.concatenate([scaled_polygon3, scaled_polygon2[::-1]])
exit_polygon = np.concatenate([scaled_polygon4, scaled_polygon3[::-1]])

# Convert each polygon in the list to np.int32 data type
polygons = [polygon.astype(np.int32) for polygon in [entrance_polygon, inside_polygon1, inside_polygon2, exit_polygon]]

#print(polygons)

colors = sv.ColorPalette.default()

video_info = sv.VideoInfo.from_video_path(SOURCE_IMAGE_PATH)
zones = [
    sv.PolygonZone(
        polygon=polygon,
        frame_resolution_wh=video_info.resolution_wh
    )
    for polygon
    in polygons
]
zone_annotators = [
    sv.PolygonZoneAnnotator(
        zone=zone,
        color=colors.by_idx(index),
        thickness=3,
        text_thickness=1,
        text_scale=0.5
    )
    for index, zone
    in enumerate(zones)
]
box_annotators = [
    sv.BoxAnnotator(
        color=colors.by_idx(index),
        thickness=1,
        text_thickness=1,
        text_scale=0.5
        )
    for index
    in range(len(polygons))
]

print(video_info)

# extract video frame
generator = sv.get_video_frames_generator(SOURCE_IMAGE_PATH)
iterator = iter(generator)
frame = next(iterator)

# model prediction on single frame and conversion to supervision Detections
results = model(frame)
xyxy = results[0].boxes.xyxy.cpu().numpy()
confidence = results[0].boxes.conf.cpu().numpy()
class_id = results[0].boxes.cls.cpu().numpy().astype(int)

detections = sv.Detections(xyxy, confidence, class_id)
detections = detections[(detections.class_id == 1) & (detections.confidence > 0.5)]
                        
# tracking detections
tracks = byte_tracker.update(
output_results=detections2boxes(detections=detections),
img_info=frame.shape,
img_size=frame.shape
)
tracker_id = match_detections_with_tracks(detections=detections, tracks=tracks)
detections.tracker_id = np.array(tracker_id)

for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
    mask = zone.trigger(detections=detections)
    detections_filtered = detections[mask]
    labels = [
            f"#{tracker_id} {CLASS_NAMES_DICT[class_id]} {confidence:0.2f}"
            for  _, confidence, class_id, tracker_id
            in detections
        ]
    frame = box_annotator.annotate(scene=frame, detections=detections_filtered, labels=labels)
    frame = zone_annotator.annotate(scene=frame)

print(tracker_id, class_id, confidence, xyxy)

# Save the frame as an image
output_image_path = os.path.join(target_directory, os.path.basename(TARGET_IMAGE_PATH))
cv2.imwrite(output_image_path, frame)

# Make a .csv file of the event
path = os.path.join(HOME, "runs", f"{source_image_name}_test_log.csv")

import csv
# Open the CSV file in write mode
with open(path, 'w', newline='') as csvfile:
    # Create a CSV writer
    writer = csv.writer(csvfile)

           # Write a row with the data
    writer.writerow([args.source_image, tracker_id, class_id, confidence, xyxy])

print(f"Data written to {path}")