#!/bin/sh
mkdir -p ~/bin
# Do libraries:
mkdir -p ~/lib
# Deal with libEZCAD:
(cd ~/lib ; rm -f libEZCAD.so libEZCAD.so.1 libEZCAD.so.1.0)
cp libEZCAD.so.1.0 ~/lib
(cd ~/lib ; ln -s libEZCAD.so.1.0 libEZCAD.so.1)
(cd ~/lib ; ln -s libEZCAD.so.1.0 libEZCAD.so)
# Deal with libCGAL:
(cd ~/lib ; rm -f libCGAL.so libCGAL.so.7 libCGAL.so.7.0 libCGAL.so.7.0.0)
cp libCGAL.so.7.0.0 ~/lib
(cd ~/lib ; ln -s libCGAL.so.7.0.0 libCGAL.so.7.0)
(cd ~/lib ; ln -s libCGAL.so.7.0.0 libCGAL.so.7)
(cd ~/lib ; ln -s libCGAL.so.7.0.0 libCGAL.so)
# Deal with libCGAL_Qt3:
(cd ~/lib ; rm -f libCGAL_Qt3.so libCGAL_Qt3.so.7 libCGAL_Qt3.so.7.0 libCGAL_Qt3.so.7.0.0)
cp libCGAL_Qt3.so.7.0.0 ~/lib
(cd ~/lib ; ln -s libCGAL_Qt3.so.7.0.0 libCGAL_Qt3.so.7.0)
(cd ~/lib ; ln -s libCGAL_Qt3.so.7.0.0 libCGAL_Qt3.so.7)
(cd ~/lib ; ln -s libCGAL_Qt3.so.7.0.0 libCGAL_Qt3.so)
# Deal with bin:
mkdir -p ~/bin
(cd ~/bin ; rm -f nef3_to_off off_fixup nh EZCAD_XML)
cp nef3_to_off nh off_fixup EZCAD_XML  ~/bin
# Deal with demo1.py:
chmod +x demo1.py
chmod +x demo2.py
chmod +x demo3.py
chmod +x demo4.py

