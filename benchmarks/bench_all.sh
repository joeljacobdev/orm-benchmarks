#!/bin/sh

echo > results

python -V | grep PyPy || DBTYPE=postgres ./bench.sh $1
cat results
