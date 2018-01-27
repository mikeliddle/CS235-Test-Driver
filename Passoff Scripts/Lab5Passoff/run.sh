#!/bin/bash

# Pass Off Script
# author: Matt Hoiland
# last edit: 2017-01-19

EXE="program"
VERSION="-std=c++14"
FLAGS="-g -Wall"

MAIN="main.cpp"
cp PathfinderInterface.h src

if [[ -e $MAIN ]];
then
    cp $MAIN src/
else
    echo "TA main file is missing. Cannot proceed"
    exit 1
fi

if g++ $VERSION src/*.cpp src/*.h -o tests/$EXE;
then
    echo "Compilation succeeded!"
else
    echo "Compilation failed."
    exit 1
fi

cd tests
echo ""
echo "Moved to $(pwd)"

echo ""
echo "Running Student Program"
echo "--------"
valgrind --leak-check=full --show-leak-kinds=all ./$EXE
rm $EXE
mv out_file*.txt ../output
echo "--------"

cd ../
echo ""
echo "Moved to $(pwd)"

echo ""
echo "Running Diff"
echo "--------"
for f in tests/file*.txt;
do
    f=${f#tests/}
    if [ $f == $"file5.txt" ];
    then
        break;
    fi
    sdiff -s --strip-trailing-cr keys/key_$f output/out_$f > diffs/diff_$f
    if [ ${PIPESTATUS[0]} -eq 0 ];
    then
        echo "key_$f and out_$f are identical"
    else
        echo "key_$f and out_$f differ :: check diffs/diff_$f for details"
    fi
done
echo "--------

"

while true;
do
    read -p "Would you like to view Out_File5.txt in vim? [Y/N]?
Hint: Type ':q' then enter when you're done in vim. 
" n
    case $n in
        [Nn]* ) echo "Don't forget to check the random mazes!"; break;;
        [Yy]* ) echo "Opening Out_File5.txt."; vi output/out_file5.txt; break;;
        * ) echo "Please answer Y or N.";;
    esac
done
echo ""
while true;
do
    read -p "Clean up the pass off environment? [Y/N]? " yn
    case $yn in
        [Yy]* ) ./clean.sh; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer Y or N.";;
    esac
done
