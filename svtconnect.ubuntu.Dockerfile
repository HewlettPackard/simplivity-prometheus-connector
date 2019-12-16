
# docker build -t svtconnect -f svtconnect.Dockerfile . 
# docker run -i -p 9091:9091 --name svtconnect svtconnect
# User Ubuntu as the base Image
FROM ubuntu
#
LABEL maintainer="Hewlett Packard Enterprise"
LABEL version="1.0"
LABEL copyright="Hewlett Packard Enterprise, 2019"
LABEL license="GNU General Public License v3"
LABEL DESCRIPTION="CTC SimpliVity Pythone container based on Ubuntu"
# Install Python 3.6
RUN apt-get update
RUN apt-get -y install python3.6 && \
	apt-get -y install python3-pip && \
	apt-get -y install vim && \
	apt-get -y install cron 
# Install the necessary Python packages:
RUN /usr/bin/pip3 install requests && \
	/usr/bin/pip3 install fernet && \
	/usr/bin/pip3 install cryptography && \
	/usr/bin/pip3 install lxml && \
	/usr/bin/pip3 install prometheus_client
# copy the necessary python files to the container
RUN mkdir /opt/svt
COPY SimpliVityClass.py /opt/svt
COPY svtPromConnector.py /opt/svt
COPY SvtConnector.key /opt/svt
COPY SvtConnector.xml /opt/svt
# Start the collector
CMD /usr/bin/python3.6 /opt/svt/svtPromConnector.py