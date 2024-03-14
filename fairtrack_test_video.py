import argparse
import os
from ultralytics import YOLO
import numpy as np
import supervision as sv
from supervision.draw.color import ColorPalette
from bytetracker import detections2boxes, match_detections_with_tracks, BYTETrackerArgs
from ByteTrack.yolox.tracker.byte_tracker import BYTETracker
import polygons.fdV2_5_polygons
from polygons.fdV2_5_polygons import fd1, fd2, fd3, fd4
import csv

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

HOME = os.path.dirname(__file__)

print(HOME)

# Specify the base directory where you want to create the new folders
base_run_directory = "runs"

# Determine the next folder name (e.g., "run1", "run2", etc.)
existing_run_folders = [folder for folder in os.listdir(base_run_directory) if folder.startswith("run")]
next_run_number = len(existing_run_folders) + 1
new_run_folder_name = f"run{next_run_number}"

# Create the new folder
new_run_folder_path = os.path.join(base_run_directory, new_run_folder_name)
os.makedirs(new_run_folder_path, exist_ok=True)

def parse_args():
    parser = argparse.ArgumentParser(description="Insect Tracking Script")
    parser.add_argument("source_video", help="Path to the source video file")
    parser.add_argument("target_video", nargs="?", default=None, help="Path to save the tracked video)")
    parser.add_argument("--device", choices=["fd1", "fd2", "fd3", "fd4"], default="fd1",
                        help="Select the device (fd1, fd2, fd3, fd4)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

# Set default target video path if not provided
    if args.target_video is None:

         # Extract the filename from the source video path
        source_video_filename = os.path.basename(args.source_video)

        # Remove the file extension (e.g., ".mp4") if present
        source_video_name, _ = os.path.splitext(source_video_filename)
                                                 
        args.target_video = os.path.join(HOME, new_run_folder_path, f"{source_video_name}_test.mp4")

    SOURCE_VIDEO_PATH = args.source_video
    TARGET_VIDEO_PATH = args.target_video

selected_device = args.device

# Make a path for a .csv file of the event
path = os.path.join(HOME, new_run_folder_path, f"{source_video_name}_test_log.csv")

model = YOLO(f"{HOME}/weights/1_class/best.pt")
model.fuse()

CLASS_NAMES_DICT = model.model.names

# create BYTETracker instance
byte_tracker = BYTETracker(BYTETrackerArgs())

# Folder target directory
target_directory = os.path.dirname(TARGET_VIDEO_PATH)

# Extract width and height from video
video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
video_width = video_info.width
video_height = video_info.height

scaled_polygon1 = polygons.fdV2_5_polygons.normalized_polygon1 * np.array([video_width, video_height])
scaled_polygon2 = polygons.fdV2_5_polygons.normalized_polygon2 * np.array([video_width, video_height])
scaled_polygon3 = polygons.fdV2_5_polygons.normalized_polygon3 * np.array([video_width, video_height])
scaled_polygon4 = polygons.fdV2_5_polygons.normalized_polygon4 * np.array([video_width, video_height])

# Extract the shift values
vertical_shift_value = getattr(locals()[selected_device], "vertical_shift", None)
horizontal_shift_value = getattr(locals()[selected_device], "horizontal_shift", None)

scaled_polygon1_shifted = scaled_polygon1 + [horizontal_shift_value, vertical_shift_value]
scaled_polygon2_shifted = scaled_polygon2 + [horizontal_shift_value, vertical_shift_value]
scaled_polygon3_shifted = scaled_polygon3 + [horizontal_shift_value, 0]

entrance_polygon = scaled_polygon1_shifted
inside_polygon1 = np.concatenate([scaled_polygon2_shifted, scaled_polygon1_shifted[::-1]])
inside_polygon2 = np.concatenate([scaled_polygon3_shifted, scaled_polygon2_shifted[::-1]])
exit_polygon = np.concatenate([scaled_polygon4, scaled_polygon3_shifted[::-1]])

# Convert each polygon in the list to np.int32 data type
polygons = [polygon.astype(np.int32) for polygon in [entrance_polygon, inside_polygon1, inside_polygon2, exit_polygon]]

colors = sv.ColorPalette.default()

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

# loop over video frames
def process_frame(frame: np.ndarray, i: int) -> np.ndarray:
    #print('frame', i)
 
    # model prediction on single frame and conversion to supervision Detections
    results = model(frame, imgsz=(video_width, video_height))
    xyxy = results[0].boxes.xyxy.cpu().numpy()
    confidence = results[0].boxes.conf.cpu().numpy()
    class_id = results[0].boxes.cls.cpu().numpy().astype(int)

    detections = sv.Detections(xyxy, confidence, class_id)
    detections = detections[(detections.class_id == 1) & (detections.confidence > 0.6)]

    # tracking detections
    tracks = byte_tracker.update(
    output_results=detections2boxes(detections=detections),
    img_info=frame.shape,
    img_size=frame.shape
        )
    tracker_id = match_detections_with_tracks(detections=detections, tracks=tracks)
    detections.tracker_id = np.array(tracker_id)

   
    for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
        
        # filtering out detections without trackers
        mask = np.array([tracker_id is not None for tracker_id in detections.tracker_id], dtype=bool)
        detections.filter(mask=mask, inplace=True)
        # specified polygon zone trigger
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
   
    # Open the CSV file in write mode
    with open(path, 'a', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)
        # Write a row with the data
        writer.writerow([args.source_video, tracker_id, class_id, confidence, xyxy])
        print(f"Data written to {path}")

    return frame

sv.process_video(source_path=SOURCE_VIDEO_PATH, target_path=TARGET_VIDEO_PATH, callback=process_frame)
