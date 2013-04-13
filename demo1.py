#!/usr/bin/python

from EZCAD import *

def demo1(parent):
    """ demo1 design. """

    inch = Length.inch
    z = inch(0)

    a1 = parent.start("demo1")
    p1 = flat_part(a1, "part1", "$T", "$TN", "$TW", "red")
    p2 = flat_part(a1, "part2", "$T", "$TW", "$TS", "green")
    p3 = flat_part(a1, "part3", "$T", "$TS", "$TE", "blue")
    p4 = flat_part(a1, "part4", "$T", "$TE", "$TN", "cyan")
    p5 = flat_part(a1, "part5", "$B", "$BN", "$BE", "red")
    p6 = flat_part(a1, "part6", "$B", "$BE", "$BS", "green")
    p7 = flat_part(a1, "part7", "$B", "$BS", "$BW", "blue")
    p8 = flat_part(a1, "part8", "$B", "$BW", "$BN", "cyan")

    if a1.dimensions_mode():
	zz = inch(0.25)
	p1p = a1.point_xyz_set("p1_place", inch(-1), inch(-1), zz)
	p2p = a1.point_xyz_set("p2_place", inch(1), inch(-1), zz)
	p3p = a1.point_xyz_set("p3_place", inch(-1), inch(1), zz)
	p4p = a1.point_xyz_set("p4_place", inch(1), inch(1), zz)
	p5p = a1.point_xyz_set("p5_place", inch(-1), inch(-1), -zz)
	p6p = a1.point_xyz_set("p6_place", inch(1), inch(-1), -zz)
	p7p = a1.point_xyz_set("p7_place", inch(-1), inch(1), -zz)
	p8p = a1.point_xyz_set("p8_place", inch(1), inch(1), -zz)
	a1.place(p1, "part1", p1p)
	a1.place(p2, "part2", p2p) 
	a1.place(p3, "part3", p3p)
	a1.place(p4, "part4", p4p)
	a1.place(p5, "part5", p5p)
	a1.place(p6, "part6", p6p) 
	a1.place(p7, "part7", p7p)
	a1.place(p8, "part8", p8p)

	xxx = a1.point_subtract("part1.$T", "part5.$T")
	print "part1.t - part5.t=", xxx

    return a1.done()

def flat_part(parent, name, surface_name, vice_name, dowel_name, color):
    """ """

    inch= Length.inch
    zero = inch(0)
    p = parent.start(name)

    if p.dimensions_mode():
	surface_point = p.point(surface_name)
	vice_point = p.point(vice_name)
	dowel_point = p.point(dowel_name)
	b = p.point("$B")
	t = p.point("$T")
	tne = p.point("$TNE")
	bne = p.point("$BNE")
	hole1_t = p.point_xyz_set("hole_tne", tne.x.half(), tne.y.half(), tne.z)
	hole1_b = p.point_xyz_set("hole_bne", bne.x.half(), bne.y.half(), bne.z)
	diagonal = p.point_new(inch(1), inch(2), inch(0.125))
	p.block_diagonal(diagonal, color, "aluminum")

	if p.construct_mode():
	    #print "Construct", name
	    p.vice_position("mount {0} in vice long-wise".format(name), \
	      surface_point, vice_point, dowel_point)
	    if surface_name == "$T":
		p.hole("hole1 NE", inch(.25), hole1_t, hole1_b, "t")
		p.screw_through("center", "6-32", t, "di")
	    else:
		p.hole("hole1 NE", inch(.25), hole1_b, hole1_t, "t")
		p.screw_through("center", "6-32", b, "di")

    return p.done()

EZCAD.process(demo1, 1, 0)


