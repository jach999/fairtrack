* * *

Fairtrack: Insect Monitoring with the FAIR-Device
=================================================
[![DOI bioRxiv](https://img.shields.io/badge/bioRxiv-10.1101%2F2024.03.22.586299-B31B1B)](https://doi.org/10.1101/2024.03.22.586299)
&nbsp;

<img src="https://raw.githubusercontent.com/jach999/fairtrack/master/assets/fair-d_scheme.png" width="700">

Overview
--------

**Fairtrack** is a project focused on developing an insect tracking system for the **Field Automatic Insect Recognizer-Device (FAIR-Device**). This script builds upon two different scripts from the same developer (see credits below). We have customized these algorithms for insect tracking inside the FAIR-Device.

### FAIR-Device

The **FAIR-Device** is a developing system designed for non-lethal insect field monitoring. Its primary objective is to provide researchers with a cost-effective monitoring solution for harmlessly identifying and counting insects in the field with high temporal resolution. Currently, this device is under development as part of the [Diabek](https://diabek.hswt.de/en/) project, which is one of the [14 digital trial fields](https://www.bmel.de/EN/topics/digitalisation/digital-trial-fields.html) funded by the [Federal Ministry of Food and Agriculture (BMEL)](https://www.bmel.de/EN/Home/home_node.html). The Diabek project aims to explore digital technologies for agriculture and evaluate their practical suitability and is being conducted at the [Biomass Institute](https://www.biomasseinstitut.de/) within [Weihenstephan-Triesdorf University](https://www.hswt.de/en/).

Key Features
------------
*   **Insect Detection**: Utilizes custom trained [YoloV8](https://github.com/ultralytics/ultralytics) for real-time insect detection in video frames (check [here](https://universe.roboflow.com/juan-chiavassa/fair-device_v2.0) the image dataset).
*   **Object Tracking**: [Bytetrack](https://github.com/ifzhang/ByteTrack) ensures smooth tracking of detected insects across frames.
*   **Polygon Zones**: With [Supervision](https://github.com/roboflow/supervision), we implement custom polygonal zones (entrance, inside, exit) for targeted monitoring.
*   **CSV Logging**: Logs relevant data (frame Nr, tracker IDs, class IDs, polygon zone, confidence scores) for analysis.

Next-Step Goals
---------------
1.  **Real-time monitoring**:
    
    * Implement camera live-streaming for real-time operation.  

2.  **Algorithm Refinement**:
    
    *   Improve the accuracy of the insect recognition model by extending the annotated image database.
    *   Refine the code to improve the integration between the detection and tracking system.
4.  **Analyzer Script Development**:
    
    *   Address data inconsistencies in the _log.csv file_ generated during tracking.
    *   Develop a metadata post-processing and analysis script to interpret insect entry- and exit- times and directions based on polygon activation.
5.  **Integration with [iNaturalist](https://www.inaturalist.org/)**:
    
    *   Extract high-confidence images from detected insects for uploading to the iNaturalist platform and perform taxonomic classification of insects. 
    *   Implement the [iNaturalist VisionAPI](https://forum.inaturalist.org/t/hidden-computer-vision-api/41775) for automatically uploading the images. 

Installation
------------

1.  Clone this repository:
    
    `git clone https://github.com/jach999/fairtrack.git`
    
     `cd fairtrack && mkdir runs`
    
3.  Set up the environment (Python 3.7+ recommended):
    
    `pip install -r requirements.txt`
    
    `python install_bytetrack.py`


    
Usage
-----

1.  Run the video tracking script:
    
    python fairtrack_test_video.py path/to/source_video.mp4 [path/to/target_video.mp4]
    *   `source_video`: Path to the input video.
    *   `target_video` (optional): Path to save the tracked video & .csv file (default: `runs/run#/source_video_test.mp4`).
    *   `--device` (optional): Specify the device used for the captured video (fd1, fd2, fd3, or fd4) - this corrects some framing differences between devices.
        
2.  Adjust polygon zones in `device_polygons.py`.
    
3.  View the tracked video and analyze the CSV log.
    

Example
-------

python fairtrack_test_video.py test_assets\fdV2_5\fd1\11-17-18.mp4 --device fd1

Result:


<img src="https://raw.githubusercontent.com/jach999/fairtrack/main/assets/11-17-18_test.gif"  width="500">

&nbsp;

**Test script in Colab** &nbsp;
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/jach999/fairtrack/blob/master/fairtrack.ipynb)

&nbsp;

Change Log
----------

*   **v1.0 (March 2024)**:
    *   Initial release.
    *   YoloV8 for insect detection.
    *   Bytetrack for tracking.
    *   Polygon zones defined.
    *   .csv logging


Author
------

*   Juan A. Chiavassa
*   Email: juan.chiavassa@hswt.com / juan.chiavassa@gmail.com
*   Project: Digitalisierung – anwenden, bewerten und kommunizieren - [Diabek](https://diabek.hswt.de/)
*   Location: [Biomass Institute](https://www.biomasseinstitut.de/), [Weihenstephan-Triesdorf University](https://www.hswt.de/en/), Merkendorf, Germany


Credits
-------

This project builds upon the work of [SkalskiP](https://github.com/SkalskiP). Specifically, we combined two of their insightful scripts:

1.  **[how-to-track-and-count-vehicles-with-yolov8](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-track-and-count-vehicles-with-yolov8.ipynb)**: This script leverages Bytetrack for vehicle tracking using YoloV8.
2.  **[how-to-detect-and-count-objects-in-polygon-zone](https://github.com/roboflow/notebooks/blob/main/notebooks/how-to-detect-and-count-objects-in-polygon-zone.ipynb)**: Here, Supervision is used for detecting and counting objects within polygonal zones.

We appreciate SkalskiP’s valuable contributions to the field, which inspired this work.


Get Involved
------------

*   **Contributors**: Join us if you’re passionate about entomology, computer vision, or open-source development.
*   **Feedback**: We welcome your ideas and suggestions.

Stay tuned as we continue refining and expanding the **Fairtrack** project 🌟🐜

* * *

