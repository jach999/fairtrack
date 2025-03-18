import os
import subprocess

HOME = os.path.dirname(__file__)
os.chdir(HOME)

def install_bytetrack():
    # Clone the ByteTrack repository
    os.system("git clone https://github.com/ifzhang/ByteTrack.git")

    os.chdir("ByteTrack")
    os.system("python setup.py -q develop")

    # Install packages
    os.system("pip install onemetric")
    os.system("pip install -opencv-python")
    os.system("pip install scikit-image")
    os.system("pip install tqdm")
    os.system("pip install thop")
    os.system("pip install tabulate")
    os.system("pip install tensorboard")
    os.system("pip install motmetrics")
    os.system("pip install filterpy")
    os.system("pip install h5py")

    # Print success message
    import yolox
    print("yolox.__version__:", yolox.__version__)
    print("ByteTrack installation completed successfully!")
    os.chdir(HOME)
    
if __name__ == "__main__":
    install_bytetrack()
