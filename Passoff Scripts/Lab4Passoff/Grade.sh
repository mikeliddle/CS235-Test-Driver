#!/bin/sh
#compile
cp StationInterface.h src
cp StationInterfaceExtra.h src

if g++ $VERSION src/*.cpp src/*.h -o EXE;
then
    echo "Compilation succeeded!"
else
    echo "Compilation failed."
    exit 1
fi
    
echo

#run with Valgrind
valgrind --leak-check=yes ./EXE

rm EXE

echo ""
while true;
do
    read -p "Clean up the pass off environment? [Y/N]? " yn
    case $yn in
        [Yy]* ) rm -fv src/*; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer Y or N.";;
    esac
done




echo
echo *******Complete*******
echo
