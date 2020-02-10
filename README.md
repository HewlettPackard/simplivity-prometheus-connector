# Prometheus Connector for HPE SimpliVity 
The monitoring environment can be build on a separate physical server or virtual machine or as a fully containerized solution. If you decide to deploy it as a virtual machine or physical server, then please consult the corresponding Prometheus und Grafana documentation. The following components are required to build the containerized solution:
- A Docker container run time environment
- Prometheus container image
- Grafana container image
- SimpliVity Prometheus Connector scripts

We will assume that you do have a Docker container run time environment available and will describe the steps necessary to implement the SimpliVity monitoring environment. Each SimpliVity connector, Prometheus and Grafana will run as a separate container. 

### Application Network
The SimpliVity connector together with the Prometheus and Grafana container are building the monitoring app. It is best practice to limit container cross talk to the necessary minimum by running different apps on separate networks. Therefore, a bridged network for the monitoring app was created first:

> docker network create svtmonitor

Each container that is part of the monitoring app will use this network.

### SimpliVity Credentials
A Python script (CreateCredentials.py) is used to create the necessary input parameter for the SimpliVity Connector. This script can run on any Python 3 system that does have the necessary Python packages (fernet, getpass, lxml) installed.

> python3 CreateCredentials.py

The script will ask for the necessary input parameter:
- username and password credentials for connecting into the SimpliVity federation, 
- the time range in seconds  
- resolution (SECONDS or MINUTES)
- monitoring interval in seconds
- logfile name
- http server port that should be used
- OVC IP address
- Filename 

The connector will capture the data every monitoring interval for the given past time range with the defined resolution and it will build an average of all available data points for the given time range. 
Two files (*__filename.xml__* and *__filename.key__*) are the output of the CreateCredentials.py script. The first one, *__\<filename>.xml__*, contains the input parameter (username and password encrypted) for the SimpliVity connector. The other one, *__\<filename>.key__*, provides the key that is needed to decrypt the encrypted username and password. 

### Prometheus Configuration File 
The Prometheus configuration file contains entries for every single process or service that should be monitored. In our case, we do have a separate entry for each SimpliVity federation that should be monitored. The entry for the SimpliVity environment looks like:

> job_name: simpliVity
> honor_timestamps: true
> scrape_interval: 20s
> scrape_timeout: 10s
> metrics_path: /metrics
> static_configs:
>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- targets: ['simplivity:9091']

The target is defined as __\<connector *container name*>:\<port>__; i.e. in the above example, the connector container for the primary Simplivity environment has the name simplivity and provides the collected metrics on port 9091.  The Prometheus job for the secondary SimpliVity federation looked similar with a different target.  Each Prometheus scrape job is defined by the job name, scrape interval and timeout, the metrics path and the targets. The above example is defining that the metrics of the SimpliVity system should be collected every 20s from the address http://simplivity:9091/metrics and the collection times out if it takes longer than 10s. It is possible to define multiple targets per job but we decided to define multiple job entries in order to be more flexible in the settings.

### Starting the container
Once the container images and the persistent volume are prepared, the docker container can be started:
1.	Start the SimpliVity connector container for the SimpliVity federation
> docker build -f svtconnect.ubuntu.Dockerfile -t svtconnect:1.0 .
> docker run -d -p 9091:9091 --network=svtmonitor svtconnect:1.0
2.	Start the Prometheus container
> docker build -f Prometheus.Dockerfile -t prometheus:1.0 .
> docker run -d -p 9090:9090 --network=svtmonitor prometheus:1.0
4.	Start the Grafana container
> docker run -d -p 3000:3000 --network=svtmonitor --restart unless-stopped --name grafana grafana/grafana

We did start all container with the restart unless-stopped flag, to make sure, even if for some reason the container is stopped, that it is restarted. The collected data is now available on the server, where the container are running, at the following web addresses:
> Prometheus:  *__https://\<hostname>:9090__*
> Grafana: *__https://\<hostname>:3000__*

During the initial testing we did make even the connector output available by using the -p option of the docker run command, but once the system is running without any issues it is not necessary to export the IP port used by the docker container to an external host port. 
The only step that is now missing is to define the Grafana dashboards to visualize the collected data. 
Sample dashboards (Federation Overview, Cluster Overview and Node Overview) are availabe. 
Please take a look at the Grafana documentation on the details on how to build Grafana dashboards.
