i=0

until [ $i -gt 6 ]
do
  docker build --build-arg ID=$i -t stanza-$i .
  ((i=i+1))
done