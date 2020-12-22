# Digital Twin Controller

 Demo video is here:
 
 
**Prerequisites (My computer settings)**
- Ubuntu 18.04
- Java 8
- Node 8.10
- npm 3.5.2
- Eclipse Ditto
- docker-compose 1.25.4
- Docker 19.03.6
- Python 3.7
- Raspberry Pi 4 B
- SenseHat Board

**Installation**
**Host**
- pip install rticonnextdds-connector
- Setting NODE_PATH environemnt variable to gloabal node_modules path
- npm install -g rticonnextdds-connector
- npm install -g bufferutil
- npm install -g utf-8-validate
- npm install -g ws
- Cloning and running Eclipse Ditto
- git clone https://github.com/eclipse/ditto.git
- cd ditto/deployment/docker
- docker-compose up -d

**Raspberry Pi**
- sudo apt install sense-hat
- pip install rticonnextdds-connector


**Running**
- clone the project 
- cd DigitalTwinController/out/production/Szakdoga
- java Main
- Add your Raspberry Pi Device
- Generate DT with ZIP file szakdoga.bme.vik_SensePi_1.0.0.zip 
- Run the DT
