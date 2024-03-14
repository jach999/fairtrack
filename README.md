* * *

Fairtrack, Insect Tracking and Polygon-Zone Detection for the FAIR-Device 
======================================================

<img src="https://raw.githubusercontent.com/jach999/fairtrack/main/assets/fair-d_scheme.png" width="500">

Welcome to the Fairtrack project! Our software combines various computer vision algorithms to track insects within the FAIR-Device, a non-lethal insect monitoring field-trap. Building upon the work of two scripts by SkalskiP (see credits), this project is still actively under construction.
--------

*   **Insect Detection**: Utilizes YoloV8 for real-time insect detection in video frames.
*   **Object Tracking**: Bytetrack ensures smooth tracking of detected insects across frames.
*   **Polygon Zones**: Define custom polygonal zones (entrance, inside, exit) for targeted monitoring.
*   **CSV Logging**: Logs relevant data (tracker IDs, class IDs, confidence scores) for analysis.

Installation
------------

1.  Clone this repository:
    
    git clone https://github.com/yourusername/FAIR-Device.git
        cd FAIR-Device
    
2.  Set up the environment (Python 3.7+ recommended):
    
    pip install -r requirements.txt
    
3.  Download YoloV8 weights (place them in the `weights` directory).
    

Usage
-----

1.  Run the video tracking script:
    
    python fairtrack_test_video.py path/to/source_video.mp4 [path/to/target_video.mp4]
    *   `source_video`: Path to the input video.
    *   `target_video` (optional): Path to save the tracked video (default: `runs/source_video_test.mp4`).
    *   `--device` (optional) you can specify the device used for the captured video (fd1, fd2, fd3 or fd4)
         this corrects some framing differences between devices
2.  Adjust polygon zones in `device_polygons.py`.
    
3.  View the tracked video and analyze the CSV log.
    

Example
-------

python fairtrack_test_video.py test_assets\fdV2_5\14-05-01.mp4 --device fd1

<img src="https://raw.githubusercontent.com/jach999/fairtrack/main/assets/14-05-01.jpg"  width="500">

Change Log
----------

*   **v1.0.0 (March 2024)**:
    *   Initial release.
    *   YoloV8 for insect detection.
    *   Bytetrack for tracking.
    *   Polygon zones defined.


Author
------

*   Juan A. Chiavassa
*   Email: juan.chiavassa.gmail.com


Credits
-------

This project builds upon the work of SkalskiP. Specifically, we combined two of their insightful scripts:

1.  **how-to-track-and-count-vehicles-with-yolov8.ipynb**: This script leverages Bytetrack for vehicle tracking using YoloV8.
2.  **how-to-detect-and-count-objects-in-polygon-zone.ipynb**: Here, Supervision is used for detecting and counting objects within polygonal zones.

We appreciate SkalskiP’s valuable contributions to the field, which inspired this work.

* * *