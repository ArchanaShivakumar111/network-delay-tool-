#!/bin/bash

echo "Starting POX Controller..."
cd ~/pox
python3 pox.py log.level --DEBUG misc.controller &
POX_PID=$!

sleep 3

echo "Starting Mininet Topology..."
cd /mnt/c/PESU/Sem4/CN/orange
sudo python3 topology.py

kill $POX_PID
