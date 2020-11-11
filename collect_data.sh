#!/bin/bash

echo "Enter name:"
read name

cd data #open data folder
mkdir $name #make directory for person
cd $name #open and make relevant folders
mkdir digits
mkdir phrases
cd ..
cd ..

python python Python/Record.py niceta