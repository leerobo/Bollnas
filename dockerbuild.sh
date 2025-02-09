#!/bin/sh
tag="sensorhub"
user="leerobo"
host="docker.io"
echo "-------------- Docker Run for vincent-$user on host $host/$user "
docker build -f dockerfile  --network=host --tag bollnas:$tag .
#docker login --username $user --password Winter1970.
#docker tag bollnas:$tag $host/$user/bollnas-$tag:main
#docker image push $user/bollnas-$tag:main
echo " "
echo "-------------- Complete $host/$user/bollnas-$tag"
echo " "