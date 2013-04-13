#!/bin/sh
# Slurp over the EZCAD.tar.gz and unpack it:
rm -f EZCAD.tar.gz EZCAD.tar
wget http://gramlich.net/projects/ezcad/EZCAD.tar.gz
gunzip EZCAD.tar.gz
tar xvf EZCAD.tar
# Execute update_helper.sh (which just got unpacked):
sh update_helper.sh

