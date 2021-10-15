sudo apt update
sudo apt install -y python3-pip
pip3 install selenium==3.141.0
pip3 install pyvirtualdisplay
sudo apt install -y unzip
sudo apt install -y xvfb
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb
wget https://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
wget -O t.py https://raw.githubusercontent.com/hbutt877/nust/master/t.py
wget -O job_t.sh https://raw.githubusercontent.com/hbutt877/nust/master/job_t.sh
rm chromedriver_linux64.zip
rm google-chrome-stable_current_amd64.deb
