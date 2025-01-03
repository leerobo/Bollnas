#!/bin/sh
tag="lee"
user="leerobo"
host="docker.io"
echo "-------------- Docker Run for vincent-$user on host $host/$user "
docker build -f dockerfile  --network=host --tag vincent:$tag .
docker login --username $user --password Winter1970.
docker tag vincent:$tag $host/$user/vincent-$tag:main
docker image push $user/vincent-$tag:main
echo " "
echo "-------------- Complete $host/$user/vincent-$tag"
echo " "