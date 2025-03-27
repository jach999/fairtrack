import argparse
import os
from ultralytics import YOLO
import numpy as np
import supervision as sv
from supervision.draw.color import ColorPalette
from bytetrack_matching import detections2boxes, match_detections_with_tracks, BYTETrackerArgs
from ByteTrack.yolox.tracker.byte_tracker import BYTETracker
import polygons.fdV2_5_polygons
from polygons.fdV2_5_polygons import fd1, fd2, fd3, fd4
import csv
from supervision.draw.utils import draw_polygon

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
    parser.add_argument("source_file", help="Path to the source video file")
    parser.add_argument("target_file", nargs="?", default=None, help="Path to save the tracked video")
    parser.add_argument("--device", choices=["fd1", "fd2", "fd3", "fd4"], default="fd1",
                        help="Select the device (fd1, fd2, fd3, fd4)")
    parser.add_argument("--model", choices=["1_class", "3_class", "39_class"], default="1_class",
                        help="Select the AI-model type (1, 2, or 39 classes)")
    parser.add_argument("--conf", type=float, default=0.5,
                        help="Detection confidence threshold (a float between 0.1 and 0.9)")
    args = parser.parse_args()

    # Validate the range for --conf
    if not (0.1 <= args.conf <= 0.9):
        parser.error("--conf must be a float between 0.1 and 0.9")

    return args

if __name__ == "__main__":
    args = parse_args()
    detection_conf = args.conf  # Assign the confidence threshold to a variable

# Set default target video path if not provided
    if args.target_file is None:

         # Extract the filename from the source video path
        source_file_filename = os.path.basename(args.source_file)

        # Remove the file extension (e.g., ".mp4") if present
        source_file_name, _ = os.path.splitext(source_file_filename)
                                                 
        args.target_file = os.path.join(HOME, new_run_folder_path, f"{source_file_name}_test.mp4")
    else:
        # If a target video path is provided, use it directly
        args.target_file = os.path.abspath(args.target_file)

# Define SOURCE_FILE_PATH and TARGET_FILE_PATH        
SOURCE_FILE_PATH = os.path.abspath(args.source_file)
TARGET_FILE_PATH = args.target_file

# Extract the filename from the target image path Remove the file extension  if present
target_file_filename = os.path.basename(TARGET_FILE_PATH)
target_file_name, _ = os.path.splitext(target_file_filename)
# Folder target directory
target_directory = os.path.dirname(TARGET_FILE_PATH)


selected_device = args.device

if args.model == "1_class":
    model_path = "1_class/best.pt"
    class_number = 1
elif args.model == "3_class":
    model_path = "3_class/best.pt"
elif args.model == "39_class":
    model_path = "39_class/best.pt"
        
# Make a path for a .csv file of the event
path = os.path.join(HOME, target_directory, f"{target_file_name}_log.csv")

model = YOLO(f"{HOME}/models/{model_path}")
model.fuse()

CLASS_NAMES_DICT = model.model.names

# create BYTETracker instance
byte_tracker = BYTETracker(BYTETrackerArgs())

# Extract width and height from video
video_info = sv.VideoInfo.from_video_path(SOURCE_FILE_PATH)
video_width = video_info.width
video_height = video_info.height

scaled_polygon1 = polygons.fdV2_5_polygons.normalized_polygon1 * np.array([video_width, video_height])
#scaled_polygon2 = polygons.fdV2_5_polygons.normalized_polygon2 * np.array([video_width, video_height])
scaled_polygon3 = polygons.fdV2_5_polygons.normalized_polygon3 * np.array([video_width, video_height])
scaled_polygon4 = polygons.fdV2_5_polygons.normalized_polygon4 * np.array([video_width, video_height])

# Extract the shift values
vertical_shift_value = getattr(locals()[selected_device], "vertical_shift", None)
horizontal_shift_value = getattr(locals()[selected_device], "horizontal_shift", None)

scaled_polygon1_shifted = scaled_polygon1 + [horizontal_shift_value, vertical_shift_value]
#scaled_polygon2_shifted = scaled_polygon2 + [horizontal_shift_value, vertical_shift_value]
scaled_polygon3_shifted = scaled_polygon3 + [horizontal_shift_value, 0]

entrance_polygon = scaled_polygon1_shifted
#inside_polygon1 = np.concatenate([scaled_polygon2_shifted, scaled_polygon1_shifted[::-1]])
#inside_polygon2 = np.concatenate([scaled_polygon3_shifted, scaled_polygon2_shifted[::-1]])
inside_polygon = np.concatenate([scaled_polygon3_shifted, scaled_polygon1_shifted[::-1]])
exit_polygon = np.concatenate([scaled_polygon4, scaled_polygon3_shifted[::-1]])

# Convert each polygon in the list to np.int32 data type
device_polygons = [polygon.astype(np.int32) for polygon in [exit_polygon, inside_polygon, entrance_polygon]]

colors = sv.ColorPalette.default()

zones = [
    sv.PolygonZone(
        polygon=polygon,
        frame_resolution_wh=video_info.resolution_wh
    )
    for polygon
    in device_polygons
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
    in range(len(device_polygons))
]


# Collect data for CSV
csv_data = []

#define polygons shapes
entrance_polygon_shape = entrance_polygon.shape
inside_polygon_shape = inside_polygon.shape
exit_polygon_shape = exit_polygon.shape


def process_frame(frame: np.ndarray, i: int) -> np.ndarray:
    print('frame', i)

    # Model prediction on a single frame and conversion to supervision Detections
    results = model(frame, imgsz=(video_width, video_height))
    boxes = results[0].boxes

    xyxy = boxes.xyxy.cpu().numpy()
    confidence = boxes.conf.cpu().numpy()
    class_id = boxes.cls.cpu().numpy().astype(int)

    detections = sv.Detections(xyxy=xyxy, confidence=confidence, class_id=class_id)

    # Conditional filtering based on the model used
    if args.model == "1_class":
        # For 1-class model, filter by class_number
        detections = detections[(detections.class_id == class_number) & (detections.confidence > detection_conf)]
    else:
        # For 3-class and 39-class models, process all detections with confidence > 0.5
        detections = detections[detections.confidence > detection_conf]

    # Tracking detections
    tracks = byte_tracker.update(
        output_results=detections2boxes(detections=detections),
        img_info=frame.shape,
        img_size=frame.shape
    )
    tracker_id = match_detections_with_tracks(detections=detections, tracks=tracks)
    detections.tracker_id = np.array(tracker_id)

    # Filtering out detections without trackers
    valid_tracks_mask = np.array([tid is not None for tid in detections.tracker_id], dtype=bool)
    detections.filter(mask=valid_tracks_mask, inplace=True)

    # Annotate the frame with zone polygons
    for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
        # Draw zone polygon
        frame = draw_polygon(
            scene=frame,
            polygon=zone.polygon,
            color=zone_annotator.color,
            thickness=zone_annotator.thickness
        )

        # Trigger detections in the specified polygon zone
        zone_mask = zone.trigger(detections=detections)
        detections_filtered = detections[zone_mask]

        if len(detections_filtered) == 0:
            continue  # Skip if no detections in this zone

        labels = []
        class_ids = detections_filtered.class_id.astype(int)
        tracker_ids = detections_filtered.tracker_id
        confidences = detections_filtered.confidence

        # Determine zone name once per zone
        polygon_shape = zone.polygon.shape
        if np.array_equal(polygon_shape, entrance_polygon_shape):
            zone_name = "Entrance"
        elif np.array_equal(polygon_shape, inside_polygon_shape):
            zone_name = "Inside"
        elif np.array_equal(polygon_shape, exit_polygon_shape):
            zone_name = "Exit"
        else:
            zone_name = "Unknown"

        # Generate labels and collect CSV data
        for idx in range(len(detections_filtered)):
            class_id = class_ids[idx]
            tracker_id = int(tracker_ids[idx]) if tracker_ids[idx] is not None else None
            conf = confidences[idx]
            bbox = detections_filtered.xyxy[idx]

            class_name = CLASS_NAMES_DICT.get(class_id, f"Class {class_id}")
            label = f"#{tracker_id} {class_name} {conf:.2f} {zone_name}"
            labels.append(label)
            csv_data.append([i, tracker_id, class_name, zone_name, conf, bbox])
            print(f"{class_name} #{tracker_id} detected in {zone_name} polygon")

        # Annotate the frame
        frame = box_annotator.annotate(scene=frame, detections=detections_filtered, labels=labels)

    return frame



    # Write data to CSV
    with open(path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)
       

    return frame

sv.process_video(source_path=SOURCE_FILE_PATH, target_path=TARGET_FILE_PATH, callback=process_frame)

print(f"Data written to {target_directory}")