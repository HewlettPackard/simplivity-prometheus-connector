
# docker build -t svtconnect -f svtconnect.Dockerfile . 
# docker run -i -p 9091:9091 --name svtconnect svtconnect
# User Centos as the base Image
FROM  centos
#
LABEL maintainer="Hewlett Packard Enterprise"
LABEL version="1.0"
LABEL copyright="Hewlett Packard Enterprise, 2019"
LABEL license="GNU General Public License v3"
LABEL DESCRIPTION="SimpliVity - Prometheus Connector"
# Install Python 3.6
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum update -y
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip
RUN /usr/bin/pip3.6 install --upgrade pip
# Install the necessary Python packages:
RUN /usr/bin/pip3.6 install datetime && \
    /usr/bin/pip3.6 install requests && \
	/usr/bin/pip3.6 install cryptography && \
	/usr/bin/pip3.6 install fernet && \
	/usr/bin/pip3.6 install lxml && \
	/usr/bin/pip3.6 install prometheus_client
# copy the necessary python files to the container
RUN mkdir /opt/svt
COPY SimpliVityClass.py /opt/svt
COPY svtPromConnector.py /opt/svt
COPY SvtConnector.key /opt/svt
COPY SvtConnector.xml /opt/svt
# Start the collector
CMD /usr/bin/python3.6 /opt/svt/svtPromConnector.py