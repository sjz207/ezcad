#!/usr/bin/python

from EZCAD import *

def demo2(parent):
    """ demo2 design. """

    inch = Length.inch
    z = inch(0)

    a1 = parent.start("demo2")
    p1 = part1(a1)

    if a1.dimensions_mode():
	zz = inch(0.25)
	p1p = a1.point_xyz_set("p1_place", inch(-1), inch(-1), zz)
	a1.place(p1, "part1", p1p)

    return a1.done()

def part1(parent):
    """ part1 design """

    inch= Length.inch
    zero = inch(0)
    p1 = parent.start("part1")

    if p1.dimensions_mode():
	b = p1.point("$B")
	t = p1.point("$T")
	tn = p1.point("$TN")
	tw = p1.point("$TW")
	tne = p1.point("$TNE")
	bne = p1.point("$BNE")
	bsw = p1.point("$BSW")
	diagonal = p1.point_new(inch(1), inch(2), inch(0.125))
	p1.block_diagonal(diagonal, "red", "aluminum")
	radius = p1.length_set("radius", inch(0.025))
	pocket1a = \
	  p1.point_xyz_set("pocket1a", tne.x.half(), tne.y.half(), tne.z.half())
	pocket1b = \
	  p1.point_xyz_set("pocket1b", bsw.x.half(), bsw.y.half(), bsw.z.half())
	pocket_radius = inch(0.25)

	if p1.construct_mode():
	    print "Construct part1"
	    p1.vice_position("moint in vice long-wise", t, tn, tw)
	    p1.corner("TNE", p1.point("$TNE"), radius)
	    p1.corner("TNW", p1.point("$TNW"), radius)
	    p1.corner("TSW", p1.point("$TSW"), radius)
	    p1.corner("TSE", p1.point("$TSE"), radius)
	    p1.chamfers(zero, zero)
	    p1.contour("exterior trim", t, b, 0.25, "t")
	    p1.simple_pocket("pocket1", pocket1a, pocket1b, pocket_radius, "t")

    return p1.done()

EZCAD.process(demo2, 1, 0)


