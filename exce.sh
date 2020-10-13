#!bin/bash

date

for ((i=1;i<2;i++));do
{
mkdir -p dir$i;cp ./smallfile-bench.py ./dir$1;cd dur$i;mkdir tes$i
}
done
wait
date