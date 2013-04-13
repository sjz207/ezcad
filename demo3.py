#!/usr/bin/python

from EZCAD import *

def demo3(parent):
    """ demo3 design. """

    d3 = parent.start("demo3")
    p1 = part1(d3)

    if d3.dimensions_mode():
	inch = Length.inch
	z = inch(0)
	p1p = d3.point_xyz_set("p1_place", z, z, z)
	d3.place(p1, "part1", p1p)

    return d3.done()

def part1(parent):
    """ part1 design """

    p1 = parent.start("part1")

    if p1.dimensions_mode():
	inch= Length.inch
	zero = inch(0)
	b = p1.point("$B")
	t = p1.point("$T")
	o = p1.point("$O")
	tn = p1.point("$TN")
	tw = p1.point("$TW")
	diagonal = p1.point_new(inch(1), inch(1), inch(2))
	p1.block_diagonal(diagonal, "red", "aluminum")

	if p1.construct_mode():
	    print "Construct part1"
	    p1.vice_position("moint in vice long-wise", t, tn, tw)
	    p1.chamfers(zero, zero)
	    p1.vertical_lathe("Lathe", t, o, inch(0.75), inch(1), "i")

    return p1.done()

EZCAD.process(demo3, 1, 0)


