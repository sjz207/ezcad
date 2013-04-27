#!/usr/bin/env python

from EZCAD2 import *

# These two values are used all over the place:
inch = Length.inch
zero = inch(0.0)

class Paste(Part):
    """ {Paste}: Solder paste holder assembly. """ 

    def __init__(self, parent):
	""" {Paste}: Initialize the paste assembly to contain
	    the top assembly, wall, and bottom holder. """

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
	""" {Paste}: Construct the final paste assembly that consists of the
	    top assembly, two walls, and the bottom holder. """

	self.place(self.wall, "west_wall", self.o)
	self.place(self.wall, "east_wall",
	  self.point(self.dx - self.wall.thickness, zero, zero))
	self.place(self.top, "top", self.o)
	self.place(self.holder, "holder", self.o)

class Top(Part):
    """ {Top}: Top assembly. """

    def __init__(self, parent):
	""" {Top}: Initialize the top assembly the consists of the shaft
	    and top plate. """

	# Create the children {Part}'s in the {Part} tree:
	self.shaft = Shaft(self)
	self.top_plate = Top_Plate(self)
	self.shaft = Shaft(self)
	self.collet_depth = inch(0.100)

	# Initilize the {Part} parent class object:
	Part.__init__(self, "top", parent)

    def construct(self):
	""" {Top}: Contruct the top assembly consisting of the shaft and the
	    top plate. """

	self.place(self.top_plate, "top_plate", self.o)
	self.place(self.shaft, "shaft", self.o)

class Top_Plate(Part):
    """ {Top_Plate}: The top plate connects the shaft to the two walls. """

    def __init__(self, parent):
	""" {Top_Plate}: Initialize the top plate. """

	# Initilize the {Part} parent class object:
	Part.__init__(self, "top_plate", parent)
	self.original_thickness = inch("1/2")
	self.shaft_depth = inch("1/8")
	self.final_thickness = zero

    def construct(self):
	""" {Top_Plate}: Construct the top plate. """

	# Extract the various {Part}'s:
	top = self._parent
	shaft = top.shaft
	paste = top._parent
	wall = paste.wall

	# Update {final_thickness}:
	final_thickness = \
	  self.final_thickness = self.original_thickness - top.collet_depth

	# Construct the original block.  This is a little tricky, becuase
	# the we want the top edge of {final_thickness} to align with the
	# top of the walls:
	extra = inch(0.25)
	self.extra_xyz(extra, extra, zero)
	corner1 = self.point(wall.e.x, wall.s.y,
	  wall.t.z - self.final_thickness)
	corner2 = self.point(-wall.e.x, wall.n.y,
	  wall.t.z - self.final_thickness + self.original_thickness)
	self.block_corners(corner1, corner2, "dark_blue", "aluminum")

	# Mount up the block:
	self.vice_position("mount flat in vice", self.t, self.xtn, self.xtw)
	self.tooling_plate("tooling plate", "1As 1Bs")
	self.tooling_plate_mount("mount tooling plate")

	# Put center hole all the way through to drain coolant:
	self.screw_through("center", "6-32", self.t, "c")
	self.cnc_flush()

	# Machine out a pocket for the shaft:
	shaft_depth = inch("3/8")
	collet_inside_diameter = inch(1.250)
	collet_outside_diameter = inch(1.500)
	collet_depth = top.collet_depth
	collet_depth_point = self.point(zero, zero, self.t.z - collet_depth)
	shaft_depth_point = self.point(zero, zero, self.t.z - shaft_depth)

	self.hole("inside collet", collet_inside_diameter,
	  self.t, collet_depth_point, "m")
	self.hole("shaft hole", shaft.diameter + inch(0.010), self.t,
	  shaft_depth_point, "m")

	# Remove a bunch of material from around the collet:
	self.vertical_lathe("outside collet", \
	  self.t, collet_depth_point, collet_outside_diameter, \
	  collet_outside_diameter + inch(1.25), "")

	# Remove the remaining stuff after the vertical lathe using
	# a left and right simple pocket:
	left_w = self.w.x - inch(0.25)
	left_e = -collet_outside_diameter.half() - inch(0.05)
	left_s = self.s.y - inch("1/16")
	left_n = self.n.y + inch("1/16")
	left_b = self.t.z - collet_depth
	left_t = self.t.z

	self.simple_pocket("left pocket",
	  self.point(left_w, left_s, left_b),
	  self.point(left_e, left_n, left_t), inch(0.25), "")

	right_w = collet_outside_diameter.half() + inch(0.05)
	right_e = self.e.x + inch(0.25)
	right_s = self.s.y - inch("1/16")
	right_n = self.n.y + inch("1/16")
	right_b = self.t.z - collet_depth
	right_t = self.t.z

	self.simple_pocket("right pocket",
	  self.point(right_w, right_s, right_b),
	  self.point(right_e, right_n, right_t), inch(0.25), "")

	# Relief Hole Locations:
	relief_diameter = inch("5/16")
	wall_dy_pitch = wall.dy_pitch
	relief_dx = inch("3/8")
	relief_w = self.w.x + relief_dx
	relief_e = self.e.x - relief_dx
	relief_n = wall_dy_pitch.half()
	relief_s = -relief_n
	relief_z = self.t.z

	# Mill relief holes after pockets:
	self.cnc_flush()
	self.hole_through("NW relief hole", relief_diameter,
	  self.point(relief_w, relief_n, relief_z), "u")
	self.hole_through("NE relief hole", relief_diameter,
	  self.point(relief_e, relief_n, relief_z), "u")
	self.hole_through("SW relief hole", relief_diameter,
	  self.point(relief_w, relief_s, relief_z), "u")
	self.hole_through("SE relief hole", relief_diameter,
	  self.point(relief_e, relief_s, relief_z), "u")

	# Trim the outer boundary:
	self.boundary_trim("Exterior Trim", inch("1/16"), "t")

	# Make wall mounting holes:

	# Specify the various wall coordinates:
	wall_z = self.b.z + self.final_thickness.half()
	wall_w_start = self.w.x
	wall_w_end = wall_w_start + relief_dx
	wall_e_start = self.e.x
	wall_e_end = wall_e_start - relief_dx
	wall_n = wall_dy_pitch.half()
	wall_s = -wall_n

	# Mount it up and do the west edge holes:
	self.vice_position("Mount West edge up in vice",
	  self.w, self.bw, self.sw)
	self.screw_hole("NW wall hole", "6-32",
	  self.point(wall_w_start, wall_n, wall_z),
	  self.point(wall_w_end, wall_n, wall_z), "du")
	self.screw_hole("SW wall hole", "6-32",
	  self.point(wall_w_start, wall_s, wall_z),
	  self.point(wall_w_end, wall_s, wall_z), "du")

	# Mount it up and do the east edge holes:
	self.vice_position("Mount East edge up on in vice",
	  self.e, self.be, self.ne)
	self.screw_hole("NE wall hole", "6-32", \
	  self.point(wall_e_start, wall_n, wall_z),
	  self.point(wall_e_end, wall_n, wall_z), "du")
	self.screw_hole("SE wall hole", "6-32", \
	  self.point(wall_e_start, wall_s, wall_z),
	  self.point(wall_e_end, wall_s, wall_z), "du")

class Shaft(Part):
    """ {Shaft} to mount into mill spindle. """


    def __init__(self, parent):
	""" {Shaft}: Initialize shaft. """

	# Initialize the parent class object:
	Part.__init__(self, "shaft", parent)

	# Initialize all accessible fields:
	self.diameter = inch(0.750)
	self.height = inch(1.500)

    def construct(self):
	""" {Shaft}: Construct shaft. """
	top = self._parent
	top_plate = top.top_plate

	rod_bottom = self.point(zero, zero,
	  top_plate.t.z - top_plate.shaft_depth)
	rod_top = self.point_new(zero, zero, rod_bottom.z + self.height)

	self.rod("purple", "aluminum", rod_bottom, rod_top, self.diameter, 0)

	#self.vice_position("mount in vice long-wise", self.b, self.bn, self.be)
	#self.screw_hole("center", "6-32", self.b, self.o, "pdu")

class Wall(Part):
    """ {Wall}: side wall """

    def __init__(self, parent):
	""" {Wall}: Initialize side wall. """

	paste = parent
	self.thickness = inch("1/8")
	self.dy_pitch = zero

	Part.__init__(self, "wall", parent)

    def construct(self):
	""" Wall: Construct side wall. """

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

	self.screw_through("TNW", "6-32", self.point(self.w.x, dy_pitch.half(),
	  self.t.z - top_plate.final_thickness.half()), "u")
	self.screw_through("TSW", "6-32", self.point(self.w.x, -dy_pitch.half(),
	  self.t.z - top_plate.final_thickness.half()), "u")
	self.screw_through("BNW", "6-32",
	  self.point(self.w.x, dy_pitch.half(), support.w.z), "u")
	self.screw_through("BSW", "6-32",
	  self.point(self.w.x, -dy_pitch.half(), support.w.z), "u")
    
class Holder(Part):
    """ {Holder}: Bottom holder for paste syringe. """

    def __init__(self, parent):
	""" {Holder}: Initalize bottom holder assembly. """
	self.support = Support(self)
	self.clamp = Clamp(self)

	Part.__init__(self, "holder", parent)

	self.syringe_diameter = inch(0.75)

    def construct(self):
	""" {Holder}: Construct bottom holder assembly. """

	self.place(self.support, "support", self.o)
	self.place(self.clamp, "clamp", self.o)

class Support(Part):
    """ {Support}: Support the clamps on one half of the solder syringe. """

    def __init__(self, parent):
	""" {Support}: Initialize the support."""
	self.thickness = inch("1/4")
	Part.__init__(self, "support", parent)

    def construct(self):
	""" {Support}: Construct the support. """

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
    """ {Clamp}: Clamp that presses the solder syringe into the support. """

    def __init__(self, parent):
	""" {Clamp}: Initialize clamp object. """

	Part.__init__(self, "clamp", parent)
	self.support_hole_pitch = zero

    def construct(self):
	""" {Clamp}: Construct the clamp to press against solder syringe. """

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

# Create the {Paste} assembly, generate VRML (.wrl) and CNC (.ngc) files:
paste = Paste(None)
paste.process()
