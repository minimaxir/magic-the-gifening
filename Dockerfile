FROM phusion/baseimage:0.9.22

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

RUN apt-get -y update && apt-get -y install python3-dev python3-pip libav-tools imagemagick libopencv-dev python-opencv

RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install imageio numpy scipy matplotlib sympy nose decorator tqdm pillow pytest twython moviepy
RUN python3 -c "import imageio; imageio.plugins.ffmpeg.download()"

COPY . /

# Setup cron job
# https://stackoverflow.com/a/44958097
RUN (crontab -l; echo "0 */6 * * * (ls; cd / && python3 /mtgifening.py) >/dev/null") | crontab

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
