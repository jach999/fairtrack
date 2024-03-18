* * *

Fairtrack: Insect Monitoring with the FAIR-Device
=================================================

<img src="https://raw.githubusercontent.com/jach999/fairtrack/main/assets/fair-d_scheme.png" width="500">

Overview
--------

**Fairtrack** is a project focused on developing an insect tracking system for the **Field Automatic Insect Recognizer-Device (FAIR-Device**). This script builds upon two different scripts from the same developer (see credits below). I’ve customized these algorithms for insect tracking inside the FAIR-Device.

### FAIR-Device

The **FAIR-Device** is a developing system for non-lethal insect field monitoring. Its goal is to offer researchers a cost-effective monitoring system that allows harmlessly and with high temporal resolution to identify and count insects on the field.

Key Features
------------
*   **Insect Detection**: Utilizes YoloV8 for real-time insect detection in video frames.
*   **Object Tracking**: Bytetrack ensures smooth tracking of detected insects across frames.
*   **Polygon Zones**: Define custom polygonal zones (entrance, inside, exit) for targeted monitoring.
*   **CSV Logging**: Logs relevant data (frame Nr, tracker IDs, class IDs, polygon zone, confidence scores) for analysis.

Next-Step Goals
---------------

1.  **Algorithm Refinement**:
    
    *   Improve the accuracy of the insect recognition model by extending the annotated image database.
    *   Refine the code to improve the integration between the detection system and the tracking system.
2.  **Analyzer Script Development**:
    
    *   Address data inconsistencies in the _log.csv file_ generated during tracking.
    *   Develop a metadata post-processing and analysis script to interpret insect entry and exit times and directions based on polygon activation.
3.  **Integration with iNaturalist**:
    
    *   Extract high-confidence images from detected insects for uploading to the iNaturalist platform and perform taxonomic classification of insects. 
    *   Utilize the iNaturalist API for automatic uploading the images. 
4.  **Real time monitoring**:
    
    * Implement camera live-streaming for real time operation.  

Installation
------------

1.  Clone this repository:
    
    git clone https://github.com/yourusername/FAIR-Device.git
        cd FAIR-Device
    
2.  Set up the environment (Python 3.7+ recommended):
    
    pip install -r requirements.txt

    
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

python fairtrack_test_video.py test_assets\fdV2_5\11-17-18.mp4 --device fd1

<img src="https://raw.githubusercontent.com/jach999/fairtrack/main/assets/11-17-18_test.gif"  width="500">

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

This project builds upon the work of [SkalskiP](https://github.com/SkalskiP). Specifically, we combined two of their insightful scripts:

1.  **[how-to-track-and-count-vehicles-with-yolov8](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-track-and-count-vehicles-with-yolov8.ipynb)**: This script leverages Bytetrack for vehicle tracking using YoloV8.
2.  **[how-to-detect-and-count-objects-in-polygon-zone](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-detect-and-count-objects-in-polygon-zone.ipynb)**: Here, Supervision is used for detecting and counting objects within polygonal zones.

We appreciate [SkalskiP](https://github.com/SkalskiP)’s valuable contributions to the field, which inspired this work.


Get Involved
------------

*   **Contributors**: Join us if you’re passionate about entomology, computer vision, or open-source development.
*   **Feedback**: We welcome your ideas and suggestions.

Stay tuned as we continue refining and expanding the **Fairtrack** project. Together, let’s uncover the hidden lives of insects! 🌟🐜

* * *

