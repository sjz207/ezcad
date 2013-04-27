#!/usr/bin/env python

from EZCAD2 import *

inch = Length.inch
zero = inch(0.0)

class Paste(Part):
    """ Paste: Solder paste holder assembly. """ 

    def __init__(self, parent):
	""" Paste_Assembly: Initialize *self* to have """

	# List the children {Part}'s in the {Part} tree:
	self.holder = Holder(self)
	self.wall = Wall(self)
	self.top = Top(self)

	# Initialize some dimensions:
	self.dz = inch(4.000)
	self.dy = inch(2.000)
	self.dx = inch(3.000)

	# Initialize the parent class object:
	Part.__init__(self, "paste", parent)

    def construct(self):
	""" Paste: Construction method. """

	self.place(self.wall, "west_wall", self.o)
	self.place(self.wall, "east_wall",
	  self.point(self.dx - self.wall.thickness, zero, zero))
	self.place(self.top, "top", self.o)
	self.place(self.holder, "holder", self.o)

class Top(Part):

    def __init__(self, parent):
	""" Top: """

	# Create the children {Part}'s in the {Part} tree:
	#self.shaft = Shaft(self)
	self.top_plate = Top_Plate(self)
	self.shaft = Shaft(self)

	# Initilize the {Part} parent class object:
	Part.__init__(self, "top", parent)

    def construct(self):
	self.place(self.top_plate, "top_plate", self.o)
	#self.place(self.shaft, "shaft", self.o)

class Top_Plate(Part):
    """ top_plate design """

    def __init__(self, parent):
	# Initilize the {Part} parent class object:
	Part.__init__(self, "top_plate", parent)
	self.thickness = inch("1/4")
	self.shaft_depth = inch("1/8")

    def construct(self):
	top = self._parent
	shaft = top.shaft
	paste = top._parent
	wall = paste.wall

	extra = inch(0.25)
	self.extra_xyz(extra, extra, zero)
	corner1 = self.point(wall.e.x, wall.s.y, wall.t.z - self.thickness)
	corner2 = self.point(-wall.e.x, wall.n.y, wall.t.z)
	self.block_corners(corner1, corner2, "dark_blue", "aluminum")

	self.vice_position("mount flat in vice", self.t, self.xtn, self.xtw)
	self.tooling_plate("tooling plate", "1As 1Bs")
	self.tooling_plate_mount("mount tooling plate")

	# Put center hole all the way through to drain coolant:
	self.screw_through("center", "6-32", self.t, "c")
	self.cnc_flush()

	shaft_depth = inch("3/8")
	collet_inside_diameter = inch(1.250)
	collet_outside_diameter = inch(1.500)
	collet_depth = inch(0.100)
	collet_depth_point = self.point(zero, zero, self.t.z - collet_depth)
	shaft_depth_point = self.point(zero, zero, self.t.z - shaft_depth)
	self.hole("inside collet", collet_inside_diameter,
	  self.t, collet_depth_point, "m")
	self.hole("shaft hole", shaft.diameter + inch(0.010), self.t,
	  shaft_depth_point, "m")

	self.vertical_lathe("outside collet", \
	  self.t, collet_depth_point, collet_outside_diameter, \
	  collet_outside_diameter + inch(1.25), "")
	left_pocket1 = self.point(self.w.x - inch(0.25),
	  self.s.y - inch("1/16"), self.t.z - collet_depth)
	left_pocket2 = \
	  self.point_new(-collet_outside_diameter.half() - inch(0.05),
	  self.n.y + inch("1/16"), self.t.z)
	right_pocket1 = self.point( \
	  collet_outside_diameter.half() + inch(0.05),
	  self.s.y - inch("1/16"), self.t.z - collet_depth)
	right_pocket2 = self.point(self.e.x + inch(0.25),
	  self.n.y + inch("1/16"), self.t.z)

	self.simple_pocket("left pocket",
	  left_pocket1, left_pocket2, inch(0.25), "")
	self.simple_pocket("right pocket",
	  right_pocket1, right_pocket2, inch(0.25), "")

	# Relief Hole Locations:
	relief_diameter = inch("7/32")
	wall_dy_pitch = wall.dy_pitch
	relief_dx = inch("3/8")
	nw_relief = self.point(self.w.x + relief_dx,
	  wall_dy_pitch.half(), self.t.z)
	sw_relief = self.point(self.w.x + relief_dx,
	  -wall_dy_pitch.half(), self.t.z)
	ne_relief = self.point(self.e.x - relief_dx,
	  wall_dy_pitch.half(), self.t.z)
	se_relief = self.point(self.e.x - relief_dx,
	  -wall_dy_pitch.half(), self.t.z)

	# Mill relief holes after pockets:
	self.cnc_flush()

	self.hole_through("NW relief hole", relief_diameter, nw_relief, "u")
	self.hole_through("NE relief hole", relief_diameter, ne_relief, "u")
	self.hole_through("relief hole SW", relief_diameter, sw_relief, "u")
	self.hole_through("relief hole SE", relief_diameter, se_relief, "u")

	if False:
	    self.boundary_trim("Exterior Trim", inch("1/16"), "t")

	    # Make wall mounting holes:
	    self.vice_position("mount edge on in vice", w, bw, sw)
	    self.screw_hole("top plate NW side hole", "6-32", \
				 hole_place_nw, hole_place_nw_end, "du")
	    self.screw_hole("top plate SW side hole", "6-32", \
				 hole_place_sw, hole_place_sw_end, "du")
	    self.vice_position("mount edge on in vice", e, be, ne)
	    self.screw_hole("top plate NE side hole", "6-32", \
				 hole_place_ne, hole_place_ne_end, "du")
	    self.screw_hole("top plate SE side hole", "6-32", \
				 hole_place_se, hole_place_se_end, "du")
	    #print "w=", w, "tw=", tw, "nw=", nw

class Shaft(Part):

    def __init__(self, parent):

	# Initialize the parent class object:
	Part.__init__(self, "shaft", parent)

	# Initialize all accessible fields:
	self.diameter = inch(0.750)
	self.height = inch(1.500)

    def construct(self):
	top = self._parent
	top_plate = top.top_plate

	rod_b = self.point(zero, zero,
	  top_plate.t.z - top_plate.shaft_depth)
	rod_t = self.point_new(zero, zero, rod_b.z + self.height)

	self.rod("purple", "aluminum", rod_b, rod_t, self.diameter, 0)

def shaft_part(parent):
    if shaft.construct_mode():
	    print "Construct shaft"
	    shaft.vice_position("mount in vice long-wise", b, bn, be)
	    shaft.screw_hole("center", "6-32", b, o, "pdu")

    return shaft.done()

class Wall(Part):
    """ side wall design """

    def __init__(self, parent):
	""" Part: Initialize *self* with *parent* and *coordinates*. """

	paste = parent
	self.thickness = inch("1/8")
	self.dy_pitch = zero

	Part.__init__(self, "wall", parent)

    def construct(self):
	""" Wall: """

	paste = self._parent
	top = paste.top
	top_plate = top.top_plate
	holder = paste.holder
	support = holder.support

	dy_pitch = self.dy_pitch = paste.dy - inch("1/2")

	## Find associated *Part*'s:
	corner1 = self.point(-paste.dx.half(),
	  -paste.dy.half(), -paste.dz.half())
	corner2 = self.point(-paste.dx.half() + self.thickness,
	  paste.dy.half(), paste.dz.half())
	self.block_corners(corner1, corner2, "green", "aluminum")

	extra = inch(0.25)
	self.extra_xyz(zero, extra, extra)

	#print "Construct wall"
	self.vice_position("mount flat in vice", self.e, self.xne, self.xte)
	self.tooling_plate("tooling plate", "1Ase 1Bsw 2Ae 2Bw")
	self.tooling_plate_mount("Mount on tooling plate")
	self.boundary_trim("Exterior Trim", inch("1/16"), "t")

	self.screw_through("TNW", "6-32",
	  self.point(self.w.x, dy_pitch.half(), top_plate.w.z), "u")
	self.screw_through("TSW", "6-32",
	  self.point(self.w.x, -dy_pitch.half(), top_plate.w.z), "u")
	self.screw_through("BNW", "6-32",
	  self.point(self.w.x, dy_pitch.half(), support.w.z), "u")
	self.screw_through("BSW", "6-32",
	  self.point(self.w.x, -dy_pitch.half(), support.w.z), "u")
    
class Holder(Part):
    """ paste design. """

    def __init__(self, parent):
	self.support = Support(self)
	self.clamp = Clamp(self)

	Part.__init__(self, "holder", parent)

	self.syringe_diameter = inch(0.75)

    def construct(self):
	self.place(self.support, "support", self.o)
	self.place(self.clamp, "clamp", self.o)

class Support(Part):
    """ Support design """

    def __init__(self, parent):
	self.thickness = inch("1/4")
	Part.__init__(self, "support", parent)

    def construct(self):
	# Find associated {Part}'s:
	holder = self._parent
	clamp = holder.clamp
	support = holder.support
	paste = holder._parent
	wall = paste.wall
	top = paste.top
	top_plate = top.top_plate

	# Figure out where all the wall mount holes go:
	relief_dx = inch("3/8")
	nw_hole_start = self.point(self.w.x, wall.dy_pitch.half(), self.w.z)
	nw_hole_end = nw_hole_start.x_adjust(relief_dx)
	ne_hole_start = self.point(self.e.x, wall.dy_pitch.half(), self.w.z)
	ne_hole_end = ne_hole_start.x_adjust(-relief_dx)

	# These wall mount holes go all the way through to the clamp edge:
	sw_hole_start = self.point(self.w.x, -wall.dy_pitch.half(), self.w.z)
	sw_hole_end = self.point(clamp.w.x, -wall.dy_pitch.half(), self.w.z)
	se_hole_start = self.point(self.e.x, -wall.dy_pitch.half(), self.w.z)
	se_hole_end = self.point(clamp.e.x, -wall.dy_pitch.half(), self.w.z)

	# The two clamp holes go all through the support:
	w_hole_start = self.point(-clamp.support_hole_pitch.half(),
	  self.n.y, self.n.z)
	w_hole_end = self.point(-clamp.support_hole_pitch.half(),
	  zero, self.n.z)
	e_hole_start = self.point(clamp.support_hole_pitch.half(),
	  self.n.y, self.n.z)
	e_hole_end = self.point(clamp.support_hole_pitch.half(),
	  zero, self.n.z)

	extra = inch(0.25)
	self.extra_xyz(extra, extra, zero)
	corner1 = self.point(top_plate.w.x, top_plate.s.y, wall.b.z)
	corner2 = self.point(top_plate.e.x,
	  top_plate.n.y, wall.b.z + self.thickness)
        self.block_corners(corner1, corner2, "red", "plastic")

	#Top Face tooling
	self.vice_position("mount flat in vice", self.t, self.xtn, self.xtw)
	self.tooling_plate("tooling plate", "1As 1Bs")
	self.tooling_plate_mount("mount tooling plate")

	self.hole_through("syringe", holder.syringe_diameter, self.t, "u")

	self.cnc_flush()
	relief_diameter = inch("7/32")
	self.hole_through("NW relief hole", relief_diameter, \
	  self.point(self.w.x + relief_dx, wall.dy_pitch.half(), self.t.z), "u")
	self.hole_through("NE releif hole", relief_diameter, \
	  self.point(self.e.x - relief_dx, wall.dy_pitch.half(), self.t.z), "u")

	self.simple_pocket("clamp gap",
	  self.point(clamp.bsw.x, clamp.bsw.y - inch("1/4"), clamp.bsw.z),
	  clamp.tne, inch("3/16"), "t")

	self.boundary_trim("Exterior Trim", inch("1/16"), "tu")

	# West wall mount holes:
	support.vice_position("mount edge on in vice", self.w, self.tw, self.nw)
	self.screw_hole("NW wall hole", "6-32",
	  nw_hole_start, nw_hole_end, "du")
	self.screw_hole("SW wall hole", "6-32",
	  sw_hole_start, sw_hole_end, "du")

	# East wall mount holes:
	self.vice_position("mount edge on in vice", self.e, self.te, self.se)
	self.screw_hole("NE wall hole", "6-32",
	  ne_hole_start, ne_hole_end, "du")
	self.screw_hole("SE wall hole", "6-32",
	  se_hole_start, se_hole_end, "du")

	# North clamp holes:
	self.vice_position("mount edge on in vice", self.n, self.bn, self.nw)
	self.screw_hole("W clamp hole", "6-32",
	  w_hole_start, w_hole_end, "du")
	self.screw_hole("E clamp hole", "6-32",
	  e_hole_start, w_hole_end, "du")

class Clamp(Part):
    """ top_plate design """

    def __init__(self, parent):
	Part.__init__(self, "clamp", parent)
	self.support_hole_pitch = zero

    def construct(self):
	# Find associated {Part}'s:
	holder = self._parent
	support = holder.support

	# Initialize the {clamp} material:
	self.dx = inch(1.750)
	syringe_diameter = self.syringe_diameter = holder.syringe_diameter
	x_extra = inch(1.0)
	corner1 = self.point(-self.dx.half(), support.s.y, support.b.z)
	corner2 = self.point(self.dx.half(), zero, support.t.z)
	extra = inch(0.25)
	self.extra_xyz(extra, extra, zero)
	self.block_corners(corner1, corner2, "orange", "plastic")

	# Load {clamp} into the vice:
	self.vice_position("mount flat in vice", self.t, self.xtn, self.xtw)
	self.tooling_plate("tooling plate", "")
	self.tooling_plate_mount("mount tooling plate")

	# Mill out the syringe hole:
	self.hole_through("syringe hole", syringe_diameter, self.tn, "u")

	# Mill out the exterior contour of {clamp}:
	self.cnc_flush()
	outside_radius = inch(0.025)
	self.corner("TSE", self.tse, outside_radius)
	self.corner("TSW", self.tsw, outside_radius)
	inside_radius = inch("3/16")
	self.corner("TNW", self.tnw, inside_radius)
	self.corner("TNE", self.tne, inside_radius)
	self.contour("exterior trim", self.t, self.b, inch(.125), "tu")

	# Drill the clamp holes:
	self.vice_position("mount edge on in vice", self.s, self.ts, self.sw)
	support_hole_pitch = self.support_hole_pitch = inch(1.25)
	hole_place_w = \
	  self.point(-support_hole_pitch.half(), self.s.y, self.s.z)
	hole_place_e = \
	  self.point(support_hole_pitch.half(), self.s.y, self.s.z)
	self.screw_through("side hole", "6-32", hole_place_w, "u")
	self.screw_through("side hole", "6-32", hole_place_e, "u")

paste = Paste(None)
paste.process()
