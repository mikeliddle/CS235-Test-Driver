#!/bin/bash
EXE=run_me
netId=$1
labName=$2
logDate=$3

# compile the code to an executable
>&2 echo "compiling files:"

for file in "./*.cpp"; do
  >&2 echo $file
done

>&2 echo ""

>&2 echo "g++ -std=c++14 -Wall -g -o\"$EXE\" *.cpp"
g++ -std=c++14 -Wall -g -o "$EXE" *.cpp

# check for any errors.
if (( $? )) ;
then
	>&2 echo Compilation Failed $?
  echo "0/0"
else
  >&2 echo Compilation Succeeded!
  echo "$logDate,$netId,$labName,10/10"

	rm ./$EXE
fi
