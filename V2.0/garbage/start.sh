#!/bin/bash
 
killall python

echo 23.001 >  /dev/shm/freq
echo 14 > /dev/shm/band

echo 0.0001 > /dev/shm/step
echo 'cw' > /dev/shm/mode
echo 'off' > /dev/shm/rit_rx_status
echo 'off' > /dev/shm/rit_tx_status
echo 'rx' > /dev/shm/tcvr_status
echo 0 > /dev/shm/rit_rx
echo 0 > /dev/shm/rit_tx
echo 2400 > /dev/shm/sota_bw
echo 1500 > /dev/shm/sota_center
echo "center" > /dev/shm/sota_mode


python encoder.py &
python main.py &



trapeze () {

printf "\rYikes! Trying to kill me!!"

killall python
exit 0
}

trap trapeze SIGINT

while true; do
 read crap
 printf "You entered some text.."
 sleep 1
done
