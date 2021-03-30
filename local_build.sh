
#!/usr/bin/bash

export HOST=artifactory.kraken.kcell.kz:6555
echo "host is ${HOST}"

docker login -u admin -p admin $HOST
export CURRENT=$HOST/datalake-$1:debug
export LATEST=$HOST/datalake-$1:latest

docker build -t $CURRENT kcell_kfp_alerts/.
docker tag $CURRENT $LATEST

docker push $CURRENT
docker push $LATEST


docker pull $LATEST

docker run -ti --entrypoint='' $LATEST $2
