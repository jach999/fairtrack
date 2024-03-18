import os
import subprocess

HOME = os.path.dirname(__file__)
os.chdir(HOME)

def install_bytetrack():
    # Clone the ByteTrack repository
    os.system("git clone https://github.com/ifzhang/ByteTrack.git")

    # Install dependencies
    os.chdir("ByteTrack")
    os.system("pip install -q -r requirements.txt")
    os.system("python setup.py -q develop")

    # Install additional packages
    os.system("pip install -q cython_bbox")
    os.system("pip install -q lap")
    os.system("pip install -q loguru") 
    os.system("pip install -q onemetric")
    # Print success message
    import yolox
    print("yolox.__version__:", yolox.__version__)
    print("ByteTrack installation completed successfully!")
    os.chdir(HOME)
    
if __name__ == "__main__":
    install_bytetrack()
