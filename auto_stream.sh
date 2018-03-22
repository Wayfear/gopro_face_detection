#!/bin/bash

a=$1
b="${a%.*}_$id.log"
nohup python -u $1 > ./$b 2>&1 &
b="nohup_pid.txt"
echo $! > ./$b
