# Copyright (c) 2011 by Wayne C. Gramlich.
# All rights reserved.

#EZCC := ../easyc/releases/latest/ezcc
EZCC := ../easyc/ezcc.ez
EZCC_OPTS := -I ../ogls -L /home/wayne/lib
OGLS_DIR := ../ogls
LIB_EZCAD := libEZCAD.so.1.0
PROGRAMS :=		\
	Lifter		\
	Test1		\
	EZCAD_XML	\
	off_fixup	\
	SCARA		\
	Tooling		\
	ViewSonic

EZCAD_TAR_FILES := 		\
    demo1.py			\
    demo2.py			\
    demo3.py			\
    demo4.py			\
    ezcad.txt			\
    EZCAD.py			\
    EZCAD_XML			\
    libCGAL.so.7.0.0		\
    libCGAL_Qt3.so.7.0.0	\
    libEZCAD.so.1.0		\
    off_fixup			\
    nef3_to_off			\
    nh				\
    update.sh			\
    update_helper.sh

#all: ${PROGRAMS} EZCAD.tar.gz
all: EZCAD_XML EZCAD.tar.gz

$(LIB_EZCAD): EZCAD.ezc off_fixup
	$(EZCC) -I ../ogls EZCAD
	cp $@ ~/lib
	(cd ~/lib; ln -fs $@ libEZCAD.so.1; ln -fs $@ libEZCAD.so )

nef3_to_off: ../nef3_to_off/nef3_to_off
	rm -f $@
	cp ../nef3_to_off/nef3_to_off .

Lifter: Lifter.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} Lifter

SCARA: SCARA.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} SCARA

Tooling: Tooling.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} Tooling

Test1: Test1.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} Test1

EZCAD_XML: EZCAD_XML.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} EZCAD_XML

nh: ../../../download/cgal/CGAL-3.8/demo/Nef_3/nef_3_homogeneous
	rm -f $@
	cp ../../../download/cgal/CGAL-3.8/demo/Nef_3/nef_3_homogeneous nh

off_fixup: off_fixup.ezc
	$(EZCC) off_fixup

libCGAL_Qt3.so.7.0.0: ../../../download/cgal/CGAL-3.8/lib/libCGAL_Qt3.so.7.0.0
	rm -f !@
	cp ../../../download/cgal/CGAL-3.8/lib/libCGAL_Qt3.so.7.0.0 .

libCGAL.so.7.0.0: ../../../download/cgal/CGAL-3.8/lib/libCGAL.so.7.0.0
	rm -f !@
	cp ../../../download/cgal/CGAL-3.8/lib/libCGAL.so.7.0.0 .

ViewSonic: ViewSonic.ezc $(LIB_EZCAD)
	$(EZCC) ${EZCC_OPTS} ViewSonic

EZCAD.tar.gz: ${EZCAD_TAR_FILES}
	rm -f $@
	tar cvf EZCAD.tar ${EZCAD_TAR_FILES}
	gzip EZCAD.tar

clean:
	rm -f ${PROGRAMS}
	rm -f libEZCAD.so.1
	for x in c h ezh ezg o ; do		\
	    rm -f Easy_C.$$x ;			\
	    rm -f GLU.$$x ;			\
	    rm -f Math.$$x ;			\
	    rm -f Unix.$$x ;			\
	    for y in ${PROGRAMS} EZCAD ; do 	\
		rm -f $$y.$$x ;			\
		done ;				\
	    done
	for x in ${PROGRAMS} EZCAD ; do		\
	    rm -f $$x.ezc~ ;			\
	    done
	rm -f Makefile~
	rm -f Easy_C_C.o Unix_C.o GLU_C.o $(LIB_EZCAD)
	touch foo.bom foo.ngc foo.ezcad
	rm *.bom *.ngc *.ezcad
	rm -rf EZCAD



