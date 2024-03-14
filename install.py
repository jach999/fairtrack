import subprocess
import os

HOME = os.path.dirname(__file__)

def install_package(package):
    subprocess.call(["pip", "install", package])

if __name__ == "__main__":
    # Install numpy
    install_package("numpy==1.22.4")

    # Install ultralytics (YOLOv8)
    install_package("ultralytics")
    
    # Install supervision
    install_package("supervision==0.2.0")

    # Clone ByteTrack repository
    #subprocess.call(["git", "clone", "https://github.com/ifzhang/ByteTrack.git"])
    
    # Change working directory to ByteTrack
    #os.chdir("ByteTrack")

    # Install required packages inside the ByteTrack directory
    #subprocess.call(["pip", "install", "-r", "requirements.txt"])
    #subprocess.call(["python", "setup.py", "develop"])
    #install_package("cython_bbox")
    #install_package("lap")
    #install_package("loguru")
    #install_package("onemetric")

    # Add ByteTrack path to sys.path in your script
    #with open(os.path.abspath(__file__), "a") as f:
     #f.write("\nimport sys\n")
     #f.write(f"sys.path.append(\"{HOME}\ByteTrack\")\n")

    # Display YOLOX version
    #subprocess.call(["python", "-c", "import yolox; print(\"yolox.__version__:\", yolox.__version__)"])
    
    # Clone yolox repository
    #subprocess.call(["git", "clone", "https://github.com/Megvii-BaseDetection/YOLOX.git"])
   
    # Change working directory to yolox
    #os.chdir("YOLOX")

    # Install required packages inside the yolox directory
    #subprocess.call(["python3", "setup.py", "develop"])



