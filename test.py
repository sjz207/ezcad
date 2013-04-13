#!/usr/bin/python

from EZCAD2 import *

class Paste(Part):
    """ Paste: Solder paste holder assembly. """ 

    def __init__(self, parent):
	""" Paste_Assembly: Initialize *self* to have """

	# List the children {Parts}'s in the {Part} tree:
	self.top = Top(self)
	self.holder = Holder(self)
	self.wall = Wall(self)

	# Initialize the parent assembly:
	Part.__init__(self, "paste", parent)

	# Part origin is at bottom aligned with center axis:

	# Initialize some dimensions:
	inch = Length.inch
	zero = inch(0)

	self.dz = inch(4.000)
	self.dy = inch(2.000)
	self.dx = inch(3.000)

    def dimensions(self):
	""" Paste:  Dimensions discovery mode. """

	inch = Length.inch
	zero = inch(0)

	origin = self.point(zero, zero, zero)
	self.place(self.top, "top", origin)
	self.place(self.holder, "holder", origin)
	self.place(self.wall, "west_wall", origin)
	self.place(self.wall, "east_wall", origin)

class Top(Part):

    def __init__(self, parent):
	""" Top: """

	self.shaft = Shaft(self)
	self.top_plate = Top_Plate(self)

	Part.__init__(self, "top", parent)

    def dimensions(self):
	pass

def top():
    if top.dimensions_mode():
	inch = Length.inch
	z = inch(0)
	paste = top.part("..")

	top_plate_z = top_plate.length("top_plate_z")

	# Place shaft:
	shaft_place = top.point_xyz_set("shaft_place", z, z, top_plate_z.half())
	top.place(shaft, "shaft", shaft_place)

	# Place top plate:
	top_plate_place = top.point_new(z, z, z)
	top.place(top_plate, "top_plate", top_plate_place)
    
    return top.done()

class Top_Plate(Part):
    """ top_plate design """

    def __init__(self, parent):

	Part.__init__(self, "top_plate", parent)

    def dimensions(self):
	inch= Length.inch
	zero = inch(0)

	#length_x = top_plate.length_set("length_x", inch(4))
	#width_y = top_plate.length_set("width_y", inch(1.75))
	#top_plate_z = top_plate.length_set("top_plate_z", inch(0.5))
	#shaft = top_plate.part("../shaft")
	#shaft_diameter = shaft.length("shaft_diameter")
	#shaft_depth = top_plate.length_set("shaft_depth", inch(3.0/8.0))
	#collet_depth = top_plate.length_set("collet_depth", inch(0.1))
	#collet_inside_diameter = inch(1.25)
	#collet_outside_diameter = inch(1.50)
	#relief_hole = top_plate.length_set("relief_hole", inch("5/16"))

	##Hole drill points
	#hole_place_nw = top_plate.point_xyz_set("hole_place_nw", \
	#				       -length_x.half(), inch(0.5), \
	#				       zero - collet_depth.half())
	#hole_place_sw = top_plate.point_xyz_set("hole_place_sw", \
	#				       -length_x.half(), -inch(0.5), \
	#				       zero - collet_depth.half())
	#hole_place_ne = top_plate.point_xyz_set("hole_place_ne", \
	#				       length_x.half(), inch(0.5), \
	#				       zero - collet_depth.half())
	#hole_place_se = top_plate.point_xyz_set("hole_place_se", \
	#				       length_x.half(), -inch(0.5), \
	#				       zero - collet_depth.half())
	##Hole end points
	#hole_place_nw_end = hole_place_nw.xz_adjust(inch(0.5), -collet_depth)
	#hole_place_sw_end = hole_place_sw.xz_adjust(inch(0.5), -collet_depth)
	#hole_place_ne_end = hole_place_ne.xz_adjust(-inch(0.5), -collet_depth)
	#hole_place_se_end = hole_place_se.xz_adjust(-inch(0.5), -collet_depth)

	##Relief Hole Locations
	#hole_place_nw_rel = hole_place_nw_end.z_adjust(top_plate_z.half())
	#hole_place_sw_rel = hole_place_sw_end.z_adjust(top_plate_z.half())
	#hole_place_ne_rel = hole_place_ne_end.z_adjust(top_plate_z.half())
	#hole_place_se_rel = hole_place_se_end.z_adjust(top_plate_z.half())

	##Pocket locations
	#pocketL1 = top_plate.point_new(-length_x.half()- inch(0.25), \
	#			       -width_y.half(), \
	#			       top_plate_z.half() - collet_depth)
	#pocketL2 = top_plate.point_new(-collet_outside_diameter.half() \
	#			       - inch(0.05), width_y.half(), \
	#			       top_plate_z.half())
	#pocketR1 = top_plate.point_new(length_x.half() + inch(0.25), \
	#			       -width_y.half(), \
	#			       top_plate_z.half() - collet_depth)
	#pocketR2 = top_plate.point_new(collet_outside_diameter.half() \
	#			       + inch(0.05), width_y.half(), \
	#			       top_plate_z.half())
	#print "Right Pocket 1:", pocketR1
	#print "Right Pocket 2:", pocketR2
	#
	#collet_depth_point = \
	#  top_plate.point_new(zero, zero, top_plate_z.half() - collet_depth)
	#shaft_depth_point = \
	#  top_plate.point_new(zero, zero, top_plate_z.half() - shaft_depth)
	##print "Collet Depth Point:", collet_depth_point

	#diagonal = top_plate.point_new(length_x, width_y, top_plate_z)
	#o = top_plate.point("$O")
	#t = top_plate.point("$T")
	#w = top_plate.point("$W")
	#e = top_plate.point("$E")
	#ne = top_plate.point("$NE")
	#bw = top_plate.point("$BW")
	#tn = top_plate.point("$TN")
	#be = top_plate.point("$BE")
	#tw = top_plate.point("$TW")
	#sw = top_plate.point("$SW")

	#extra = inch(0.25)
	#top_plate.extra_xyz(extra, extra, zero)
	#xtn = top_plate.point("$XTN")
	#xtw = top_plate.point("$XTW")
	#
	#top_plate.block_diagonal(diagonal, "dark_blue", "aluminum")

def top_plate(parent):
    if top_plate.construct_mode():
	    print "Construct top_plate"
	    #print "xtn=", xtn, "xtw=", xtw
	    top_plate.chamfers(inch(0.025), zero)
	    top_plate.vice_position("mount flat in vice", t, xtn, xtw)
	    top_plate.tooling_plate("tooling plate", "")
	    top_plate.tooling_plate_mount("mount tooling plate")

	    # Put center hole all the way through to drain coolant:
	    top_plate.screw_through("center", "6-32", t, "c")

	    top_plate.cnc_flush()

	    top_plate.hole("inside collet", collet_inside_diameter, \
	      t, collet_depth_point, "m")
	    top_plate.hole("shaft hole", shaft_diameter + inch(0.010), t, \
	      shaft_depth_point, "m")
	    top_plate.vertical_lathe("outside collet", \
	      t, collet_depth_point, collet_outside_diameter, \
				     collet_outside_diameter + inch(1.25), "")
	    top_plate.simple_pocket("left pocket", pocketL1, pocketL2, \
	      inch(0.25), "")
	    top_plate.simple_pocket("right pocket", pocketR1, pocketR2, \
	      inch(0.25), "")

	    # Mill relief holes after pockets:
	    top_plate.cnc_flush()

	    top_plate.hole_through("relief hole NW", relief_hole, \
				   hole_place_nw_rel, "u")
	    top_plate.hole_through("relief hole NE", relief_hole, \
				   hole_place_ne_rel, "u")
	    top_plate.hole_through("relief hole SW", relief_hole, \
				   hole_place_sw_rel, "u")
	    top_plate.hole_through("relief hole SE", relief_hole, \
				   hole_place_se_rel, "u")

	    top_plate.boundary_trim("Exterior Trim", inch("1/16"), "t")

	    # Make wall mounting holes:
	    top_plate.vice_position("mount edge on in vice", w, bw, sw)
	    top_plate.screw_hole("top plate NW side hole", "6-32", \
				 hole_place_nw, hole_place_nw_end, "du")
	    top_plate.screw_hole("top plate SW side hole", "6-32", \
				 hole_place_sw, hole_place_sw_end, "du")
	    top_plate.vice_position("mount edge on in vice", e, be, ne)
	    top_plate.screw_hole("top plate NE side hole", "6-32", \
				 hole_place_ne, hole_place_ne_end, "du")
	    top_plate.screw_hole("top plate SE side hole", "6-32", \
				 hole_place_se, hole_place_se_end, "du")
	    #print "w=", w, "tw=", tw, "nw=", nw

    return top_plate.done()

class Shaft(Part):

    def __init__(self, parent):

	Part.__init__(self, "shaft", parent)


    def dimensions(self):
	inch= Length.inch
	zero = inch(0)

	#top = shaft.part("..")
	#top_plate = top.part("top_plate")

	#top_plate_shaft_depth = top_plate.length("shaft_depth")
	#shaft_z = inch(1.375) + top_plate_shaft_depth

	#shaft_diameter = shaft.length_set("shaft_diameter", inch(0.75))
	#shaft_above = shaft_z - top_plate_shaft_depth
  
	#rod_start = shaft.point_new(zero, zero, -top_plate_shaft_depth)
	#rod_end = shaft.point_new(zero, zero, shaft_above)

	#o = shaft.point("$O")
	#t = shaft.point("$T")
	#b = shaft.point("$B")
	#bn = shaft.point("$BN")
	#be = shaft.point("$BE")
	#bw = shaft.point("$BW")

	#shaft.rod("purple", "aluminum", rod_start, rod_end, shaft_diameter, 0)

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

	Part.__init__(self, "wall", parent)

    def dimensions(self):
	""" Wall: """

	## Find associated *Part*'s:
	#paste = self._parent
	#top = paste.top
	#top_plate = top.top_plate
	#holder = paste.holder
	#support = holder.support

	## Extract some values from {top_plate and paste assembly}:
	#width_y = top_plate.length("width_y")
	#top_plate_z = top_plate.length("top_plate_z")
	#height_z = paste.length("height_z")
	#collet_depth = top_plate.length("collet_depth")
	##hole_place_n = top_plate.point("hole_place_n")
	##hole_place_s = top_plate.point("hole_place_s")
	#inch= Length.inch
	#zero = inch(0)
	##Holes to line up with top plate
	#hole_place_nwt = paste.point_subtract("top/top_plate.hole_place_nw", \
	#				     "wall_w.$O")
	#hole_place_swt = paste.point_subtract("top/top_plate.hole_place_sw", \
	#				     "wall_w.$O")
	#
	##Holes to line up with support plate
	#hole_place_nwb = paste.point_subtract("holder/support.hole_place_nw", \
	#				     "wall_w.$O")
	#hole_place_swb = paste.point_subtract("holder/support.hole_place_sw", \
	#				     "wall_w.$O")
	#
	#wall_thickness = wall.length_set("wall_thickness", inch("1/8"))

	#diagonal = top_plate.point_new(wall_thickness, width_y, \
	#			       height_z - top_plate_z + collet_depth)

	#o = wall.point("$O")
	#t = wall.point("$T")
	#e = wall.point("$E")
	#ne = wall.point("$NE")
	#te = wall.point("$TE")

	#extra = inch(0.25)
	#wall.extra_xyz(zero, extra, extra)
	#xne = wall.point("$XNE")
	#xte = wall.point("$XTE")

	#wall.block_diagonal(diagonal, "green", "aluminum")
	pass

def wall():
    if wall.construct_mode():
	    print "Construct wall"
	    wall.chamfers(inch(0.025), zero)
	    wall.vice_position("mount flat in vice", e, xne, xte)
	    #wall.tooling_plate("tooling plate", "1Ase 1Bsw 2Ae 2Bw")
	    wall.tooling_plate("tooling plate", "")
	    wall.tooling_plate_mount("mount tooling plate")

	    wall.boundary_trim("Exterior Trim", inch("1/16"), "t")

	    wall.screw_through("side hole", "6-32", hole_place_nwt, "u")
	    wall.screw_through("side hole", "6-32", hole_place_swt, "u")
	    wall.screw_through("side hole", "6-32", hole_place_nwb, "u")
	    wall.screw_through("side hole", "6-32", hole_place_swb, "u")
    
    return wall.done()

class Holder(Part):
    """ paste design. """

    def __init__(self, parent):

	self.support = Support(self)
	self.clamp = Clamp(self)
	Part.__init__(self, "holder", parent)

    def dimensions(self):
	#inch = Length.inch
	#z = inch(0)

	#clamp_y = clamp.length("clamp_y")

	## Place support plate:
	#support_place = holder.point_xyz_set("tp_place", z, z, z)
	#holder.place(support, "support", support_place)
	
	## Place clamp:
	#clamp_place = holder.point_new(z, -clamp_y.half(), z)
	#holder.place(clamp, "clamp", clamp_place)
	pass

class Support(Part):
    """ Support design """

    def __init__(self, parent):
	Part.__init__(self, "support", parent)

    def dimensions(self):
	#inch= Length.inch
	#zero = inch(0)

	## Find associated {Part}'s:
	#holder = support.part("..")
	#clamp = holder.part("clamp")
	#paste = holder.part("..")
	#top = paste.part("top")
	#top_plate = top.part("top_plate")

	#clamp_y = clamp.length("clamp_y")
	#support_x = \
	#  support.length_set("support_x", top_plate.length("length_x"))
	#support_y = support.length_set("support_y", top_plate.length("width_y"))
	#support_z = \
	#  support.length_set("support_z", top_plate.length("top_plate_z"))
	#print "clamp_y=", clamp_y, "support_y=", support_y

	## Get some bounding box points:
	#o = support.point("$O")
	#t = support.point("$T")
	#e = support.point("$E")
	#n = support.point("$N")
	#w = support.point("$W")
	#s = support.point("$S")
	#ne = support.point("$NE")
	#nw = support.point("$NW")
	#sw = support.point("$SW")
	#se = support.point("$SE")
	#te = support.point("$TE")
	#tn = support.point("$TN")
	#ts = support.point("$TS")
	#tw = support.point("$TW")
	#bn = support.point("$BN")

	## Extract some values from {clamp}:
	#bridge_y = support_y - clamp_y
	#support_hole_pitch = clamp.length("support_hole_pitch")
	#hole_place_w = n.x_adjust(-support_hole_pitch.half())
	#hole_place_w_end = hole_place_w.y_adjust(-bridge_y)
	#hole_place_e = n.x_adjust(support_hole_pitch.half())
	#hole_place_e_end = hole_place_e.y_adjust(-bridge_y)

	#print "hole_place_w=", hole_place_w, \
	#  "hole_place_w_end=", hole_place_w_end


	#support.point_set("hole_place_w", hole_place_w)
	#support.point_set("hole_place_e", hole_place_e)
	#relief_hole = top_plate.length("relief_hole")
	#
	##Top plate holes
	#hole_nw = paste.point_subtract("top/top_plate.hole_place_nw",\
	#				    "holder/support.$O")
	#hole_sw = paste.point_subtract("top/top_plate.hole_place_sw",\
	#				    "holder/support.$O")
	#hole_ne = paste.point_subtract("top/top_plate.hole_place_ne",\
	#				    "holder/support.$O")
	#hole_se = paste.point_subtract("top/top_plate.hole_place_se",\
	#				    "holder/support.$O")
	##Adjust for z=0
	#hole_place_nw = hole_nw.z_adjust(paste.length("height_z") + \
	#			       top_plate.length("collet_depth").half())
	#hole_place_sw = hole_sw.z_adjust(paste.length("height_z") + \
	#			       top_plate.length("collet_depth").half())
	#hole_place_ne = hole_ne.z_adjust(paste.length("height_z") + \
	#			       top_plate.length("collet_depth").half())
	#hole_place_se = hole_se.z_adjust(paste.length("height_z") + \
	#			       top_plate.length("collet_depth").half())

	##Hole end points
	#hole_place_nw_end = hole_place_nw.x_adjust(inch(0.5))
	#hole_place_sw_end = hole_place_sw.x_adjust(clamp.length("clamp_y"))
	#hole_place_ne_end = hole_place_ne.x_adjust(-inch(0.5))
	#hole_place_se_end = hole_place_se.x_adjust(-clamp.length("clamp_y"))

	##Relief hole points
	#hole_place_nw_rel = hole_place_nw_end.z_adjust(\
	#    top_plate.length("top_plate_z"))
	#hole_place_ne_rel = hole_place_ne_end.z_adjust(\
	#    top_plate.length("top_plate_z"))
	#
	#support.point_set("hole_place_nw", hole_place_nw)
	#support.point_set("hole_place_sw", hole_place_sw)
	#support.point_set("hole_place_ne", hole_place_ne)
	#support.point_set("hole_place_se", hole_place_se)
	#
	#syringe_diameter = clamp.length("syringe_diameter")
	#clamp_x = clamp.length("clamp_x")
	#clamp_y = clamp.length("clamp_y")
	#clamp_inside_radius = clamp.length("inside_radius")

	#support_diagonal = support.point_new(support_x, support_y, support_z)

	#pocket1 = support.point_new(-clamp_x.half(), \
	#		      -clamp_y - clamp_inside_radius, -support_z.half())
	#pocket2 = support.point_new(clamp_x.half(), zero, support_z.half())
	#

	#extra = inch(0.25)
	#support.extra_xyz(extra, extra, zero)
	#xtn = support.point("$XTN")
	#xtw = support.point("$XTW")

	#support.block_diagonal(support_diagonal, "red", "plastic")
	pass

def support():
    if support.construct_mode():
	    print "Construct support"
	    support.chamfers(inch(0.025), zero)
	    #Top Face tooling
	    support.vice_position("mount flat in vice", t, xtn, xtw)
	    support.tooling_plate("tooling plate", "")
	    support.tooling_plate_mount("mount tooling plate")
	    #support.cnc_flush()
	    support.hole_through("syringe", syringe_diameter, t, "u")
	    support.hole_through("relief hole NW", relief_hole, \
				 hole_place_nw_rel, "u")
	    support.hole_through("relief hole NE", relief_hole, \
				 hole_place_ne_rel, "u")
	    support.simple_pocket("clamp gap", pocket1, pocket2, \
	      clamp_inside_radius, "t")
	    support.boundary_trim("Exterior Trim", inch("1/16"), "tu")
	    #West Face drill holes
	    support.vice_position("mount edge on in vice", w, tw, nw)
	    support.screw_hole("support NW side hole", "6-32", hole_place_nw, \
				 hole_place_nw_end, "du")
	    support.screw_hole("support SW side hole", "6-32", hole_place_sw, \
				 hole_place_sw_end, "du")

	    #East Face drill holes
	    support.vice_position("mount edge on in vice", e, te, se)
	    support.screw_hole("support NE side hole", "6-32", hole_place_ne, \
				hole_place_ne_end, "du")
	    support.screw_hole("support SE side hole", "6-32", hole_place_se, \
				 hole_place_se_end, "du")
	    #North Face drill holes
	    support.vice_position("mount edge on in vice", n, bn, nw)
	    support.screw_hole("side hole", "6-32",\
	      hole_place_w, hole_place_w_end, "du")
	    support.screw_hole("side hole", "6-32", \
	      hole_place_e, hole_place_e_end, "du")

    return support.done()

class Clamp(Part):
    """ top_plate design """

    def __init__(self, parent):
	Part.__init__(self, "clamp", parent)

    def dimensions(self):
	# Some useful values:
	inch= Length.inch
	zero = inch(0)

	# Find associated {Part}'s:
	holder = self._parent
	assert holder._name == "holder"
	support = holder.support

	# Extract some values from {support}:
	#support_y = support.support_y
	#support_z = support.support_z

	# Define some values for {clamp}:
	#support_hole_pitch = clamp.length_set("support_hole_pitch", inch(1.5))

	#syringe_diameter = clamp.length_set("syringe_diameter", inch(0.75))
	#clamp_x = clamp.length_set("clamp_x", syringe_diameter + inch(2))
	#clamp_x_new = clamp.length_set("clamp_x_new", \
	#			       syringe_diameter + inch(1.95))
	#clamp_y = clamp.length_set("clamp_y", support_y.half())
	#clamp_y_new = clamp.length_set("clamp_y_new", \
	#			       support_y.half()-inch(0.125))
	#clamp_z = clamp.length_set("clamp_z", support_z)
	#inside_radius = clamp.length_set("inside_radius", inch(3.0/16.0))
	#hole_place_w = clamp.point_xyz_set("hole_place_w", \
	#  -support_hole_pitch.half(), -clamp_y_new, zero)
	#hole_place_e = clamp.point_xyz_set("hole_place_e", \
	#  support_hole_pitch.half(), -clamp_y_new, zero)

	#outside_radius = inch(0.025)
	#clamp_diagonal = clamp.point_new(clamp_x_new, clamp_y_new, clamp_z)
	#syringe_point = clamp.point_new(zero, clamp_y_new.half(), clamp_z.half())
	#syringe_point_new = clamp.point_new(zero, clamp_y_new.half() \
	#					+ inch(0.125), clamp_z.half())
	# Lookup some bounding box values for {clamp}:
	#o = clamp.point("$O")
	#t = clamp.point("$T")
	#b = clamp.point("$B")      
	#w = clamp.point("$W")
	#s = clamp.point("$S")
	#nw = clamp.point("$NW")
	#sw = clamp.point("$SW")
	#tn = clamp.point("$TN")
	#ts = clamp.point("$TS")
	#tw = clamp.point("$TW")

	#extra = inch(0.25)
	#clamp.extra_xyz(extra, extra, zero)
	#xtn = clamp.point("$XTN")
	#xtw = clamp.point("$XTW")

	# Initialize the {clamp} material:
	#clamp.block_diagonal(clamp_diagonal, "orange", "plastic")
	pass

def clamp_part(parent):
    if clamp.construct_mode():
	    print "Construct clamp"
	    # Load {clamp} into the vice:
	    clamp.vice_position("mount flat in vice", t, xtn, xtw)
	    clamp.tooling_plate("tooling plate", "")
	    clamp.tooling_plate_mount("mount tooling plate")
	    clamp.chamfers(inch(0.025), zero)
	    # Mill out the syringe hole:
	    clamp.hole_through("syringe hole", \
			      syringe_diameter, syringe_point_new, "u")

	    # Mill out the exterior contour of {clamp}:
	    clamp.cnc_flush()
	    clamp.corner("TSE", clamp.point("$TSE"), outside_radius)
	    clamp.corner("TSW", clamp.point("$TSW"), outside_radius)
	    clamp.corner("TNW", clamp.point("$TNW"), inside_radius)
	    clamp.corner("TNE", clamp.point("$TNE"), inside_radius)
	    clamp.contour("exterior trim", t, b, inch(.125), "tu")
	    clamp.vice_position("mount edge on in vice", s, ts, sw)
	    clamp.screw_through("side hole", "6-32", hole_place_w, "u")
	    clamp.screw_through("side hole", "6-32", hole_place_e, "u")
    return clamp.done()

paste = Paste(None)
paste.process()
