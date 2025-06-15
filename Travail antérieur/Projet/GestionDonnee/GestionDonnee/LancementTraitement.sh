#!/bin/bash

python3 HeatMap.py

cd APrecision
./AutomatisationCalculPrecision.sh

sleep 2

cd ..
cd ./NoteComplexite
 
./AutomatisationRecuperationNote.sh

sleep 2

cd ..

