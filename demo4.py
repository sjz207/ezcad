#!/usr/bin/python

from EZCAD import *

def demo4(parent):
    """ demo3 design. """

    d4 = parent.start("demo4")
    p1 = part1(d4)

    if d4.dimensions_mode():
	inch = Length.inch
	z = inch(0)
	p1p = d4.point_xyz_set("p1_place", z, z, z)
	d4.place(p1, "part1", p1p)

    return d4.done()

def part1(parent):
    """ part1 design """

    p1 = parent.start("part1")

    if p1.dimensions_mode():
	inch= Length.inch
	zero = inch(0)
	tube_start = p1.point_new(zero, zero, inch(-2))
	tube_end = p1.point_new(zero, zero, inch(2))
	o = p1.point("$O")
	t = p1.point("$T")
	tn = p1.point("$TN")
	tw = p1.point("$TW")
	p1.rod("cyan", "aluminum", tube_start, tube_end, inch(1), 0)

	if p1.construct_mode():
	    print "Construct part1"
	    p1.vice_position("mount in vice long-wise", t, tn, tw)
	    p1.screw_hole("center", "6-32", t, o, "p")

    return p1.done()

EZCAD.process(demo4, 1, 0)


