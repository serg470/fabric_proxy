#!/bin/sh

sed -i "s/changeme/$(cat /opt/elk/elastic)/g" /opt/elk/kibana/config/kibana.yml
sed -i "s/changeme/$(cat /opt/elk/elastic)/g" /opt/elk/logstash/config/logstash.yml
sed -i "s/changeme/$(cat /opt/elk/elastic)/g" /opt/elk/logstash/pipeline/logstash.conf

curl -X POST "http://localhost:5601/api/spaces/space" -u elastic:$(cat /opt/elk/elastic) -H 'kbn-xsrf: true' -H 'Content-Type: application/json' -d'{"id": "linux-servers","name": "Linux

touch /opt/elk/filebeat.yml
echo "output.elasticsearch:" >> /opt/elk/filebeat.yml
echo " hosts: ["$HOSTNAME".intertransl.com:9200\"]" >> /opt/elk/filebeat.yml
echo " username: \"elastic\"" >> /opt/elk/filebeat.yml
echo " password: "$(cat /opt/elk/elastic) >> /opt/elk/filebeat.yml
echo "setup.kibana:" >> /opt/elk/filebeat.yml
echo " host: "$HOSTNAME".intertransl.com:5601\"" >> /opt/elk/filebeat.yml
echo " space.id: \"linux-servers\"" >> /opt/elk/filebeat.yml