#!/bin/sh

export ITERATIONS=100

cd $(dirname $0)

echo Iterations: $ITERATIONS


echo Test 1
export TEST=1
printf '' > outfile1

#django/bench.sh | tee -a outfile1
sqlalchemy/bench.sh | tee -a outfile1
#sqlalchemysync/bench.sh | tee -a outfile1
tortoise/bench.sh | tee -a outfile1


echo Test 2
export TEST=2
printf '' > outfile2

#django/bench.sh | tee -a outfile2
sqlalchemy/bench.sh | tee -a outfile2
#sqlalchemysync/bench.sh | tee -a outfile2
tortoise/bench.sh | tee -a outfile2


echo Test 3
export TEST=3
printf '' > outfile3

#django/bench.sh | tee -a outfile3
sqlalchemy/bench.sh | tee -a outfile3
#sqlalchemysync/bench.sh | tee -a outfile3
tortoise/bench.sh | tee -a outfile3

echo `python -V`, Iterations: $ITERATIONS| tee -a results
cat outfile1 | ./present.py "Test 1" | tee -a results
cat outfile2 | ./present.py "Test 2" | tee -a results
cat outfile3 | ./present.py "Test 3" | tee -a results
echo | tee -a results
