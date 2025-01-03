host="ghcr.io"
user="krkj-te"
password="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"
dockerhost="$host/tietoevry-card-acquiring/vincent"
echo '-------------- Forced Github Build '
docker build -f dockerfile --network=host --tag vincent .
docker login $host --username $user --password "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"
docker tag vincent $dockerhost/vincent:main
docker image push $dockerhost/vincent:main
echo " "
echo "-------------- Complete $host/$user/vincent:main"
echo " "
