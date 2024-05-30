install nececery dependancys:

----------------------------------------
sudo apt-get install libgstreamer1.0-dev gstreamer1.0-tools gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly
----------------------------------------

----------------------------------------
pip3 install opencv-python
----------------------------------------

----------------------------------------
python3 -c "import cv2; print(cv2.__version__)"
----------------------------------------

----------------------------------------
Ensure all dependencies are met: Sometimes, missing dependencies can cause issues. Install the necessary dependencies:

sudo apt-get install -y libjpeg-dev libpng-dev libtiff-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
----------------------------------------