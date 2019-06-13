#!/bin/bash

curl -X POST "http://extproxy.intertransl.com:5601/api/spaces/space" -u elastic:$(cat /opt/elk/elastic) -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d '{"id": "linux-servers","name": "Linux Servers","description" : "This is the Linux Servers Space","color": "#6198d6","initials": "LS"}'
curl -X POST "http://extproxy.intertransl.com:5601/api/spaces/space" -u elastic:$(cat /opt/elk/elastic) -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d '{"id": "docker","name": "Docker","description" : "This is the Docker Space","color": "#ea7e89","initials": "DK"}'

touch /opt/elk/fb.conf
echo "output.elasticsearch:" >> /opt/elk/fb.conf
echo " hosts: [\""$HOSTNAME".intertransl.com:9200\"]" >> /opt/elk/fb.conf
echo " username: \"elastic\"" >> /opt/elk/fb.conf
echo " password: "$(cat /opt/elk/elastic) >> /opt/elk/fb.conf
echo "setup.kibana:" >> /opt/elk/fb.conf
echo " host: \""$HOSTNAME".intertransl.com:5601\"" >> /opt/elk/fb.conf
echo " space.id: \"linux-servers\"" >> /opt/elk/fb.conf