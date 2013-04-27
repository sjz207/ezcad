#!/usr/bin/python

# Tasks:
#
# Bugs:
# - Combined contour plus countersinking does not get to Z-safe
# - Dowel pin does not work in all orientations
# - Work Offset computation is totally broken
# Python Library:
# - Add dimension descriptions
# Documentation:
# - Document screws
# - General update
# - Shop interface

import os
import math

# Forward class definitions:

class Angle:
    """ An {Angle} represents an angle. """

    pi = 3.14159265358979323846

    def __init__(self, scalar_radians):
	""" Angle: Initia	lize self to contain {scalar_radians}. """

	self.radians = float(scalar_radians)

    def __add__(self, angle):
	""" Angle: Return {angle} added to {self}. """

	return Angle(self.radians + angle.radians)

    def __div__(self, scalar):
	""" Angle: Return {self} divided by {scalar}. """

	return Angle(self.radians / scalar)

    def __eq__(self, angle):
	""" Angle: Return {True} if {self} is equal to {angle}. """

	return self.radians == angle.radians

    def __format__(self, fmt):
	""" Angle: Format {self} into a string and return it. """

	return str(self.radians * 180.0 / Angle.pi)

    def __ge__(self, angle):
	""" Angle: Return {True} if {self} is greater than or equal
	    to {angle}. """

	return self.radians >= angle.radians

    def __gt__(self, angle):
	""" Angle: Return {True} if {self} is greater than {angle}. """

	return self.radians > angle.radians

    def __le__(self, angle):
	""" Angle: Return {True} if {self} is less than or equal to {angle}. """

	return self.radians <= angle.radians

    def __lt__(self, angle):
	""" Angle: Return {True} if {self} is less than {angle}. """

	return self.radians < angle.radians

    def __mul__(self, scalar):
	""" Angle: Return {self} divided by {scalar}. """

	return Angle(self.radians * scalar)

    def __ne__(self, angle):
	""" Angle: Return {True} if {self} is not equal to {angle}. """

	return self.radians != angle.radians

    def __neg__(self):
	""" Angle: Return negative of {self}. """

	return Angle(-self.radians)

    def __rmul__(self, scalar):
	""" Angle: Return {self} divided by {scalar}. """

	return Angle(self.radians * scalar)

    def __str__(self):
	""" Angle: Return {self} as a string. """

	return str(self.radians * 180.0 / Angle.pi)

    def __sub__(self, angle):
	""" Angle: Return {angle} subtracted from {self}. """

	return Angle(self.radians - angle.radians)

    def cosine(self):
	""" Angle: Return the cosine of {self}. """

	return math.cos(self.radians)

    @staticmethod
    def deg(scalar_degrees):
	""" Angle: Convert {scalar_degrees} into an {Angle} and return it. """

	return Angle(scalar_degrees * Angle.pi / 180.0)

    def degrees(self):
	""" Angle: Convert {self} back into degrees and return it. """

	return self.radians * 180.0 / Angle.pi

    def half(self):
	""" Angle: Return half of {self}. """

	return Angle(self.length / 2.0)

    @staticmethod
    def rad(scalar_radians):
	""" Angle: Convert {scalar_radians} degrees into an {Angle} and
	    return it. """

	return Angle(scalar_radians)

    def radians(self):
	""" Angle: Convert {self} into radians and return it. """

	return self.radians

    def sine(self):
	""" Angle: Return the sine of {self}. """

	return math.sin(self.radians)

    def tangent(self):
	""" Angle: Return the tangent of {self}. """

	return math.tan(self.radians)

    def twice(self):
	""" Angle: Return twice of {self}. """

	return Angle(self.length * 2.0)

class EZCAD2:
    """ EZCAD is the top level engine that executes the design. """

    # Modes:
    DIMENSIONS = 1
    MANUFACTURE = 2

    def __init__(self, major, minor):
	""" {EZCAD}: Initialize the contents of {self} to contain
	    {major} and {minor} version numbers. """

	#print "EZCAD.__init__() called"

	# Check argument types:
	assert major == 1
	assert minor == 0

	# Load up {self}:
	self._major = major
	self._minor = minor
	self._parts_stack = []
	self._xml_indent = 0
	self._xml_stream = None

    def construct_mode(self):
	""" EZCAD: Return {True} if {self} is in construct mode. """

	return self.mode >= EZCAD2.CONSTRUCT_MODE


    def dimensions_changed(self, called_from):
	""" EZCAD: Mark that a dimension has changed somewhere in {self}. """

	#print "dimensions_changed.EZCAD(*, '%s')" % (called_from)
	self.changed_count = self.changed_count + 1

    def dimensions_mode(self):
	""" EZCAD: Return {True} if {self} is in dimensions mode. """

	return self.mode >= EZCAD.DIMENSIONS_DEFINE_MODE

    def dimensions_define_mode(self):
	""" EZCAD: Return {True} if {self} is in dimensions define mode. """

	return self.mode == EZCAD.DIMENSIONS_DEFINE_MODE

    def dimensions_refine_mode(self):
	""" EZCAD: Return {True} if {self} is in dimensions refine mode. """

	return self.mode == EZCAD.DIMENSIONS_REFINE_MODE

    def part_pop(self):
	""" EZCAD: Return top {Part} off the part stack of {self}. """

	parts_stack = self.parts_stack
	assert len(parts_stack) != 0, \
	  "Part stack is empty; probably missing call to done(). "
	
	return parts_stack.pop()

    def part_push(self, part):
	""" EZCAD: Push {part} onto the part stack of {self}. """

	self.parts_stack.append(part)

    def part_tree_mode(self):
	""" EZCAD: Return {True} if {self} is in tree mode. """

	return self.mode == EZCAD.PART_TREE_MODE

    def process(self, root_assembly_type):
	""" EZCAD: Perform the various phases of the CAD design using
	    {routine}. """
	
	# Phase 1: Define all of the {Part}'s:
	print "-------- Phase 1"
	self.mode = EZCAD2.PART_TREE_MODE
	routine(root)

	root.show("")

	# Phase 2a: Get point names defined:
	print "-------- Phase 2a"
	ezcad.mode = EZCAD2.DIMENSIONS_DEFINE_MODE
	routine(root)
	
	# Phase 2b: Get point values define
	ezcad.mode = EZCAD2.DIMENSIONS_REFINE_MODE
	ezcad.changed_count = 1
	while ezcad.changed_count != 0:
	    print "-------- Phase 2b"
	    ezcad.changed_count = 0
	    routine(root)

	# Phase 3: Iterate until all parts are constructed:
	print "-------- Phase 3"

	# Verify that we have exactly one root {Part}:
	root_part_names = root.parts.keys()
	assert len(root_part_names) == 1, \
	  "There must only be one root Part"

	# Open the XML output stream:
	root_part_name = root_part_names[0]
	xml_file_name = root_part_name + ".xml"
	xml_stream = open(xml_file_name, "w")
	assert xml_stream != None, \
	  "Unable to open XML output file '%s'" % (xml_file_name)
	ezcad.xml_stream = xml_stream
	ezcad._xml_indent = ""

	# Write the top level <EZCAD ...> line:
	version = 4
	xml_stream.write('<EZCAD Major="{0}" Minor="{1}" Version="{2}">\n'. \
	  format(ezcad.major, ezcad.minor, version))
	ezcad.xml_indent_push()

	# Now visit all of the part routins in construct mode:
	ezcad.mode = EZCAD2.CONSTRUCT_MODE
	routine(root)

	# Phase 4: Do anything that remains:

	# Close the XML Stream.
	ezcad.xml_indent_pop()
	assert ezcad._xml_indent == 0, \
	  "XML indentaion bracketing failure"

	xml_stream.write("</EZCAD>\n")
	xml_stream.close()
	ezcad.xml_stream = None

	# Now feed {xml_file_name} into EZCAD_XML:
	ezcad_xml = os.popen("EZCAD_XML {0}".format(xml_file_name), 'r')
	ezcad_xml.read()
	assert ezcad_xml.close() == None, \
	  "Error running 'EZCAD_XML {0}'".format(xml_file_name)

    def xml_indent_pop(self):
	""" {EZCAD}: Decrease the XML indentation and return it."""

	xml_indent = self._xml_indent
	assert xml_indent > 0, "Indentation error"
	self._xml_indent = xml_indent - 1


    def xml_indent_push(self):
	""" {EZCAD}: Increase the XML indentation and return the new
	    inendation level.  """

	self._xml_indent += 1

class Length:
    """ A {Length} represents a length. """

    # Currently {Length} is represented in inches:

    def __init__(self, value):
	""" Length: Create {Length} with a value of {value}. """

	self.value = float(value)


    def __add__(self, length):
	""" Length: Add {Length} to {self}. """

	return Length(self.value + length.value)

    def __div__(self, scalar):
	""" Length: Divide {self} by {scalar}. """

	return Length(self.value / scalar)

    def __eq__(self, length):
	""" Length: Return {True} if {self} is equal to {length}. """

	return self.value == length.value

    def __ge__(self, length):
	""" Length: Return {True} if {self} is greater than or equal
	    to {length}. """

	return self.value >= length.value

    def __lt__(self, length):
	""" Length: Return {True} if {self} is greater than {length}. """

	return self.value > length.value

    def __le__(self, length):
	""" Length: Return {True} if {self} is less than or equal
	    to {length}. """

	return self.value <= length.value

    def __lt__(self, length):
	""" Length: Return {True} if {self} is less than {length}. """

	return self.value < length.value

    def __format__(self, fmt):
	""" Length: Format {self} into a string an return it. """

	return "%f" % (self.value)

    def __mul__(self, scalar):
	""" Length: Multiply {self} by {scalar}. """

	return Length(self.value * scalar)

    def __rmul__(self, scalar):
	""" Length: Multiply {self} by {scalar}. """

	return Length(self.value * scalar)

    def __ne__(self, length):
	""" Length: Return {True} if {self} is not equal to {length}. """

	return self.value != length.value

    def __neg__(self):
	""" Length: Return the negative of {self}. """

	return Length(-self.value)

    def __str__(self):
	""" Length: Return {self} as a formated string. """

	return str(self.value)

    def __sub__(self, length):
	""" Length: Subtract {length} from {self}. """

	return Length(self.value - length.value)

    def abs(self):
	""" Length: Return absolue value of {self}. """

	return Length(abs(self.value))

    def arc_tangent2(self, dx):
	""" Length: Return the arctangent of {self} over {dx} being careful
	    that the returned angle is in the correct quadrant. """

	return Angle.rad(math.atan2(self.value, dx.value))

    def centimeters(self):
	""" Length: Return {self} as a scalar measured in centimeters. """

	return self.value * 2.54

    @staticmethod
    def cm(centimeters):
	""" Length: Return a {Length} of {centimeters}. """

	return Length(centimeters / 2.54)

    def cosine(self, angle):
	""" Length: Return {self} * cos(angle). """

	return Length(angle.cosine() * self.value)

    @staticmethod
    def distance2(dx, dy):
	""" Length: Return the length of the edge from the origin to
	    ({dx}, {dy}). """

	sdx = dx.value
	sdy = dy.value
	result = Length(math.sqrt(sdx * sdx + sdy * sdy))
	return result

    @staticmethod
    def distance3(dx, dy, dz):
	""" Length: Return the length of the edge from the origin to
	    ({dx}, {dy}, {dz}). """

	sdx = dx.value
	sdy = dy.value
	sdz = dz.value
	result = Length(math.sqrt(sdx * sdx + sdy * sdy + sdz * sdz))
	return result

    def half(self):
	""" Length: Return half of {self}. """

	return Length(self.value / 2.0)

    @staticmethod
    def inch(inches):
	""" Length: Return a {Length} of {inches}. """
	if type(inches) == type(""):
	    # We have a string, parse it:
            whole_fraction = inches.split("-")
	    if len(whole_fraction) == 2:
		whole = float(whole_fraction[0])
		faction = whole_fraction[1]
            elif len(whole_fraction) == 1:
		whole = 0.0
		fraction = inches
	    else:
		assert False, "Poorly formed inches string '{0}'".format(inches)
	    numerator_denominator = fraction.split("/")
	    assert len(numerator_denominator) == 2, \
	      "Bad fraction '{0}'".format(fraction)
	    numerator = float(numerator_denominator[0])
	    denominator = float(numerator_denominator[1])
	    inches = whole + numerator / denominator
		
	return Length(inches)

    def inches(self):
	""" Length: Return {self} as a scalar in units of inches. """

	return self.value

    @staticmethod
    def m(meters):
	""" Length: Return a {Length} of {meters} meters. """

	return Length(meters / 0.0254)

    def maximum(self, length):
	""" Length: Return the maximum of {self} and {length}. """

	result = self
	if length > result:
	    result = length
	return result

    def minimum(self, length):
	""" Length: Return the minimum of {self} and {length}. """

	result = self
	if length < result:
	    result = length
	return result

    def meters(self):
	""" Length: Return {self} as a scalar in units of meters. """

	return self.value * 0.0254

    def millimeters(self):
	""" Length: Return a {self} as a scalar in units of millimeters. """

	return self.value * 25.4

    @staticmethod
    def mm(millimeters):
	""" Length: Return a {Length} of {millimeters}. """

	return Length(millimeters / 25.4)

    def sine(self, angle):
	""" Length: Return {self} * sin(angle). """

	return Length(angle.sine() * self.value)

    def twice(self):
	""" Length: Return twice of {self}. """

	return Length(self.value * 2.0)

class Part:
    """ A {Part} specifies either an assembly of parts or a single
	physical part. """

    EZCAD = EZCAD2(1, 0)

    # Flavors of values that can be stored in a {Part}:
    def __init__(self, name, parent):

        # Check argument types:
	assert isinstance(name, str)
	assert parent == None or isinstance(parent, Part)

	# Some useful abbreviations:
	inch = Length.inch
	zero = inch(0)

	# Load up {points}:
	points = {}
	points["$O"] = Point(self, zero, zero, zero)
	
	# Find all the child *Part*'s:
	children = []
	for attribute_name in dir(self):
	    attribute = getattr(self, attribute_name)
            if isinstance(attribute, Part):
		children.append(attribute)
		#print("{0}['{1}'] = {2}". \
		#  format(name, attribute_name, attribute._name))

	# Load up {screw_levels}:
	screw_levels = {}
	screw_levels["B"] = {}
	screw_levels["E"] = {}
	screw_levels["N"] = {}
	screw_levels["S"] = {}
	screw_levels["T"] = {}
	screw_levels["W"] = {}

	# Load up *self*:
	self._angles = {}
	self._children = children
	self._corners = []
	self._ezcad = Part.EZCAD
	self._name = name
	self._origin = None
	self._material = "None"
	self._transparency = 1.0
	self._parent = parent
	self._parts = {}
	self._points = points
	self._places = {}
	self._lengths = {}
	self._scalars = {}
	self._strings = {}
	self._screws = {}
	self._screw_levels = screw_levels	
	self._transparency = 0.0
	self._top_surface = None
	self._top_surface_set = False
	self._xml_lines = []

	# Load up the bounding box:
	origin = self.point(zero, zero, zero)
	self.o = origin

	# Faces:
	self.b = origin
	self.e = origin
	self.n = origin
	self.s = origin
	self.t = origin
	self.w = origin

	# Edges:
	self.be = origin
	self.bw = origin
	self.bn = origin
	self.bs = origin
	self.ne = origin
	self.nw = origin
	self.se = origin
	self.sw = origin
	self.te = origin
	self.tw = origin
	self.tn = origin
	self.ts = origin

	# Corners:
	self.tne = origin
	self.tnw = origin
	self.tse = origin
	self.tsw = origin
	self.bne = origin
	self.bnw = origin
	self.bse = origin
	self.bsw = origin

	if parent == None:
	    zero = Length.inch(0.0)
	    self._origin_set(Point(self, zero, zero, zero))

    def _bounding_box_update(self, w, s, b, e, n, t):
	""" {Part} internal: Update the bounding box for {self} to have
	    corners of ({w}, {s}, {b}) and ({e}, {n}, {t}). """

	# Check argument types:
	assert isinstance(w, Length)
	assert isinstance(s, Length)
	assert isinstance(b, Length)
	assert isinstance(e, Length)
	assert isinstance(n, Length)
	assert isinstance(t, Length)
	assert w <= e, "w={0} should be less than e={1}".format(w, e)
	assert s <= n, "s={0} should be less than n={1}".format(s, n)
	assert b <= t, "b={0} should be less than t={1}".format(b, t)

	# Compute the mid-point values for east-west, north-south and
	# top-bottom:
	ew2 = (e + w).half()
	ns2 = (n + s).half()
	tb2 = (t + b).half()

	# Install 6 bounding box surface {Point}'s:
	self.b = self.point_new(ew2, ns2,   b)
	self.e = self.point_new(  e, ns2, tb2)
	self.n = self.point_new(ew2,   n, tb2)
	self.s = self.point_new(ew2,   s, tb2)
	self.t = self.point_new(ew2, ns2,   t)
	self.w = self.point_new(  w, ns2, tb2)

	# Install 12 bounding box edge {Point}'s into {points}:
	self.be = self.point_new(  e, ns2,   b)
	self.bn = self.point_new(ew2,   n,   b)
	self.bs = self.point_new(ew2,   s,   b)
	self.bw = self.point_new(  w, ns2,   b)
	self.ne = self.point_new(  e,   n, tb2)
	self.nw = self.point_new(  w,   n, tb2)
	self.se = self.point_new(  e,   s, tb2)
	self.sw = self.point_new(  w,   s, tb2)
	self.te = self.point_new(  e, ns2,   t)
	self.tn = self.point_new(ew2,   n,   t)
	self.ts = self.point_new(ew2,   s,   t)
	self.tw = self.point_new(  w, ns2,   t)

	# Install 8 bounding box corner {Point}'s into {points}:
	self.bne = self.point_new(e, n, b)
	self.bnw = self.point_new(w, n, b)
	self.bse = self.point_new(e, s, b)
	self.bsw = self.point_new(w, s, b)
	self.tne = self.point_new(e, n, t)
	self.tnw = self.point_new(w, n, t)
	self.tse = self.point_new(e, s, t)
	self.tsw = self.point_new(w, s, t)

	# Install the bounding box origin:
	self.o = self.point_new(ew2, ns2, tb2)

	#print "<=Part.bouinding_box_update('%s')" % (self.name)

    def origin_set(self, origin):
	""" Part: This method will recursively set the origin of *self*
	    and all of *self*'s children to *origin*. """

	self._origin_set(origin)

    def _origin_set(self, origin):
	""" Part (internal): This method will recursively set the origin
	    of *self* and all of *self*'s children to *origin*. """

	self._origin = origin
	for child in self._children:
	    child._origin_set(origin)

    def __getitem__(self, path):

	# Check argument types:
	assert isinstance(path, str)

	assert False

	children = self._children
	part = self
	path_parts = path.split("/")
	for index in range(len(path_parts)):
	    path_part = path_parts[index]
	    if path_part == "..":
		assert self._parent != None, \
		  "'{0}'[{1}]='{2}' stepped past root". \
		  format(path, index, path_part)
		part = self._parent
            else:
		if path_part in children:
		    path = children[path_part]
		else:
		    assert False, \
		      "'{0}'[{1}]='{2}' is not sub-part of {3}". \
		      format(path, index, path_part, part)
	return part

    def dimensions(self):
	assert False, \
	  "No dimensions() method defined for part '{0}'".format(self._name)

    def construct(self):
	assert False, \
	  "No construct() method defined for part '{0}'".format(self._name)

    def process(self):
	""" {Part}: Generate the XML control file for *self*. """

	# Do the dimensions propogate phase:
	changed = 1
	while changed != 0:
	    changed = self._dimensions_update(-1000000)

	# Open the XML output stream:
	xml_file_name = self._name + ".xml"
	xml_stream = open(xml_file_name, "w")
	assert xml_stream != None, \
	  "Unable to open XML output file '%s'" % (xml_file_name)

	# Prepare the {ezcad} object for generating XML file:
	ezcad = self._ezcad
	ezcad._xml_stream = xml_stream

	# Write the top level <EZCAD ...> line:
	version = 4
	xml_stream.write('<EZCAD Major="{0}" Minor="{1}" Version="{2}">\n'. \
	  format(ezcad._major, ezcad._minor, version))
	ezcad.xml_indent_push()

	# Now visit *self* and all of its children:
	self._manufacture()

	# Close the XML Stream.
	ezcad.xml_indent_pop()
	assert ezcad._xml_indent == 0, \
	  "XML indentaion bracketing failure"
	xml_stream.write("</EZCAD>\n")
	xml_stream.close()
	ezcad.xml_stream = None

	# Now feed {xml_file_name} into EZCAD_XML:
	ezcad_xml = os.popen("EZCAD_XML {0}".format(xml_file_name), 'r')
	ezcad_xml.read()
	assert ezcad_xml.close() == None, \
	  "Error running 'EZCAD_XML {0}'".format(xml_file_name)

    def _dimensions_update(self, trace):

	if trace >= 0:
	    print("{0}=>Part.dimensions_update('{1}')". \
	      format(' ' * trace, self._name))

	# Do dimension updating for children of *self*:
	changed = 0
	for child in self._children:
	    changed += child._dimensions_update(trace + 1)
	
	# Clear out any previous {_xml_lines} and {_places}:
	del self._xml_lines[:]

	# Generate a list of the *before* values for *self*:
	attribute_names = dir(self)
	before_values = {}
	for attribute_name in attribute_names:
	    if attribute_name[0] != '_':
		before_values[attribute_name] = getattr(self, attribute_name)
	
	# Peform dimension updating for *self*:
	self.construct()

	# See if anything changed:
	for attribute_name in attribute_names:
	    if attribute_name[0] != '_':
		before_value = before_values[attribute_name]
		after_value = getattr(self, attribute_name)
		assert type(before_value) == type(after_value), \
		  "{0}.{1} before type ({2}) different from after type ({3})". \
		  format(self._name, attribute_name, type(before_value),
		  type(after_value))
		if before_value != after_value:
		    changed += 1

	if trace >= 0:
	    print("{0}<=Part.dimensions_update('{1}')=>{2}". \
	      format(' ' * trace, self._name, changed))

	return changed

    def __str__(self):
	""" Part: Return {self} as a formatted string. """

	return str(self._name)

    def angle(self, angle_path):
	""" Part dimensions: Return the {Angle} associated with {angle_path}
	    starting from {self}. """
	
	return self.value_lookup(angle_path, Part.ANGLES)

    def angle_set(self, angle_name, angle_value):
	""" Part dimensions: Store an {Angle} named {angle_name} into {self}
	    with a value of  {angle_value}.  In addtion, {angle_value} is
	    returned. """

	return self.value_set(angle_name, angle, Part.ANGLES)

    def boundary_trim(self, comment, corner_radius, flags):
	""" Part construction: Using the last selected top surface
	    from {vice_position}() trim the 4 corners with a radius of
	    {corner_radius}. """

	#print "=>Part.boundary_trim({0}, '{1}', {2}, '{3}')". \
	#  format(self._name, comment, corner_radius, flags)

	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    # Grab the 6 surfaces:
	    t = self.t
	    b = self.b
	    n = self.n
	    s = self.s
	    e = self.e
	    w = self.w

	    # Grab the 8 corners:
	    tne = self.tne
	    tnw = self.tnw
	    tse = self.tse
	    tsw = self.tsw
	    bne = self.bne
	    bnw = self.bnw
	    bse = self.bse
	    bsw = self.bsw

	    # Compute {x_extra}, {y_extra}, {z_extra}:
	    x_extra = (w.x - self.xw.x).maximum(self.xe.x - e.x)
	    y_extra = (s.y - self.xs.y).maximum(self.xn.y - n.y)
	    z_extra = (b.z - self.xb.z).maximum(self.xt.z - t.z)

	    assert self._top_surface_set, \
	      "Top surface for part '{0}' is not set".format(self._name)
	    top_surface = self._top_surface
	    if top_surface == t:
		# Top surface:
		self.corner(comment + ":TNW", tnw, corner_radius)
		self.corner(comment + ":TNE", tne, corner_radius)
		self.corner(comment + ":TSE", tse, corner_radius)
		self.corner(comment + ":TSW", tsw, corner_radius)
		extra = x_extra.maximum(y_extra)
		self.contour(comment, t, b, extra, flags)
	    elif top_surface == b:
		# Bottom surface:
		self.corner(comment + ":BNW", bnw, corner_radius)
		self.corner(comment + ":BSW", bsw, corner_radius)
		self.corner(comment + ":BSE", bse, corner_radius)
		self.corner(comment + ":BNE", bne, corner_radius)
		extra = x_extra.maximum(y_extra)
		self.contour(comment, b, t, extra, flags)
	    elif top_surface == e:
		# East surface:
		self.corner(comment + ":BNE", bne, corner_radius)
		self.corner(comment + ":BSE", bse, corner_radius)
		self.corner(comment + ":TSE", tse, corner_radius)
		self.corner(comment + ":TNE", tne, corner_radius)
		extra = y_extra.maximum(z_extra)
		self.contour(comment, e, w, extra, flags)
	    elif top_surface == w:
		# West surface:
		self.corner(comment + ":BNW", bnw, corner_radius)
		self.corner(comment + ":BSW", bsw, corner_radius)
		self.corner(comment + ":TSW", tsw, corner_radius)
		self.corner(comment + ":TNW", tnw, corner_radius)
		extra = y_extra.maximum(z_extra)
		self.contour(comment, w, e, extra, flags)
	    elif top_surface == n:
		# North surface:
		self.corner(comment + ":TNE", tne, corner_radius)
		self.corner(comment + ":TNW", tnw, corner_radius)
		self.corner(comment + ":BNW", bnw, corner_radius)
		self.corner(comment + ":BNE", bne, corner_radius)
		extra = x_extra.maximum(z_extra)
		self.contour(comment, n, s, extra, flags)
	    elif top_surface == s:
		# South surface:
		self.corner(comment + ":TSE", tse, corner_radius)
		self.corner(comment + ":TSW", tsw, corner_radius)
		self.corner(comment + ":BSW", bsw, corner_radius)
		self.corner(comment + ":BSE", bse, corner_radius)
		extra = x_extra.maximum(z_extra)
		self.contour(comment, s, n, extra, flags)
	    else:
		assert False, \
		  "Top surface for {0} is {1} which is not $N/$S/$E/$W/$T/$B". \
		  format(self.name, top_surface)

    def block_corners(self, corner1, corner2, color, material):
	""" {Part} construct: Create a block with corners at {corner1} and
	    {corner2}.  The block is made of {material} and visualized as
	    {color}. """

	#print "block_corners('{0}', {1}, {2}, '{3}', '{4}')".format( \
	#  self.name, corner1, corner2, color, material)

	# Check argument types:
	assert isinstance(corner1, Point)
	assert isinstance(corner2, Point)
	assert isinstance(color, str)
	assert isinstance(material, str)

	# Make sure that the corners are diagonal from bottom south west
	# to top north east:
	x1 = min(corner1.x, corner2.x)
	x2 = max(corner1.x, corner2.x)
	y1 = min(corner1.y, corner2.y)
	y2 = max(corner1.y, corner2.y)
	z1 = min(corner1.z, corner2.z)
	z2 = max(corner1.z, corner2.z)

	#assert x1 < x2, "x1={0} should be less than x2={1}".format(x1, x2)
	#assert y1 < y2, "y1={0} should be less than y2={1}".format(y1, y2)
	#assert z1 < z2, "xz={0} should be less than z2={1}".format(z1, z2)

	#print "c1=({0},{1},{2}) c2=({3},{4},{5})".format( \
	#  x1, y1, z1, x2, y2, z2)

	self._bounding_box_update(x1, y1, z1, x2, y2, z2)

	# Record the material:
	self._material = material
	self._color = color
	self._xml_lines.append( ('<Block C1X="{0}" ' + \
	  'C1Y="{1}" C1Z="{2}" C2X="{3}" C2Y="{4}" C2Z="{5}"' + \
	  ' Color="{6}" Transparency="{7}" Material="{8}" Comment="{9}"/>'). \
	  format(x1, y1, z1, x2, y2, z2,
	  color, self._transparency, material, self._name))
	#print "Part.block_corners:_xml_lines={0}".format(self._xml_lines)

    def block_diagonal(self, diagonal, color, material):
	""" Part construct: Turn {self} into a block centered on the origin
	    with {diagonal} stretching equally across to the two opposite
	    corners.  The block is made of {material} and visualized
	    as {color}. """

	corner2 = diagonal.half()
	corner1 = -corner2
	self.block_corners(corner1, corner2, color, material)

    def chamfers(self, upper_chamfer, lower_chamfer):
	""" {Part} construct: Set the chamfers for contours and simple
	    pockets.  {upper_chamfer} specifies the chamfer of the
	    upper edge and the {lower_chamfer} specifies the chamer
	    of the lower edge.  Zero disables the chamfer for the
	    specified edge. """

	# Check argument types:
	assert isinstance(upper_chamfer, Length)
	assert isinstance(lower_chamfer, Length)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	# Output <Chamfers Upper= Lower= />:
	xml_stream.write('{0}<Chamfers Upper="{1}" Lower="{2}"/>\n'. \
	  format(xml_indent, upper_chamfer, lower_chamfer))

    def cnc_flush(self):
	""" Part constuct: """

	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    xml_stream.write('{0}<CNC_Flush />\n'. \
	      format(" " * ezcad._xml_indent))

    def construct_mode(self):
	""" Part dimensions: Return {True} if {self} should be constructed. """

	result = self.ezcad.construct_mode()
	return result

    def contour(self, comment, start_point, end_point, extra, flags):
	""" Part construct: Cause the current list of corners associated
	    with {self} to be removed starting at a depth of {start_point}
	    and ending at a depth of {end_point} using an exterior contour.
	    {extra} is the amount of extra material being removed. {flags}
	    can contain the letter 'u' for an upper chamfer, 'l' for a lower
	    chamfer, and 't' for a contour that cuts entirely through {self}.
	    {comment} is used in error messages and any generated G-code. """

	# Verify that each flag in {flags} is OK:
	for flag in flags:
	    assert flag == 'u' or flag == 'l' or flag == 't', \
	      'Part.Contour: Bad flag "{0}" in flags "{1}" for part {2}'. \
	      format(flag, flags, self.name)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	# Make sure we are in construct mode:
	#assert self.ezcad.construct_mode(), \
	#  "Part.Contour: Called when Part {0} is not in consturct mode". \
	#  format(self.name)

	if xml_stream != None:
	    # Make sure we have some {corners} for the contour:
	    corners = self._corners
	    corners_size = len(corners)
	    assert corners_size >= 3, \
	      "Part '{0}' only has {1} corners which is insufficient". \
	      format(self._name, corners_size)

	    # Now figure out the desired order for {corners}.  Depending upon
	    # what {top_surface} is being used, we reverse the contour
	    # direction:
	    top_surface = self._top_surface
	    reverse = None
	    if top_surface == self.e:
		reverse = False
	    elif top_surface == self.w:
		reverse = True
	    elif top_surface == self.n:
		reverse = False
	    elif top_surface == self.s:
		reverse = True
	    elif top_surface == self.t:
		reverse = False
	    elif top_surface == self.b:
		reverse = False
	    assert reverse != None, \
	      "Part {0} top surface must be one of T, B, N, S, E, or W". \
	      format(self.name)
	    if reverse:
		corners.reverse()

	    # Now output {corners} and clear it for the next contour:
	    for corner in self._corners:
		xml_stream.write(corner)
	    self._corners = []

	    # <Contour SX= SY= SZ= EX= EY= EZ= Extra= Flags= Comment= />:
	    xml_stream.write('{0}<Contour SX="{1}" SY="{2}" SZ="{3}"'. \
	      format(" " * xml_indent,
	      start_point.x, start_point.y, start_point.z))
	    xml_stream.write(' EX="{0}" EY="{1}" EZ="{2}"'. \
	      format(end_point.x, end_point.y, end_point.z))
	    xml_stream.write(' Extra="{0}" Flags="{1}" Comment="{2}"/>\n'. \
	      format(extra, flags, comment))

    def contour_reverse(self):
	""" """

	self._corners.reverse()

    def corner(self, comment, corner_point, radius):
	""" Part construct: Add a corner with a radius of {radius} to
	    {self} using {corner_point} to specify the corner location.
	    {comment} will show up any error messages or generated G-code. """

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    corner_xml = \
	      ('{0}<Corner Radius="{1}" CX="{2}" CY="{3}" CZ="{4}"' + \
	      ' Comment="{5}"/>\n').format(" " * ezcad._xml_indent,
	      radius, corner_point.x, corner_point.y, corner_point.z, comment)
	    self._corners.append(corner_xml)

    def done(self):
	""" Part (tree_mode): Mark {self} as done.  {self} is
	    always returned. """

	#print "=>Part.done('%s')" % (self.name)

	# Verify that parts stack is properly synchronized:
	if self.ezcad.part_tree_mode():
	    # Verify that the top of the parts stack matches {self}:
	    popped_part = self.ezcad.part_pop()
	    assert popped_part == self, \
	      "Part '%s' does not match popped part '%s'; mismathed done()?" % \
	      (self.name, popped_part.name)

	if self.construct_mode():
	    # Flush any remaining screw holes for current surface:
	    if self.top_surface_set:
		self.screw_holes(True)

       	    # Look for any screws that have not been processed:
	    screw_levels = self._screw_levels
            for screw_level_table in screw_levels.values():
		for screw_level in screw_level_table.values():
		    assert screw_level.done, \
		      "Screw {0} on {1} of part {2} has not been output". \
		      format(screw_level.screw.name, screw_level.surface, \
		      self.name)

	    # Close out this part in XML stream:
	    ezcad = self.ezcad
	    xml_stream = ezcad.xml_stream
	    ezcad.xml_indent_pop()
	    xml_stream.write("{0}</Part>\n".format(ezcad._xml_indent))

	#print "<=Part.done('%s')" % (self.name)
	return self

    def dimensions_changed(self, called_from):
	""" Part internal: Mark that a {Point} value associated with {self}
	    has changed. """

	self.ezcad.dimensions_changed(called_from)

    def dimensions_mode(self):
	""" Part internal: Return whether {True} if we in dimension mode
	    for {self}. """

	return self.ezcad.dimensions_mode()

    def dimensions_define_mode(self):
	""" Part internal: Return whether {True} if we in dimension define mode
	    for {self}. """

	return self.ezcad.dimensions_define_mode()

    def dimensions_refine_mode(self):
	""" Part internal: Return whether {True} if we in dimension refine mode
	    for {self}. """

	return self.ezcad.dimensions_refine_mode()

    def dxf_place(self, dxf_name, x_offset, y_offset):
	""" Part dimensions: Place {self} into the DXF file named {dxf_name}
	    with an offset of {x_offset} and {y_offset}. """

	if self.construct_mode():
	    ezcad = self.ezcad
	    xml_stream = ezcad.xml_stream
	    xml_stream.write(
	      '{0}<DXF_Place DX="{1}" DY="{2}" DXF_Name="{3}"/>\n'. \
	      format(ezcad._xml_indent, x_offset, y_offset, dxf_name))

    def extra_ewnstb(self, east, west, north, south, top, bottom):
	""" {Part} manufacture: Update the extra bounding box for {self}
	    to be extended by {east} and {west} in the X axis, {north} and
	    {south} in the Y axis, and {top} and {bottom} in the Z axis. """

	#print "extra_ewnstb: e={0} w={1} n={2} s={3} t={4} b={5}". \
	#  format(east, west, north, south, top, bottom)

	# Arugment type checking:
	assert isinstance(east, Length)
	assert isinstance(west, Length)
	assert isinstance(north, Length)
	assert isinstance(south, Length)
	assert isinstance(top, Length)
	assert isinstance(bottom, Length)

	# Look up {bsw} and {tne}, the bounding box corner {Point}'s:
	bsw = self.bsw
	tne = self.tne

	# Compute the dimensions of extra bounding box:
	b = bsw.z - bottom
	s = bsw.y - south
	w = bsw.x - west
	t = tne.z + top
	n = tne.y + north
	e = tne.x + east

	# Compute the mid-point values for east-west, north-south and
	# top-bottom:
	ew2 = (e + w).half()
	ns2 = (n + s).half()
	tb2 = (t + b).half()

	# Install 6 bounding box surface {Point}'s into {points}:
	self.xb = self.point_new(ew2, ns2,   b)
	self.xe = self.point_new(  e, ns2, tb2)
	self.xn = self.point_new(ew2,   n, tb2)
	self.xs = self.point_new(ew2,   s, tb2)
	self.xt = self.point_new(ew2, ns2,   t)
	self.xw = self.point_new(  w, ns2, tb2)

	# Install 12 bounding box edge {Point}'s into {points}:
	self.xbe = self.point_new(  e, ns2,   b)
	self.xbn = self.point_new(ew2,   n,   b)
	self.xbs = self.point_new(ew2,   s,   b)
	self.xbw = self.point_new(  w, ns2,   b)
	self.xne = self.point_new(  e,   n, tb2)
	self.xnw = self.point_new(  w,   n, tb2)
	self.xse = self.point_new(  e,   s, tb2)
	self.xsw = self.point_new(  w,   s, tb2)
	self.xte = self.point_new(  e, ns2,   t)
	self.xtn = self.point_new(ew2,   n,   t)
	self.xts = self.point_new(ew2,   s,   t)
	self.xtw = self.point_new(  w, ns2,   t)

	# Install 8 bounding box corner {Point}'s into {points}:
	self.xbne = self.point_new(e, n, b)
	self.xbnw = self.point_new(w, n, b)
	self.xbse = self.point_new(e, s, b)
	self.xbsw = self.point_new(w, s, b)
	self.xtne = self.point_new(e, n, t)
	self.xtnw = self.point_new(w, n, t)
	self.xtse = self.point_new(e, s, t)
	self.xtsw = self.point_new(w, s, t)

	xbsw = self.xbsw
	xtne = self.xtne
	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    xml_stream.write( ('{0}<Extra C1X="{1}" C1Y="{2}" C1Z="{3}"' + \
	      ' C2X="{4}" C2Y="{5}" C2Z="{6}"/>\n'). \
	      format(" " * ezcad._xml_indent,
	      xbsw.x, xbsw.y, xbsw.z, xtne.x, xtne.y, xtne.z))

    def extra_xyz(self, dx, dy, dz):
	""" {Part}: Add some extra material the block of {self} by {dx},
	    {dy}, and {dz} in the X, Y, and Z dimensions. """

	# Argument type checking:
	assert isinstance(dx, Length)
	assert isinstance(dy, Length)
	assert isinstance(dz, Length)

	# Pass everything on to {extra_ewnstb}:
	half_dx = dx.half()
	half_dy = dy.half()
	half_dz = dz.half()
	self.extra_ewnstb(half_dx, half_dx, half_dy, half_dy, half_dz, half_dz)

    def extrusion(self, color, material, kind, start_point, end_point, \
      a_width, a_thickness, b_width, b_thickness, rotate):
	""" Part dimensions: Create a {kind} extrusion manufactured out of
	    {material} that goes from {start_point} to {end_point} rotated
	    by {rotate}.  {a_width}, {a_thickness}, {b_width} and
	    {b_thickness} specify the extra dimentions of the extrusion.
	    The returned part is visualized using {color}. The extrusion
	    must be aligned with one of the X, Y or Z axes. """

	# Check argument types:
	assert isinstance(color, str)
	assert isinstance(material, str)
	assert isinstance(start_point, Point)
	assert isinstance(end_point, Point)
	assert isinstance(a_width, Length)
	assert isinstance(a_thickness, Length)
	assert isinstance(b_width, Length)
	assert isinstance(b_thickness, Length)
	assert isinstance(rotate, Angle)

	# Define soem useful abreviations:
	cosine = Angle.cosine
	inch = Length.inch
	sine = Angle.sine
	zero = inch(0)

	# Make sure we are in the right mode:
	assert not self.part_tree_mode(), \
	  "Part.extrusion: Part '{0}' is in part tree mode".format(self.name)

	# Compute {extrusion_axis}, the axis along with the tube is aligned:
	extrusion_axis = end_point - start_point
	extrusion_axis_x = extrusion_axis.x
	extrusion_axis_y = extrusion_axis.y
	extrusion_axis_z = extrusion_axis.z
	#print "start={0} end={1} extrusion_axis={2}". \
	#  format(start_point, end_point, extrusion_axis)

	# Extract coordinates from {start_point} and {end_point}:
	x1 = start_point.x
	y1 = start_point.y
	z1 = start_point.z
	x2 = end_point.x
	y2 = end_point.y
	z2 = end_point.z

	if kind == 'L':
	    # angLe extrusion:
	    # We have angle material:
	    #
	    #    |    |<----- a_width ------>|
	    #    v                             
	    # ------- +----------------------O -----
	    #         |                      |   ^
	    # ------- +-------------------+  |   |
	    #    ^                        |  |   |
	    #    |                        |  |   |
	    # b_thickness                 |  |   |
	    #                             |  | b_width
	    #                             |  |   |
	    #                             |  |   |
	    #                             |  |   |
	    #                             |  |   v
	    #                             +--+ -----
	    #
	    #             a_thickness --->|  |<---
	    #
	    # O = origin
	    # A goes negative from origin
	    # B goes negative from origin
	    a1 = -a_width
	    a2 = zero
	    b1 = zero
	    b2 = -b_width
	elif kind == 'C':
	    # We have channel material:

	    #       ->|  |<-- b_thickness
	    #
	    # ------- +--+                +--+ 
	    #    ^    |  |                |  | 
	    #    |    |  |                |  | 
	    #    |    |  |                |  | 
	    #    |    |  |                |  | 
	    #    |    |  |                |  | a_thickness
	    # b_width |  |                |  |   |
	    #    |    |  |                |  |   V
	    #    |    |  +----------------+  | -----
	    #    V    |                      |
	    # ------- O----------------------+ -----
	    #                                    ^
	    #         |<----- a_width ------>|   |
	    a1 = zero
	    a2 = a_width
	    b1 = zero
	    b2 = b_wdith
	elif kind == 'I':
	    assert False, "I beam not defined"
	elif kind == 'T':
	    assert False, "T beam not defined"
	elif kind == 'X':
	    assert False, "X beam not defined"
	elif kind == 'Z':
	    assert False, "Z beam not defined"
	else:
	    assert False, "Unrecognized extrusion '{0}'".format(kind)

	# Figure out what axis we are aligned on:
	if extrusion_axis_x != zero and \
	  extrusion_axis_y == zero and extrusion_axis_z == zero:
	    # Extrusion aligned on X:
	    # (a1, b1) (a1, b2) (a2, b1) (a2, b2)
	    a1_b1_distance = Length.distance2(a1, b1)
	    a1_b1_angle = a1.arc_tangent2(b1) + rotate
	    a1_b1_y = y1 + a1_b1_distance.cosine(a1_b1_angle)
	    a1_b1_z = z1 + a1_b1_distance.sine(a1_b1_angle)
	    #print("extrusion: a1b1d={0} a1b1a={1} a1b1x={2} a1b1y={3}". \
	    #  format(a1_b1_distance, a1_b1_angle, a1_b1_y, a1_b1_z))

	    a1_b2_distance = Length.distance2(a1, b2)
	    a1_b2_angle = a1.arc_tangent2(b2) + rotate
            a1_b2_y = y1 + a1_b2_distance.cosine(a1_b2_angle)
            a1_b2_z = z1 + a1_b2_distance.sine(a1_b2_angle)
	    #print("extrusion: a1b2d={0} a1b2a={1} a1b2x={2} a1b2y={3}". \
	    #  format(a1_b2_distance, a1_b2_angle, a1_b2_y, a1_b2_z))

	    a2_b1_distance = Length.distance2(a2, b1)
	    a2_b1_angle = a2.arc_tangent2(b1) + rotate
            a2_b1_y = y1 + a2_b1_distance.cosine(a2_b1_angle)
            a2_b1_z = z1 + a2_b1_distance.sine(a2_b1_angle)
	    #print("extrusion: a2b1d={0} a2b1a={1} a2b1x={2} a2b1y={3}". \
	    #  format(a2_b1_distance, a2_b1_angle, a2_b1_y, a2_b1_z))

	    a2_b2_distance = Length.distance2(a2, b2)
	    a2_b2_angle = a2.arc_tangent2(b2) + rotate
            a2_b2_y = y1 + a2_b2_distance.cosine(a2_b2_angle)
            a2_b2_z = z1 + a2_b2_distance.sine(a2_b2_angle)
	    #print("extrusion: a2b2d={0} a2b2a={1} a2b2x={2} a2b2y={3}". \
	    #  format(a2_b2_distance, a2_b2_angle, a2_b2_y, a2_b2_z))

	    e = max(x1, x2)
	    w = min(x1, x2)
	    n = max(max(a1_b1_y, a1_b2_y), max(a2_b1_y, a2_b2_y))
	    s = min(min(a1_b1_y, a1_b2_y), min(a2_b1_y, a2_b2_y))
	    t = max(max(a1_b1_z, a1_b2_z), max(a2_b1_z, a2_b2_z))
	    b = min(min(a1_b1_z, a1_b2_z), min(a2_b1_z, a2_b2_z))
	    #print("extrusion: e={0} w={1} n={2} s={3} t={4} b={5}". \
	    #  format(e, w, n, s, t, b))
	elif extrusion_axis_x == zero and \
	  extrusion_axis_y != zero and extrusion_axis_z == zero:
	    # Extrusion aligned on Y:
	    assert False, "Fix Y alignment"

	    e = max(xa1, xa2)
	    w = min(xa1, xa2)
	    n = max(y1, y2)
	    s = min(y1, y2)
            t = max(zb1, zb2)
            b = min(zb1, zb2)
	elif extrusion_axis_x == zero and \
	  extrusion_axis_y == zero and extrusion_axis_z != zero:
	    # Extrusion aligned on Z:
	    assert False, "Fix Z alignment"

	    e = max(xa1, xa2)
	    w = min(xa1, xa2)
	    n = max(yb1, yb2)
	    s = min(yb1, yb2)
            t = max(z1, z2)
            b = min(z1, z2)
	else:
	    assert not self.construct_mode(), \
 	      "Angle extrusion is not aligned with X, Y, or Z axis"
	    t = z2
            b = z1
	    n = y2
	    s = y1
	    w = x1
	    e = x2

	# Record the angle corners in {self}:
	self.point_xyz_set(kind + "_extrusion_corner_bsw", w, s, b)
	self.point_xyz_set(kind + "_extrusion_corner_tne", e, n, t)

	# Record the material in {self}:
	self._material = material

	if self.dimensions_mode():
            self.bounding_box_update(w, s, b, e, n, t)

	# In consturct mode, output the <Block ...> line:
	if self.construct_mode():
	    ezcad = self.ezcad
	    xml_stream = ezcad.xml_stream
	    xml_stream.write('{0}<Extrusion'.format(ezcad._xml_indent))
	    xml_stream.write(' Kind="{0}"'.format(kind))
	    xml_stream.write(' SX="{0}" SY="{1}" SZ="{2}"'.format(x1, y1, z1))
	    xml_stream.write(' EX="{0}" EY="{1}" EZ="{2}"'.format(x2, y2, z2))
	    xml_stream.write(' A_Width="{0}" A_Thickness="{1}"'. \
	      format(a_width, b_thickness))
	    xml_stream.write(' B_Width="{0}" B_Thickness="{1}"'. \
	      format(b_width, b_thickness))
	    xml_stream.write(' Rotate="{0}"'.format(rotate))
	    xml_stream.write(' Color="{0}" Transparency="{1}" Material="{2}"'. \
	      format(color, self.transparency, material))
	    xml_stream.write(' Comment="{0}"/>\n'.format(self.name))

    def hole(self, comment, diameter, start_point, end_point, flags, \
      countersink_diameter = Length.inch(0)):
	""" Part construct: Make a {diameter} hole in {part} with starting
	    at {start_point} and ending at {end_point}.  {comment} will
	    show in any error messages and any generated G-code.  The
	    allowed flag letters in {flags} are:

	      One of 't' (default), 'f', or 'p':
		't'	through hole (i.e. Through)
		'f'	flat hole (i.e. Flat)
		'p'	tip hole (drill tip stops at {end_point} (i.e. tiP)

	      Allowed additional flags:	  
		'u' upper hole edge should be chamfered (i.e. Upper)
		'l' lower hole edge should be chamfered (i.e. Lower)
		'm' hole is to be milled (i.e. Milled)
	"""


	# Define some useful abbreviations:
	inch = Length.inch
	zero = inch(0)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	if xml_stream != None:
	    # Output <Hole Diameter= Countersink_Diameter= ...
	    # ... SX= SY= SZ= EX= EY= EZ= Flags= Comment= />:
	    countersink_diameter = zero
	    xml_stream.write( \
	      '{0}<Hole Diameter="{1}" Countersink_Diameter="{2}"'. \
	      format(" " * xml_indent, diameter, countersink_diameter))
	    xml_stream.write(' SX="{0}" SY="{1}" SZ="{2}"'. \
	      format(start_point.x, start_point.y, start_point.z))
	    xml_stream.write(' EX="{0}" EY="{1}" EZ="{2}"'. \
	      format(end_point.x, end_point.y, end_point.z))
	    xml_stream.write(' Flags="{0}" Comment="{1}"/>\n'. \
	      format(flags, comment))
	
    def hole_through(self, comment, diameter, start_point, flags, \
      countersink_diameter = Length.inch(0)):
	""" Part construct: Make a {diameter} hole in {self} with starting
	    at {start_point} and going all the way through {self}.
	    {comment} will show in any error messages and any generated
	    G-code.  The allowed flag letters in {flags} are:

	      Zero, one or more of the following:
		't' through hole (i.e. Through)
		'u' upper hole edge should be chamfered (i.e. Upper)
		'l' lower hole edge should be chamfered (i.e. Lower)
	"""

	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream

	if xml_stream != None:

	    # Define some useful abbreviations:
	    inch = Length.inch
	    zero = inch(0)

	    # Extract some values from {ezcad}:
	    ezcad = self._ezcad
	    xml_indent = ezcad._xml_indent

	    # Write out <Hole_Through Diameter= SX= SY= SZ= Flags= Comment= />:
	    xml_stream.write('{0}<Hole_Through Diameter="{1}"'. \
	      format(" " * xml_indent, diameter))
	    xml_stream.write(' Countersink_Diameter="{0}"'. \
	      format(countersink_diameter))
	    xml_stream.write(' SX="{0}" SY="{1}" SZ="{2}"'. \
	      format(start_point.x, start_point.y, start_point.z))
	    xml_stream.write(' Flags="{0}" Comment="{1}"/>\n'. \
	      format(flags, comment))

    def length(self, length_path):
	""" Part dimensions: Return the {Angle} associated with {length_path}
	    starting from {self}. """
	
	return self.value_lookup(length_path, Part.LENGTHS)

    def length_set(self, length_name, length_value):
	""" Part dimensions: Store a {Length} named {length_name} into {self}
	    with a value of {length_value}.  In addtion, {length_value} is
	    returned. """

	return self.value_set(length_name, length_value, Part.LENGTHS)

    def part(self, part_path):
	""" Part dimensions: Return the {Part} associated with {part_pat}
	    starting from {self}. """

	path_parts = part_path.split('/')
	part = self
	for path_part in path_parts:
	    if path_part == "..":
		assert part.parent != None, \
		  "Path %s goes past root" % (part_path)
		part = part.parent
	    else:
		parts = part.parts
		assert path_part in parts, \
		  "No part named '{0}' in path '{1}' starting from part {2}". \
		  format(path_part, part_path, self.name)
		part = parts[path_part]
	return part

    def part_tree_mode(self):
	""" Part internal: Return {True} if {self} is in part tree mode. """

	return self.ezcad.part_tree_mode()

    def path_parts(self):
	""" Part internal: Return a list the contains the sequence of
	    {Part}'s from the root {Part} to {self}.  {self} is always the
	    last item on the returned list. """

	parts = []
	part = self
	while part.parent != None:
	    parts.append(part)
	    part = part.parent

	parts.reverse()
	#print "parts=", parts
	return parts

    def place(self, place_part, place_name, translate_point):
	""" Part dimensions: Place {place_part} at {translate_point} relative
	    to {self} with no rotation.  {place_name} is used for point
	    paths. """

	assert isinstance(place_part, Part)
	assert isinstance(place_name, str)
	assert isinstance(translate_point, Point)

	deg = Angle.deg
	inch = Length.inch
	zero = inch(0)

	center_point = self.point_new(zero, zero, zero)
	axis_point = self.point_new(inch(1), zero, zero)
	rotate_angle = deg(0)
	self.place_rotated(place_part, place_name, center_point,
	  axis_point, rotate_angle, translate_point)

    def place_rotated(self, place_part, place_name, center_point, \
      axis_point, rotate_angle, translate_point):
	""" Move {place_part} from {center_point} to the origin,
	    rotate by {rotate_angle} about the line from the origin
	    through {axis_point}, return the part back to
	    {center_point} and finaly translate to {translate_point}
	    {place_name} is used in place paths (described later)
	    to select amongst placement locations. """

	#print "Part.place_rotated({0}, {1}, {2}, {3}, {4}, {5}, {6})". \
	#  format(self.name, place_part.name, place_name, center_point, \
	#  axis_point, rotate_angle, translate_point)

	assert self != place_part, \
	  "Part.place('{0}'): Attempting a self-referential place"

	assert isinstance(place_part, Part)
	assert isinstance(place_name, str)
	assert isinstance(translate_point, Point)
	assert isinstance(axis_point, Point)
	assert isinstance(rotate_angle, Angle)
	assert isinstance(translate_point, Point)

	places = self._places

	cm = Length.cm
	deg = Angle.deg
	zero = cm(0)
	place = Place(place_name, self, place_part, \
	  center_point, axis_point, rotate_angle, translate_point)
	places[place_name] = place

	#if self.dimensions_define_mode():
	#    assert not (place_name in places), \
	#      "Placement '%s' in Part '%s' a duplicate" % \
	#      (place_name, self.name)
	#    places[place_name] = place
	#elif self.dimensions_refine_mode():
	#    assert place_name in places, \
	#      "Placement '%s' in Part '%s' is not defined" % \
	#      (place_name, self.name)
	#    previous_place = places[place_name]
	#
	#    if previous_place != place:
	#	places[place_name] = place
	#	self.dimensions_changed("Part.place(*, '%s', ...)" % \
	#	  (place_name))
	#else:
	#    assert False, "Performing a placement in part tree mode "


    def point(self, x, y, z):
	
	assert isinstance(x, Length)
	assert isinstance(y, Length)
	assert isinstance(z, Length)

	return Point(self, x, y, z)

    #def point(self, point_path):
    #	""" Part dimensions: Return the {Point} associated with {point_path}
    #	    starting from {self}. """
    #
    #	return self.value_lookup(point_path, Part.POINTS)

    def point_map(self, place_path):
	""" Part dimensions: Return the {Point} that corresponds to
	    the point specified by {place_path} in the {self} reference
	    frame. """

	assert not self.part_tree_mode(), \
	  "Part.point_subtract: Not allowed in part tree mode"

	# Wait until after all part names have been defined:
	if self.dimensions_define_mode():
	    zero = Length.inch(0)
	    result = Point(self, zero, zero, zero)
	else:
	    # Look up the {Part}/{Point}/{Matrix} triple for {place_path1}:
	    part_point_matrix = self.point_subtract_helper(place_path)
	    part = part_point_matrix[0]
	    point = part_point_matrix[1]
	    matrix = part_point_matrix[2]

	    # Perform the final subtraction and refernce to {part2}:
	    result = matrix.point_multiply(point, self)
	    #print "result={0}".format(result)

	return result

    def point_new(self, x, y, z):
	""" Part dimensions: Return a new point a ({x}, {y}, {z})
	    with  {self} as the reference frame.  """

	point = Point(self, x, y, z)
	return point

    def point_set(self, point_name, point_value):
	""" Part dimensions: Store a {Point} named {point_name} into {self}
	    with a value of {point_value}.  In addition, {point_value}
	    is returned. """

	return self.value_set(point_name, point_value, Part.POINTS)

    def point_subtract(self, place_path1, place_path2):
	""" Part dimensions: Return the {Point} that results from
	    subtracting {place_path2} from {place_path1}, where both
	    {place_path1} and {place_path2} start from a {self}.
	    The returned {Point} will use the {Part} associated
	    with {place_path2} as its reference frame. """

	assert not self.part_tree_mode(), \
	  "Part.point_subtract: Not allowed in part tree mode"

	# Wait until after all part names have been defined:
	if self.dimensions_define_mode():
	    zero = Length.inch(0)
	    result = Point(self, zero, zero, zero)
	else:
	    # Look up the {Part}/{Point}/{Matrix} triple for {place_path1}:
	    part_point_matrix1 = self.point_subtract_helper(place_path1)
	    part1 = part_point_matrix1[0]
	    point1 = part_point_matrix1[1]
	    matrix1 = part_point_matrix1[2]

	    # Look up the {Part}/{Point}/{Matrix} triple for {place_path2}:
	    part_point_matrix2 = self.point_subtract_helper(place_path2)
	    part2 = part_point_matrix2[0]
	    point2 = part_point_matrix2[1]
	    matrix2 = part_point_matrix2[2]

	    #print "matrix1=\n", matrix1
	    #print "matrix2=\n", matrix2
	    #print "matrix2.I=\n", matrix2.I
	    #print "point1_matrix=\n", point1_matrix
	    #print "matrix2.I * point1_matrix=\n", matrix2.I * point1_matrix

	    # Compute {mapping_matrix} which takes a point from {part2}
	    # referernce frame to {part1} reference frame:
	    mapping_matrix = matrix1 * matrix2.inverse()
	    #print "mapping_matrix=\n", mapping_matrix

	    # Now map {point1_matrix} into the same reference frame as {part2}:
	    point1_mapped = mapping_matrix.point_multiply(point1, part2)
	    #print "point1_mapped_matrix=", point1_mapped_matrix

	    # Perform the final subtraction and refernce to {part2}:
	    result = point1_mapped - point2
	return result

    def point_subtract_helper(self, place_path):
	""" Part internal: Return a 3 place tuple that contains the {Part},
	    {Point}, and {Matrix} associated with {place_path} starting
	    from {self}. """

	place_path_point_name = place_path.split('.')
	place_path_point_name_size = len(place_path_point_name)
	if place_path_point_name_size == 1 or place_path_point_name_size == 2:
	    if place_path_point_name_size == 1:
		# We only have a point name:
		point_name = place_path
		place_path = ""
	    else:
		# We have a place path and a point name:
		point_name = place_path_point_name[1]
		place_path = place_path_point_name[0]

	    # Start {forward_matrix} of with an identity matrix:
	    forward = Matrix.identity_create()

	    # Iterate across {place_path}:
	    part = self
	    place_names = place_path.split('/')
	    for place_name in place_names:
		places = part.places
		if not place_name in places:
		    message = "Invalid place name '{0}'" + \
		      " in place path '{1}' starting from part '{2}'"
		    assert False, \
		      message.format(place_name, place_path, self.name)

		# Move forward by {place}:
		place = places[place_name]
		forward = forward * place.forward_matrix
		part = place.placed_part

	    # Lookup {place_name}:
	    points = part.points
	    if not (point_name in points):
		message = "Point name '{0}' not found in part '{1}' using" + \
		  " place path '{2}' starting from part '{3}'"
		assert False, message. \
		  format(point_name, part.name, place_path, self.name)
	    point = points[point_name]
	else:
	    # Invalid place path:
	    assert False, \
	      "Invalid place path '{0}' starting from Part '{1}'". \
	      format(place_path, self.name)

	return (part, point, forward)

    def point_xyz_set(self, point_name, x, y, z):
	""" Part: Create a {Point} containing {x}, {y}, {z}, using {self}
	    for the reference frame, associate it with {point_name} in
	    {self}, and return the resulting {Point}. """

	return self.point_set(point_name, self.point_new(x, y, z))

    def relative_path(self, to_part):
	""" Part internal: Return the relative path from {self}
	    to {to_part}. """

	#print "Part.relative_path('{0}', '{1}')". \
	#  format(self.name, to_part.name)

	from_path_parts = self.path_parts()
	to_path_parts = to_part.path_parts()

	#print "from_path_parts=", from_path_parts
	#print "to_path_parts=", to_path_parts

	while len(from_path_parts) != 0 and len(to_path_parts) != 0 and \
	  from_path_parts[0] == to_path_parts[0]:
	    from_path_parts.pop(0)
	    to_path_parts.pop(0)
	
	separator = ''
	path = ""
	while len(from_path_parts) != 0:
	    from_path_parts.pop()
	    path = path + separator + ".."
	    separator = '/'

	while len(to_path_parts) != 0:
	    part = to_path_parts.pop()
	    path = path + separator + part.name
	    separator = '/'

	return path

    def rod(self, color, material, start_point, end_point, diameter, sides):
	""" Part dimensions: Create a rod for {self} out of {material} that
	    goes from {start_point} to {end_point} and is {diameter} round.
	    The rod is visualized with {color}.  {sides} specifies how many
	    sides to use for visualization; setting {sides} to zero gives a
	    reasonable visualization.  The rod must be aligned with
	    one of the X, Y or Z axes. """

	self.tube(color, material, start_point, end_point, diameter, \
	  diameter.half() - Length.inch(.0001), sides)

    def scalar(self, scalar_path):
	""" Part dimensions: Return the {Angle} associated with {scalar_path}
	    starting from {self}. """
	
	return self.value_lookup(scalar_path, Part.SCALARS)

    def scalar_set(self, scalar_name, scalar_value):
	""" Part dimensions: Store a scaler into {self} named {scalar_name}
	    with a value of {scalar_value}.  In addition, {scalar_value}
	    is returned. """

	return self.value_set(scalar_name, scalar_value, Part.SCALARS)

    def screw(self, screw_path):
	""" Part dimensions: Return the {Screw} associated with {screw_path}
	    starting from {self}. """
	
	screw = self.value_lookup(screw_path, Part.SCREWS)
	return screw

    def screw_anchor_set(self, screw_name, anchor_point):
	""" Part dimensions: Set the anchor for the {Screw} named {screw_name}
	    in {self} to {anchor_point}. """

	if self.dimensions_refine_mode():
	    screw = self.screw_find(screw_name)
	    screw.anchor_set(anchor_point)

    def screw_attach(self, screw_path, surface, flags):
	""" Part dimensions: Attach the {Part} specified by {screw_path}
	    to the last {Screw} created with {Part.screw_create}.
	    The screw is attached to {surface} with hole {flags}. """

	if self.dimensions_mode():
	    screw_last = self.screw_last
	    assert screw_last != None, \
	      "Part '{0}' does not have a previously created Screw". \
	      format(self.name)

	    screw_last.attach(screw_path, surface, flags)

    def screw_create(self, screw_name, thread, direction):
	""" Part dimensions: Store a new {Screw} named {screw_name} into
	    {self}.  The new {screw} will contain {thread} and {direction}.
	    In addtion, {screw_value} is returned. """

	assert not self.part_tree_mode(), \
	  "Can not create screw in part {0} before dimensions mode". \
	  format(self.name)

	# Stuff it into {self} in the screws table:
	if self.dimensions_define_mode():
	    screw = Screw(self, screw_name, thread, direction)
	    self.value_set(screw_name, screw, Part.SCREWS)
	else:
	    screw = self.value_lookup(screw_name, Part.SCREWS)
	self.screw_last = screw
	return screw

    def screw_depth_set(self, screw_name, depth):
	""" Part dimensions: Set screw depth of the {Screw} named {screw_depth}
	    to {depth} for {self}. """

	if self.dimensions_refine_mode():
	    screw_level = self.screw_level_find(screw_name)
	    screw_level.depth_set(depth)

    def screw_diameter(self, screw, flags):
	""" Part internal: Return the diamter associated with {screw}
	    using {flags} to select the style of hole. """

	# http://www.electroimpact.com/company/QMS-0003.pdf

	# Create letter and number drill table:
	drill = {}
	drill["80"] = 0.0135
	drill["79"] = 0.0145
	drill["78"] = 0.0160
	drill["77"] = 0.0180
	drill["76"] = 0.0200
	drill["75"] = 0.0210
	drill["74"] = 0.0225
	drill["73"] = 0.0240
	drill["72"] = 0.0250
	drill["71"] = 0.0260
	drill["70"] = 0.0280
	drill["69"] = 0.0292
	drill["68"] = 0.0310
	drill["67"] = 0.0320
	drill["66"] = 0.0330
	drill["65"] = 0.0350
	drill["64"] = 0.0360
	drill["63"] = 0.0370
	drill["62"] = 0.0380
	drill["61"] = 0.0390
	drill["60"] = 0.0400
	drill["59"] = 0.0410
	drill["58"] = 0.0420
	drill["57"] = 0.0430
	drill["56"] = 0.0465
	drill["55"] = 0.0520
	drill["54"] = 0.0550
	drill["53"] = 0.0595
	drill["52"] = 0.0635
	drill["51"] = 0.0670
	drill["50"] = 0.0700
	drill["49"] = 0.0730
	drill["48"] = 0.0760
	drill["47"] = 0.0785
	drill["46"] = 0.0810
	drill["45"] = 0.0820
	drill["44"] = 0.0860
	drill["43"] = 0.0890
	drill["42"] = 0.0935
	drill["41"] = 0.0960
	drill["40"] = 0.0980
	drill["39"] = 0.0995
	drill["38"] = 0.1015
	drill["37"] = 0.1040
	drill["36"] = 0.1065
	drill["35"] = 0.1100
	drill["34"] = 0.1110
	drill["33"] = 0.1130
	drill["32"] = 0.1160
	drill["31"] = 0.1200
	drill["30"] = 0.1285
	drill["29"] = 0.1360
	drill["28"] = 0.1405
	drill["27"] = 0.1440
	drill["26"] = 0.1470
	drill["25"] = 0.1495
	drill["24"] = 0.1520
	drill["23"] = 0.1540
	drill["22"] = 0.1570
	drill["21"] = 0.1590
	drill["20"] = 0.1610
	drill["19"] = 0.1660
	drill["18"] = 0.1695
	drill["17"] = 0.1730
	drill["16"] = 0.1770
	drill["15"] = 0.1800
	drill["14"] = 0.1820
	drill["13"] = 0.1850
	drill["12"] = 0.1890
	drill["11"] = 0.1910
	drill["10"] = 0.1935
	drill["9"] = 0.1960
	drill["8"] = 0.1990
	drill["7"] = 0.2010
	drill["6"] = 0.2040
	drill["5"] = 0.2055
	drill["4"] = 0.2090
	drill["3"] = 0.2130
	drill["2"] = 0.2210
	drill["1"] = 0.2280
	drill["A"] = 0.2340
	drill["B"] = 0.2380
	drill["C"] = 0.2420
	drill["D"] = 0.2460
	drill["E"] = 0.2500
	drill["F"] = 0.2570
	drill["G"] = 0.2610
	drill["H"] = 0.2660
	drill["I"] = 0.2720
	drill["J"] = 0.2770
	drill["K"] = 0.2810
	drill["L"] = 0.2900
	drill["M"] = 0.2950
	drill["N"] = 0.3020
	drill["O"] = 0.3160
	drill["P"] = 0.3230
	drill["Q"] = 0.3320
	drill["R"] = 0.3390
	drill["S"] = 0.3480
	drill["T"] = 0.3580
	drill["U"] = 0.3680
	drill["V"] = 0.3770
	drill["W"] = 0.3860
	drill["X"] = 0.3970
	drill["Y"] = 0.4040
	drill["Z"] = 0.4130

	# Create metric screw table {m}:
	# (75% M, 75% I, 50% M, 50% I, close M, close I, loose M, loose I)
	m = {}
	m["M1.5x0.35"] = (1.15, "56", 1.25, "55", 1.60, "1/16", 1.65, "52")
	m["M1.6x0.35"] = (1.25, "55", 1.35, "54", 1.70, "51", 1.75, "50")
	m["M1.8x0.35"] = (1.45," 53", 1.55, "1/16", 1.90, "49", 2.00, "5/64")
	m["M2x0.45"] = (1.55, "1/16", 1.70, "51", 2.10, "45", 2.20, "44")
	m["M2x0.40"] = (1.60, "52", 1.75, "50", 2.10, "45", 2.20, "44")
	m["M2.2x0.45"] = (1.75, "50", 1.90, "48", 2.30, "3/32", 2.40, "41")
	m["M2.5x0.45"] = (2.05, "46", 2.20, "44", 2.65, "37", 2.75, "7/64")
	m["M3x0.60"] = (2.40, "41", 2.60, "37", 3.15, "1/8", 3.30, "30")
	m["M3x0.50"] = (2.50, "39", 2.70, "36", 3.15, "1/8", 3.30, "30")
	m["M3.5x0.60"] = (2.90, "32", 3.10, "31", 3.70, "27", 3.85, "24")
	m["M4x0.75"] = (3.25, "30", 3.50, "28", 4.20, "19", 4.40, "17")
	m["M4x0.70"] = (3.30, "30", 3.50, "28", 4.20, "19", 4.40, "17")
	m["M4.5x0.75"] = (3.75, "25", 4.00, "22", 4.75, "13", 5.00, "9")
	m["M5x1.0"] = (4.00, "21", 4.40, "11/64", 5.25, "5", 5.50, "7/32")
	m["M5x0.90"] = (4.10, "20", 4.40, "17", 5.25, "5", 5.50, "7/32")
	m["M5x0.80"] = (4.20, "19", 4.50, "16", 5.25, "5", 5.50, "7/32")
	m["M5.5x0.90"] = (4.60, "14", 4.90, "10", 5.80, "1", 6.10, "B")
	m["M6x1.0"] = (5.00, "8", 5.40, "4", 6.30, "E", 6.60, "G")
	m["M6x0.75"] = (5.25, "4", 5.50, "7/32", 6.30, "E", 6.60, "G")
	m["M7x1.0"] = (6.00, "B", 6.40, "E", 7.40, "L", 7.70, "N")
	m["M7x0.75"] = (6.25, "D", 6.50, "F", 7.40, "L", 7.70, "N")
	m["M8x1.25"] = (6.80, "H", 7.20, "J", 8.40, "Q", 8.80, "S")
	m["M8x1.0"] = (7.00, "J", 7.40, "L", 8.40, "Q", 8.80, "S")
	m["M9x1.25"] = (7.80, "N", 8.20, "P", 9.50, "3/8", 9.90, "25/64")
	m["M9x1.0"] = (8.00, "O", 8.40, "21/64", 9.50, "3/8", 9.90, "25/64")
	m["M10x1.50"] = (8.50, "R", 9.00, "T", 10.50, "Z", 11.00, "7/16")
	m["M10x1.25"] = \
	    (8.80, "11/32", 9.20, "23/64", 10.50, "Z", 11.00, "7/16")
	m["M10x1.0"] = \
	    (9.00, "T", 9.40, "U", 10.50, "Z", 11.00, "7/16")
	m["M11x1.50"] = \
	    (9.50, "3/8", 10.00, "X", 11.60, "29/64", 12.10, "15/32")
	m["M12x1.75"] = \
	    (10.30, "13/32", 10.90, "27/64", 12.60, "1/2", 13.20, "33/64")
	m["M12x1.50"] = \
	    (10.50, "Z", 11.00, "7/16", 12.60, "1/2", 13.20, "33/64")
	m["M12x1.25"] = \
	    (10.80, "27/64", 11.20, "7/16", 12.60, "1/2", 13.20, "33/64")
	m["M14x2.0"] = \
	    (12.10, "15/32", 12.70, "1/2", 14.75, "37/64", 15.50, "39/64")
	m["M14x1.50"] = \
	    (12.50, "1/2", 13.00, "33/64", 14.75, "37/64", 15.50, "39/64")
	m["M14x1.25"] = \
	    (12.80, "1/2", 13.20, "33/64", 14.75, "37/64", 15.50, "39/64")
	m["M15x1.50"] = \
	    (13.50, "17/32", 14.00, "35/64", 15.75, "5/8", 16.50, "21/32")
	m["M16x2.0"] = \
	    (14.00, "35/64", 14.75, "37/64", 16.75, "21/32", 17.50, "11/16")
	m["M16x1.50"] = \
	    (14.50, "37/64", 15.00, "19/32", 16.75, "21/32", 17.50, "11/16")
	m["M17x1.50"] = \
	    (15.50, "39/64", 16.00, "5/8", 18.00, "45/64", 18.50, "47/64")
	m["M18x2.50"] = \
	    (15.50, "39/64", 16.50, "41/64", 19.00, "3/4", 20.00, "25/32")
	m["M18x2.0"] = \
	    (16.00, "5/8", 16.75, "21/32", 19.00, "3/4", 20.00, "25/32")
	m["M18x1.50"] = \
	    (16.50, "21/32", 17.00, "43/64", 19.00, "3/4", 20.00, "25/32")
	m["M19x2.50"] = \
	    (16.50, "21/32", 17.50, "11/16", 20.00, "25/32", 21.00, "53/64")
	m["M20x2.50"] = \
	    (17.50, "11/16", 18.50, "23/32", 21.00, "53/64", 22.00, "55/64")
	m["M20x2.0"] = \
	    (18.00, "45/64", 18.50, "47/64", 21.00, "53/64", 22.00, "55/64")
	m["M20x1.50"] = \
	    (18.50, "47/64", 19.00, "3/4", 21.00, "53/64", 22.00, "55/64")

	diameter = None
	if screw.find("M") == 0:
	    # We have metric:
	    #print "metric_screw"
	    if screw in m:
		# We have found the metric screw:
		values = m[screw]


		# Use {flags} to select {drill_name}:
		drill_name = None
		if flags.find("d") >= 0:
		    # threaDed:
		    if self._material.find("steel") == 0:
			# Hard material => 50% tap:
			drill_name = values[3]
		    else:
			# Soft material => 75% tap:
			drill_name = values[1]
		elif flags.find("p") >= 0:
		    # Loose fit:
		    drill_name = values[7]
		else:
		    # Close fit: 
		    drill_name = values[5]

		# Deal with fractional, number and letter drills:
		if drill_name.find('/') >= 0:
		    # We have a fractional drill:
		    numerator_denominator = drill_name.split('/')
		    diameter = float(numerator_denominator[0]) / \
		      float(numerator_denominator[1])
		else:
		    # We have a number or letter drill:
		    diameter = drill[drill_name]
	else:
	    # Try imperial:
            # (75%, 50%, close, loose, countersink)
	    values = None
	    if screw.find("0-") == 0:
		# Number 0 screw:
		if screw == "0-80":
		    values = (.0469, .0520, .0635, .0700, None)
	    elif screw.find("2-") == 0:
		# Number 2 screw:
		if screw == "2-56":
		    values = (.0700, .0730, .0890, .0960, 0.214)
	    elif screw.find("4-") == 0:
		# Number 4 screw:
	 	if screw == "4-40":
		    values = (.0890, .0960, .1160, .1285, 0.272)
	    elif screw.find("6-") == 0:
		# Number 6 screw:
		if screw == "6-32":
		    values = (.1065, .1160, .1440, .1495, 0.324)
	    elif screw.find("8-") == 0:
		# Number 8 screw:
		if screw == "8-32":
		    values = (.1260, .1440, .1695, .1770, 0.376)
	    elif screw.find("10-") == 0:
		# Number 10 screw:
		if screw == "10-32":
		    values = (.1517, .1590, .1960, .2010, 0.428)
		elif screw == "10-24":
		    values = (.1495, .1610, .1960, .2010, 0.428)
	    elif screw.find("12-") == 0:
		# Number 12 screw:
		if screw == "12-24":
		    values = (.1649, .1770, .2210, .2280, None)
	    assert values != None, "Screw '{0}' is not recognized".format(screw)

	    if flags.find("d") >= 0:
		# threaDed:
		if self._material.find("steel") == 0:
		    # Hard material => 50% tap:
		    diameter = values[1]
		else:
		    # Soft material => 75% tap:
		    diameter = values[0]
	    elif flags.find("s") >= 0:
		# Loose fit:
		diameter = values[3]
	    elif flags.find("!") >= 0:
		# Return counersink
		diameter = values[4]
		assert diameter != None, \
		  "Need to fill in table value for countersink diamete"
	    else:
		# Close fit: 
		diameter = values[2]

	#print "flags={0} values={1} diameter={2}". \
	#  format(flags, values, diameter)

	assert diameter != None, "Screw {0} not recognized".format(screw)
	return Length.inch(diameter)

    def screw_find(self, screw_name):
	""" Part dimensions: Return the {Screw} associated with {screw_name}
	    in {self}. """

	# Iterate across {screw_levels} in {self}:
	screw_level = self.screw_level_find(screw_name)
	return screw_level.screw

    def screw_hole(self, comment, screw, start_point, end_point, flags):
	""" Part construct: Make a hole for {screw} in {self} with starting
	    at {start_point} and ending at {end_point}.  {comment} will
	    show up in any error messages and any generated G-code.
	    The allowed flag letters in {flags} are:

	      One of 't' (default), 'f', or 'p':
		't' through hole (i.e. Through)
		'f' flat hole (i.e. Flat)
		'p' tip hole (drill tip stops at {end_point} (i.e. tiP)

	      One of 'd', 'c' (default), or 's':
		'd' hole is to be tapped (i.e. threaDed)
		'c' hole is a close fit (i.e. Close fit)
		's' hole is a loose fit (i.e. LooSe fit)

	      Allowed additional flags:	  
		'u' upper hole edge should be chamfered (i.e. Upper)
		'l' lower hole edge should be chamfered (i.e. Lower)
		'm' hole is to be milled (i.e. Milled)
		'i' imperial vs. metric swapping allowed (i.e. Interchangeable)
		'a' counterink hole for a flAthead screw
	"""

	# Check argument types:
	assert isinstance(comment, str)
	assert isinstance(screw, str)
	assert isinstance(start_point, Point)
	assert isinstance(end_point, Point)
	assert isinstance(flags, str)

	#print "Part.screw_hole: Part={0} screw={1} flags={2}". \
	#  format(self.name, screw, flags)

	screw_diameter = self.screw_diameter(screw, flags)
	countersink_diameter = Length.inch(0)
	if flags.find('a') != 0:
	    countersink_diameter = self.screw_diameter(screw, '!')

	self.hole(comment, screw_diameter, \
	  start_point, end_point, flags, countersink_diameter)
	
    def screw_holes(self, errors_suppress = False):
	""" Part construct: Perform all pending screws for the currently
	    mounted surface. """

	#print "=>Part.screw_holes({0})".format(self.name)

	# Some useful abbreviations:
	inch = Length.inch
	big = inch(123456789.0)
	
	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    # Grab the six surfaces from {self}:
	    b = self.b
	    e = self.e
	    n = self.n
	    s = self.s
	    t = self.t
	    w = self.w

	    # Extract the bounding box of {self}:
	    t_z = t.z
	    b_z = b.z
	    n_y = n.y
	    s_y = s.y
	    e_x = e.x
	    w_x = w.x

	    # Figure out {screw_levels_table} based on {top_surface}:
	    screw_levels = self._screw_levels
	    top_surface = self._top_surface
	    screw_levels_table = {}
	    if self._top_surface_set:
		if top_surface == t:
		    screw_levels_table = screw_levels["T"]
		    top_surface_name = "Top"
		    t_z = big
		    b_z = -big
		elif top_surface == b:
		    screw_levels_table = screw_levels["B"]
		    top_surface_name = "Bottom"
		    t_z = big
		    b_z = -big
		elif top_surface == n:
		    screw_levels_table = screw_levels["N"]
		    top_surface_name = "North"
		    n_y = big
		    s_y = -big
		elif top_surface == s:
		    screw_levels_table = screw_levels["S"]
		    top_surface_name = "South"
		    n_y = big
		    s_y = -big
		elif top_surface == e:
		    screw_levels_table = screw_levels["E"]
		    top_surface_name = "East"
		    e_x = big
		    w_x = -big
		elif top_surface == w:
		    screw_levels_table = screw_levels["W"]
		    top_surface_name = "West"
		    e_x = big
		    w_x = -big
		else:
		    assert False, \
		      "Unexpected top surface for part {0} is {1}". \
		      format(self.name, top_surface)

	    if len(screw_levels_table) == 0:
		assert errors_suppress, \
		  "Part '{0}' does not have any attached holes on {1} surface".\
		  format(self.name, top_surface_name)
	    else:
		for screw_level in screw_levels_table.values():
		    #print "screw_level=", screw_level
		    screw = screw_level.screw
		    #print "screw.name=", screw.name
		    trace = False
		    #trace = screw.name.find("skin_west_bottom") >= 0

		    # Grap {anchor_point_mapped} from {screw}:
		    anchor_point_mapped = screw.anchor_point_mapped
		    if trace:
			print "=>Part.screw_holes({0})".format(self.name)
			print "anchor_point_mapped={0}". \
			  format(anchor_point_mapped)

		    remap_matrix = screw_level.reverse_matrix
		    if trace:
			print "screw_level_forward_matrix=\n{0}". \
			  format(screw_level.forward_matrix.mat	)
			print "screw_level_reverse_matrix=\n{0}". \
			  format(screw_level.reverse_matrix.mat)
			#print "remap_matrix=\n{0}".format(remap_matrix.mat)
		    anchor_point_remapped = \
		      remap_matrix.point_multiply(anchor_point_mapped, self)
		    x = anchor_point_remapped.x
		    y = anchor_point_remapped.y
		    z = anchor_point_remapped.z
		    if trace:
			bse = self.point("$BSE")
			tnw = self.point("$TNW")
			print "bse={0}".format(bse)
			print "tnw={0}".format(tnw)
			print "anchor_point_remapped={0}". \
			  format(anchor_point_remapped)
			#print \
			#  "w_x={0} e_x={1} s_y={2} n_y={3} b_z={4} t_z={5}". \
			#  format(w_x, e_x, s_y, n_y, b_z, t_z)

		    # Make sure everything is in on the part:
		    assert w_x <= x and x <= e_x, \
		      ("X (={0}) for screw {1} not between {2}" + \
		      " and {3} (part={4})"). \
		      format(x, screw.name, w_x, e_x, self.name)
		    assert s_y <= y and y <= n_y, \
		      ("Y (={0}) for screw {1} not between {2}" + \
		      " and {3} (part={4})"). \
		      format(y, screw.name, s_y, n_y, self.name)
		    assert b_z <= z and z <= t_z, \
		      ("Z (={0}) for screw {1} not between {2}" + \
		      " and {3} (part={4})"). \
		      format(z, screw.name, b_z, t_z, self.name)

		    # Compute {start_point} and {end_point} based on
		    # {top_surface} and {depth}:
		    depth = screw_level.depth
		    if top_surface == t:
			start_point = self.point_new(x, y, t.z)
			end_point = start_point.z_adjust(-depth)
		    elif top_surface == b:
			start_point = self.point_new(x, y, b.z)
			end_point = start_point.z_adjust(depth)
		    elif top_surface == n:
			start_point = self.point_new(x, n.y, z)
			end_point = start_point.y_adjust(-depth)
		    elif top_surface == s:
			start_point = self.point_new(x, s.y, z)
			end_point = start_point.y_adjust(depth)
		    elif top_surface == e:
			start_point = self.point_new(e.x, y, z)
			end_point = start_point.x_adjust(-depth)
		    elif top_surface == w:
			start_point = self.point_new(w.x, y, z)
			end_point = start_point.x_adjust(depth)
		    else:
			assert False

		    # No do either a through hole or a hole to {depth}:
		    if not screw_level.done:
			thread = screw.thread
			flags = screw_level.flags
			#print "Part.screw_holes: part={0} screw={1}" + \
			#  " thread={2} flags={3}". \
			#  format(self.name, screw_level.screw.name, \
			#  thread, flags)
			if depth <= Length.inch(0):
			    # Drill all the way through:
			    self.screw_through(screw.name,thread, \
			      start_point, flags)
			else:
			    # Drill to the specified {end_point}:
			    self.screw_hole(screw.name, \
			      thread, start_point, end_point, flags)

			# Remember that we did this {screw_level}:
			screw_level.done = True

		if trace:
		    print "<=Part.screw_holes({0})".format(self.name)

    def screw_level_find(self, screw_name):
	""" Part internal: Return the {Screw_Level} associated with {screw_name}
	    in {self}."""

	# Iterate across {screw_levels} in {self}:
	screw_level = None
	for screw_level_table in self.screw_levels.values():
            # Is {screw} name in {screw_level_table}:
            if screw_name in screw_level_table:
		# Got it:
		screw_level = screw_level_table[screw_name]
	assert screw_level != None, "No screw named '{0}' in part '{1}'". \
	  format(screw_name, self.name)

	return screw_level


    def screw_through(self, comment, \
      screw, start_point, flags, countersink_diameter = Length.inch(0)):
	""" Part construct: Make a hole for {screw} in {self} with starting
	    at {start_point} all the way through {part}.  {comment} will
	    show in any error messages and any generated G-code.
	    The allowed flag letters in {flags} are:

	      One of 'd', 'c' (default), or 's':
		'd' hole is to be tapped (i.e. threaDed)
		'c' hole is a close fit (i.e. Close fit)
		's' hole is a loose fit (i.e. LooSe fit)

	      Allowed additional flags:	  
		'u' upper hole edge should be chamfered (i.e. Upper)
		'l' lower hole edge should be chamfered (i.e. Lower)
		'm' hole is to be milled (i.e. Milled)
		'i' imperial vs. metric swapping allowed (i.e. Interchangeable)
		'a' counterink hole for a flAthead screw

	    """

	screw_diameter = self.screw_diameter(screw, flags)
	if flags.find('a') >= 0:
	    countersink_diameter = self.screw_diameter(screw, '!')

	#print "Part.screw_through: Part={0} screw={1} flags={2} cs={3}". \
	#  format(self.name, screw, flags, countersink_diameter)

	self.hole_through(comment, screw_diameter, \
	  start_point, flags, countersink_diameter)

    def show(self, indent):
	""" Part debug: Show {self} indented with {indent}. """

	print "%sPart: name='%s'" % (indent, self.name)
	for part in self.parts.values():
	    part.show(indent + " ")

    def simple_pocket(self, comment, \
      corner1_point, corner2_point, radius, flags):
	""" Part construct: Mill a pocket in {self} where {corner1_point}
	    and {corner2_point} specify a diagonal across the pocket.  The
	    radius of the inside corners is {radisu}.  {flags} can have
	    the character 't' for a pocket that goes {self} and 'u' to
	    specify that an upper chamfer is requested.  {comment} will
	    show up in error messages and any generated G-code. """

	# Verify that each flag in {flags} is OK:
	for flag in flags:
	    assert flag == 'u' or flag == 't', \
	      'simple_pocket("{0}"): Bad flag "{1}" in "{2}" for part {3}'. \
	      format(comment, flag, flags, self.name)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	if xml_stream != None:
	    # <Simple_Pocket C1X= C1Y= C1Z= C2X= C2Y= C2Z= ...
	    #  ... Radius= Flags= Comment= />:
	    xml_stream.write('{0}<Simple_Pocket'.format(" " * xml_indent))
	    xml_stream.write(' C1X="{0}" C1Y="{1}" C1Z="{2}"'. \
	      format(corner1_point.x, corner1_point.y, corner1_point.z))
	    xml_stream.write(' C2X="{0}" C2Y="{1}" C2Z="{2}"'. \
	      format(corner2_point.x, corner2_point.y, corner2_point.z))
	    xml_stream.write(' Radius="{0}" Flags="{1}" Comment="{2}"/>\n'. \
	      format(radius, flags, comment))

    def manufacture(self):
	""" Part: Override this method to do any manufacturing steps. """

	print("No manufacture method for '{0}'".format(self))

    def _manufacture(self):
	""" Part: Output the XML for *self* to *xml_stream*
	    indented by *indent*. """

	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	xml_indent = ezcad._xml_indent

	children = self._children
	places_values = self._places.values()

	# Output "<Part ...>" to *xml_stream*:
	xml_stream.write('{0}<Part Name="{1}" Parts="{2}" Places="{3}">\n'. \
	  format(" " * ezcad._xml_indent,
	  self._name, len(children), len(places_values)))
	
	# Output all of the manufacturing XML for *self* to *xml_stream*:
	ezcad = self._ezcad
	ezcad.xml_indent_push()
	for xml_line in self._xml_lines:
	    xml_stream.write("{0}{1}\n". \
	      format(" " * ezcad._xml_indent, xml_line))

	self.construct()

	# Output all of the XML for the child parts of *self* to *xml_stream*:
	for child in children:
	    child._manufacture()

	# Output each placement as well:
	for place in places_values:
	    home_part = place.home_part
	    placed_part = place.placed_part
	    xml_stream.write(
	      '{0}<Place Part_Path="{1}" Place_Name="{2}"'.format(
	      " " * ezcad._xml_indent, placed_part._name, place.place_name))
	    center_point = place.center_point
	    xml_stream.write(' CX="{0}" CY="{1}" CZ="{2}"'.format( \
	      center_point.x, center_point.y, center_point.z))
	    axis_point = place.axis_point
	    xml_stream.write(' AX="{0}" AY="{1}" AZ="{2}" Angle="{3}"'. \
	      format(axis_point.x, axis_point.y, axis_point.z, \
	      place.rotate_angle))
	    translate_point = place.translate_point
	    xml_stream.write(' DX="{0}" DY="{1}" DZ="{2}"/>\n'.format( \
	       translate_point.x, translate_point.y, translate_point.z))

	#def start(self, name):
	#""" Part (part tree mode): Create a new {Part} with a name of {name}
	#    and a parent of {self}. """

	#parent = self
	#parent_parts = parent.parts
	#ezcad = parent.ezcad
	#if ezcad.part_tree_mode():
	#    # We are building the part tree:
	#    #print "=>Part.start('%s', '%s')" % (self.name, name)

	#    # Check for duplicates:
	#    assert not (name in parent_parts), \
	#      "Part '%s' is duplicated in part '%s'" % (name, parent.name)

	#    # No duplicate {name}; create {part} and add it to {parent_parts}:
	#    part = Part(name, self)
	#    parent_parts[name] = part

	#   # Now push part on the {ezcad} part stack.
	#   ezcad.part_push(part)

	#    #print "<=Part.start('%s', '%s')" % (self.name, name)
	#else:
	#    # We are not building the part tree, so just return the
	#    # appropriat part:
	#    part = parent_parts[name]

        #   # Reset {screw_last}:
	#   part.screw_last = None

	#    if self.construct_mode():
	#	ezcad = self.ezcad
	#	xml_stream = ezcad.xml_stream
	#	xml_stream.write( \
	#	  '{0}<Part Name="{1}" Parts="{2}" Places="{3}">\n'.format( \
	#	  ezcad._xml_indent, name, len(part.parts.keys()), \
	#	  len(part.places.keys())))
	#	ezcad.xml_indent_push()
		
	#return part

	ezcad.xml_indent_pop()
	xml_stream.write("{0}</Part>\n".format(" " * ezcad._xml_indent))

    def string(self, string_path):
	""" Part dimensions: Return the {String} associated with {string_path}
	    starting from {self}. """
	
	return self.value_lookup(scalar_path, Part.STRINGS)

    def string_set(self, string_name, string_value):
	""" Point dimensions: Store Set the value of {string_name} in {self}
	    to {string_value}.  In addition, {string_value} is returned. """

	return self.value_set(self, string_name, string_value, Part.STRINGS)

    def tool_prefer(self, tool_name):
	""" Part construct: Cause {tool_name} to be the preferred tool
	    for {self}.  If {tool_name} is an empty string, the preferred
	    tool is cleared. """

	if self.construct_mode():
	    ezcad = self.ezcad
	    xml_stream = ezcad.xml_stream
	    xml_stream.write( \
	      '{0}<Tool_Prefer Tool_Name="{1}"/>\n'. \
	      format(ezcad._xml_indent, tool_name))

    def tooling_plate(self, comment, flags, trace = False):
	""" Part construct: Cause a grid of tooling plate holes to be
	drilled into {self}.  {flags} are used to adjust the position
	the tooling plate holes.  The grid is 2 row by 2 column
	(i.e. 2 by 2) but {flags} can be modified to specifically
	set the number of rows and/or columns.  For example,
	"3r 4c" establishes a grid that 3 rows by 4 columns.
	The grid holes are initially distributed to just fill
	the {sefl} bounding box in the X and Y dimensions.
	Additional flags can be specified to move the holes
	around a little.  Tooling plate holes are specified by
	row and column 	where a number specifies the row and an
	upper case letter specifies the column.  The row numbers
	start with 1 on the "north" side and move southwards.
	The column letters start with the letter 'A' on the "west"
	and move eastwards.  Lower case letters 'e' (for East),
	'n' (for North), 's' (for South), and 'w' (for west) are used
	to move a tooling plate hole east, north, south, or west
	respectively.  The lower case letter 'x' (for eXclude)
	can be used to remove a tooling hole  A tooling hole
	can be moved by following it by one or more movement letters.
	The following example "5r 5c 2Bnw 2Dne 3Cx 4Bsw 4Dse" creates
	a 5x5 grid of tooling holes, the middle hole is removed "3Cr"
	and 4 of the tooling holes on the inside are moved outward
	from the center. """

	#if self.construct_mode():
	if True:
	    # Parse {flags}:

	    # {adjusts} lists any holes that have been moved:
	    adjusts = {}

	    # {removes} lists any holes that been removed or ignored:
	    removes = {}

	    # Initialize some variables for the parsing process:
	    column = 0
	    columns = 2
	    number = 0
	    row = 0
	    row_column = (0, 0)
	    rows = 2
	    adjusts[row_column] = (0, 0)

	    # Iterate across {flags}:
	    for flag in flags:
		if '0' <= flag and flag <= '9':
		    # We have a decimal digit, add it to {number}:
		    number = number * 10 + ord(flag) - ord('0')
		else:
		    # We have something other than a decimal digit:
		    if 'A' <= flag and flag <= 'Z':
			# We have a column letter
			column = ord(flag) - ord('A')
			row = number - 1
			row_column = (row, column)
			if not (row_column in adjusts):
			    adjusts[row_column] = (0, 0)
		    elif flag == 'c':
			columns = number
			if trace:
			    print "columns=", columns
		    elif flag == 'e':
			adjust = adjusts[row_column]
			adjusts[row_column] = (adjust[0] + 1, adjust[1])
		    elif flag == 'i':
			removes[row_column] = 'i'
		    elif flag == 'n':
			adjust = adjusts[row_column]
			adjusts[row_column] = (adjust[0], adjust[1] + 1)
		    elif flag == 'r':
			rows = number
			if trace:
			    print "rows=", rows
		    elif flag == 's':
			adjust = adjusts[row_column]
			adjusts[row_column] = (adjust[0], adjust[1] - 1)
		    elif flag == 'w':
			adjust = adjusts[row_column]
			adjusts[row_column] = (adjust[0] - 1, adjust[1])
		    elif flag == 'x':
			removes[row_column] = 'x'
		    elif flag == ' ':
		        number = 0
		    else:
			assert False, \
			  "Bad flag letter '{0}' in flags '{1}'". \
			  format(flag, flags)

		    # All non-digit operations reset {number} at the end:
		    number = 0

	    if trace:
		print "removes=", removes
		print "adjusts=", adjusts

	    ezcad = self._ezcad
	    xml_stream = ezcad._xml_stream
	    if xml_stream != None:
		xml_stream.write('{0}<Tooling_Plate Rows="{1}" '. \
		  format(" " * ezcad._xml_indent, rows))
		xml_stream.write('Columns="{0}" Comment="{1}">\n'. \
		  format(columns, comment))
	    
		ezcad.xml_indent_push()
		for row in range(0, rows):
		    for column in range(0, columns):
			row_column = (row, column)
			adjust = (0, 0)
			if row_column in adjusts:
			    adjust = adjusts[row_column]
			remove = ""
			if row_column in removes:
			    remove = removes[row_column]

			if trace:
			    print "[{0},{1}] = {2}{3}". \
			      format(row, column, adjust, remove)

			xml_stream.write('{0}<Tooling_Hole'. \
			  format(" " * ezcad._xml_indent))
			xml_stream.write(' Row="{0}" Column="{1}"'. \
			  format(row, column))
			xml_stream.write(' Adjust_X="{0}" Adjust_Y="{1}"'. \
			  format(adjust[0], adjust[1]))
			xml_stream.write(' Flags="{0}"/>\n'. format(remove))
		    
		ezcad.xml_indent_pop()
		xml_stream.write('{0}</Tooling_Plate>\n'. \
		  format(" " *ezcad._xml_indent))

    def tooling_plate_mount(self, comment):
	""" Part construction: Cause the mounting plate that holds {self}
	    to be mounted. """

	#if self.construct_mode():
	ezcad = self._ezcad
	xml_stream = ezcad._xml_stream
	if xml_stream != None:
	    ezcad._xml_stream.write( \
	      '{0}<Tooling_Plate_Mount Comment="{1}"/>\n'. \
	      format(" " * ezcad._xml_indent, comment))

    def tube(self, color, material, \
      start_point, end_point, diameter, wall_thickness, sides):
	""" Part dimensions: Create a tube for {self} out of {material}
	    goes from {start_point} to {end_point} is {diameter} round
	    and has a wall thickness of {wall_thickness}.  The tube is
	    visualized with {color}.  {sides} specifies how many sides
	    to use for visualization; setting {sides} to zero gives a
	    reasonable visualization of a tube.  The tube must be
	    aligned with one of the X, Y or Z axes. """

	# Make sure we
	#assert not self.part_tree_mode(), \
	#  "Part.tube: Part '{0}' is in part tree mode".format(self.name)

	# Compute {tube_axis}, the axis along with the tube is aligned:
	tube_axis = end_point - start_point

	# Extract coordinates from {start_point} and {end_point}:
	x1 = start_point.x
	y1 = start_point.y
	z1 = start_point.z
	x2 = end_point.x
	y2 = end_point.y
	z2 = end_point.z

	zero = Length.inch(0)
	radius = diameter.half()
	if tube_axis.x != zero:
	    # Tube aligned on X:
	    t = z1 + radius
	    b = z1 - radius
	    n = y1 + radius
	    s = y1 - radius
	    if x1 < x2:
		w = x1
		e = x2
	    else:
		w = x2
		e = x1
	elif tube_axis.y != zero:
	    # Tube aligned on Y:
	    t = z1 + radius
	    b = z1 - radius
	    if y1 < y2:
		s = y1
		n = y2
	    else:
		s = y2
		n = y1
	    e = x1 + radius
	    w = x1 - radius
	elif tube_axis.z != zero:
	    # Tube aligned on Z:
	    if z1 < z2:
		b = z1
		t = z2
	    else:
		b = z2
		t = z1
	    n = y1 + radius
	    s = y1 - radius
	    e = x1 + radius
	    w = x1 - radius
	else:
	    assert not self.construct_mode(), \
 	      "Tube is not aligned with X, Y, or Z axis"
	    t = z2
            b = z1
	    n = y2
	    s = y1
	    w = x1
	    e = x2

	# Compute the tube corners:
	bsw = self.point(w, s, b)
	tne = self.point(e, n, t)
	#print "bsw={0} tne={1}".format(bsw, tne)

	# Record the material in {self}:
	self._material = material

	#if self.dimensions_mode():
        #    self.bounding_box_update(w, s, b, e, n, t)

	self._bounding_box_update(w, s, b, e, n, t)

	# In consturct mode, output the <Tube ...> line:
	#if self.construct_mode():
	self._xml_lines.append( ('<Tube SX="{0}" SY="{1}" SZ="{2}"' + \
	  ' EX="{3}" EY="{4}" EZ="{5}" Outer_Diameter="{6}"' + \
	  ' Wall_Thickness="{7}" Sides="{8}" Color="{9}"' + \
	  ' Transparency="{10}" Material="{11}" Comment="{12}"/>') . \
	  format(x1, y1, z1, x2, y2, z2, diameter, wall_thickness, sides, 
	  color, self._transparency, material, self._name))

    def value_lookup(self, path, flavor):
	""" Part internal: Return the value for for {path} starting
	    from {self}.  {flavor} specifies the type to lookup. """

	if self.dimensions_refine_mode() or self.construct_mode():
	    # We are in a mode where {path} is actually looked up:

	    # Split the {part_path} and {point_name} from {point_path}:
	    part_path_value_name = path.split('.')
	    if len(part_path_value_name) == 1:
		part = self
		value_name = path
	    elif len(part_path_value_name) == 2:
		part_path = part_path_value_name[0]
		value_name = part_path_value_name[1]

		# Now iterate across {part_path} starting from {self}:
		part = self
		for part_name in part_path.split('/'):
		    # {part_name} is the next component of {part_path}:
		    if part_name == "..":
			# Move up the part tree towards the root:
			part = part.parent

			# Check for going too far up tree:
			if part.name == "":
		            assert False, \
			      "Path '%s' goes too far up the Part tree" % (path)
		    else:
			# Move down the tree:
			parts = part.parts
			if part_name in parts:
			    part = parts[part_name]
			else:
			    assert False, \
			      "Part path '%s' does not contain part '%s'" % \
			      (path, part.name)
	    else:
		# We have either an empty path, or one with two or more '.':
		assert False, "Path '%s' is not valid" % (point_path)

	    # Use {flavor} to select the {values} dictionary to use:
	    if flavor == Part.SCALARS:
		values = self.scalars
	    elif flavor == Part.ANGLES:
		values = self.angles
	    elif flavor == Part.LENGTHS:
		values = self.lengths
	    elif flavor == Part.POINTS:
		values = self.points
	    elif flavor == Part.SCREWS:
		values = self.screws
	    else:
		assert False
	    
	    # Now lookup {value_name} in {values}:
	    if value_name in values:
		value = values[value_name]
	    else:
		assert False, \
		  "Can not find '{0}' in path '{1}' starting from part {2}". \
		  format(value_name, path, self.name)
	else:
	    # We are in a mode where {path} is ignored, and an empty
	    # value is returned:
	    if flavor == Part.SCALARS:
		value = 0.0
	    elif flavor == Part.ANGLES:
		value = Angle(0.0)
	    elif flavor == Part.LENGTHS:
		value = Length(0.0)
	    elif flavor == Part.POINTS:
		zero = Length(0.0)
		value = Point(self, zero, zero, zero)
	    elif flavor == Part.SCREWS:
		# Create a bogus {Screw}, that will not actually be used:
		value = Screw(self, "", "", "TB")
	    else:
		assert False

	return value

    def value_set(self, value_name, value, flavor):
	""" Part (internal): Store {value} into {self} under the
	    name {value_name} using the {flavor} dictionary.  In all cases,
	    {value} is returned. """

	# Select the {values} dictionary based on {flavor}:
	if flavor == Part.ANGLES:
	    values = self.angles
	    flavor_name = "Angle"
	elif flavor == Part.LENGTHS:
	    values = self.lengths
	    flavor_name = "Length"
	elif flavor == Part.POINTS:
	    values = self.points
	    flavor_name = "Point"
	elif flavor == Part.SCALARS:
	    values = self.scalars
	    flavor_name = "Scalar"
	elif flavor == Part.SCREWS:
	    values = self.screws
	    flavor_name = "Screw"
	else:
	    assert False

	# Routine behavior depends upon mode:
	if self.dimensions_define_mode():
	    # In define mode, we make sure that no duplicates occur:
	    assert not (value_name in values), \
	      "{0} name '{1}' is a duplicate in Part '{2}'". \
	      format(flavor_name, value_name, self.name)
	    values[value_name] = value
	elif self.dimensions_refine_mode():
	    # In refine mode, we make sure that {value_name} is defined:
	    assert value_name in values, \
	      "{0} name '{1}' is undefined in part '{2}'". \
	      format(flavor_name, angle_name, self.name)

	    # Now check to see if the value is actually changed:
	    previous_value = values[value_name]
	    if value != previous_value:
		values[value_name] = value
		self.dimensions_changed("value_set['%s']" % (value_name))
	elif self.part_tree_mode():
	    # Make sure we are not in part tree mode:
	    assert False, "Setting value in part tree mode"
	# else we are in construct mode and do nothing:

	return value

    def vertical_lathe(self, comment, axis_start_point, axis_end_point, \
      inner_diameter, outer_diameter, flags):
	""" Part construct: Mill out a tube of material from {self} along
	    the axis from {axis_start_point} to {axis_end_point} where
	    {inner_diameter} and {outer_diameter} specify the tube
	    inside and outside diameter.  {flags} can be 'i' to specify
	    that only the inside diameter matters, allowing for an end-mill
	    that extends past outside_diameter.  {comment} is used in
	    error messages and any generated G-code. """

	# Verify that each flag in {flags} is OK:
	for flag in flags:
	    assert flag == 'i', \
	      "verical_lathe('{0}'): Bad flag '{1}' in '{2}' for part {3}". \
	      format(comment, flag, flags, self.name)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	if xml_stream != None:
	    # <Contour SX= SY= SZ= EX= EY= EZ= Engagement= Flags= Comment= />:
	    xml_stream.write('{0}<Vertical_Lathe'.format(" " * xml_indent))
	    xml_stream.write(' SX="{0}" SY="{1}" SZ="{2}"'. \
	      format(axis_start_point.x, axis_start_point.y,
	      axis_start_point.z))
	    xml_stream.write(' EX="{0}" EY="{1}" EZ="{2}"'. \
	      format(axis_end_point.x, axis_end_point.y, axis_end_point.z))
	    xml_stream.write(' Inner_Diameter="{0}" Outer_Diameter="{1}"'. \
	      format(inner_diameter, outer_diameter))
	    xml_stream.write(' Flags="{0}" Comment="{1}"/>\n'. \
	      format(flags, comment))

    def vice_position(self, comment, surface_point, north_point, west_point):
	""" Part construct: Cause {self} to be mounted in a vice with
	    {surface_point} as the top surface, {north_point} as the edge
	    mounted against the top vice edge, and {west_point} as the edge
	    left pointing edge of {self}.  {comment} is the attached
	    to any generated G-code. """

	# Before we get too far, flush any pending screw holes
	# from the previous mounting:
	if self._top_surface_set:
            self.screw_holes(True)

	# Extract some values from {ezcad}:
	ezcad = self._ezcad
	xml_indent = ezcad._xml_indent
	xml_stream = ezcad._xml_stream

	corner1 = self.tne
	corner2 = self.bsw
	cx = (corner1.x + corner2.x).half()
	cy = (corner1.y + corner2.y).half()
	cz = (corner1.z + corner2.z).half()

	# <Vice_Position TX= TY= TZ= NX= NY= NZ= WX= WY= WZ= CX= CY= CZ=/>:
	if xml_stream != None:
	    xml_stream.write( \
	      '{0}<Vice_Position TX="{1}" TY="{2}" TZ="{3}"'. \
	      format(" " * xml_indent, surface_point.x, surface_point.y,
	      surface_point.z))
	    xml_stream.write( \
	      ' NX="{0}" NY="{1}" NZ="{2}"'.format( \
	      north_point.x, north_point.y, north_point.z))
	    xml_stream.write(' WX="{0}" WY="{1}" WZ="{2}"'.format( \
	      west_point.x, west_point.y, west_point.z))
	    xml_stream.write(' CX="{0}" CY="{1}" CZ="{2}"'.format(cx, cy, cz))
	    xml_stream.write(' Comment="{0}"/>\n'.format(comment))
	self._top_surface = surface_point
	self._top_surface_set = True

class Place:
    """ A {Place} represents the placement of a part relative to the
	origin of an assembly. """

    def __init__(self, place_name, home_part, placed_part, \
      center_point, axis_point, rotate_angle, translate_point):
	""" Place: Initialize {self} to contain {home_part}, {placed_part},
	    {center_point}, {axis_point}, {rotate_angle}, and
	    {translate_point}. """

	assert isinstance(place_name, str)
	assert isinstance(home_part, Part)
	assert isinstance(placed_part, Part)
	assert isinstance(center_point, Point)
	assert isinstance(axis_point, Point)
	assert isinstance(rotate_angle, Angle)
	assert isinstance(translate_point, Point)

	#print "Place({0}, {1}, {2}, {3}, {4}, {5})". \
	#  format(home_part.name, placed_part.name, center_point, \
	#  axis_point, rotate_angle, translate_point)

	# Extract some values from {rotate_center}:
	center_x = center_point.x.inches()
	center_y = center_point.y.inches()
	center_z = center_point.z.inches()

	# Extract some values from {axis_point}:
	axis_x = axis_point.x.inches()
	axis_y = axis_point.y.inches()
	axis_z = axis_point.z.inches()
	#print "axis=({0},{1},{2})".format(axis_x, axis_y, axis_z)

	# Normalize rotate axis:
	axis_length = \
	  math.sqrt(axis_x * axis_x + axis_y * axis_y + axis_z * axis_z)
	#print "axis_length=", axis_length
	x = axis_x / axis_length
	y = axis_y / axis_length
	z = axis_z / axis_length

	rotate_matrix = Matrix.rotate_create(x, y, z, rotate_angle)

	# Create {center_matrix} and {center_reverse_matrix}:
	center_matrix = Matrix.translate_create(-center_x, -center_y, -center_z)
	center_reverse_matrix = \
	  Matrix.translate_create(center_x, center_y, center_z)

	# Extract some values from {translate_point}:
	t_x = translate_point.x.inches()
	t_y = translate_point.y.inches()
	t_z = translate_point.z.inches()

	# Create {translate_matrix}:
	translate_matrix = Matrix.translate_create(t_x, t_y, t_z)
	#print "translate_matrix=\n", translate_matrix

	#print "Place(): cm=\n{0}\nrm=\n{1}\nrcm=\n{2}\ntm=\n{3}\n". \
	#  format(center_matrix.mat, rotate_matrix.mat, \
	#  center_reverse_matrix.mat, translate_matrix.mat)

	# Compute {forward_matrix} and {reverse_matrix}:
	forward_matrix = center_matrix * \
	  rotate_matrix * center_reverse_matrix * translate_matrix
	reverse_matrix = forward_matrix.inverse()
	#print "Place(): forward=\n{0}\nreverse=\n{0}\n". \
	#  format(forward_matrix.mat, reverse_matrix.mat)

	# Load up {self}:
	self.place_name = place_name
	self.forward_matrix = forward_matrix
	self.home_part = home_part
	self.placed_part = placed_part
	self.translate_point = translate_point
	self.reverse_matrix = reverse_matrix
	self.center_point = center_point
	self.axis_point = axis_point
	self.rotate_angle = rotate_angle

    def __eq__(self, place):
	""" Place: Return {True} if {self} is equal to {place}. """

	home_part_changed = self.home_part != place.home_part
	placed_part_changed = self.placed_part != place.placed_part
	center_point_changed = self.center_point != place.center_point
	axis_point_changed = self.axis_point != place.axis_point
	rotate_angle_changed = self.rotate_angle != place.rotate_angle
	translate_point_changed = self.translate_point != place.translate_point

	changed = home_part_changed or placed_part_changed or \
	  center_point_changed or translate_point_changed or \
	  axis_point_changed or rotate_angle_changed

	#if changed:
	#    print "home_part_changed=", home_part_changed
	#    print "placed_part_changed=", placed_part_changed
	#    print "location_changed=", location_part_changed
	#    print "axis_point_changed=", axis_point_changed
	#    print "rotate_angle_changed=", rotate_angle_changed

	result = not changed
	#print "Place.__eq__() =>", result
	return result

    def __ne__(self, place):
	""" Place: Return {True} if {self} is not equal to {place}. """

	return not (self == place)

class Point:
    """ {Point} represents a point in 3-space associated with a specific
	{Part} to provide the frame of reference. """

    def __init__(self, part, x, y, z):
	""" Point: Intialize {self} to contain {part}, {x}, {y}, {z}. """

	self.part = part
	self.x = x
	self.y = y
	self.z = z

    def __add__(self, point):
	""" Point: Add {point} to {self}. """

	assert isinstance(point, Point)
	assert self.part == point.part, \
	  "Can not add a point for part '%s' to a point for part '%s'" % \
	   (self.part.name, point.part_name)

	return Point(self.part, \
	  self.x + point.x, self.y + point.y, self.z + point.x)

    def __div__(self, scalar):
	""" Point: Return the result of dividing {self} by {scalar}. """

	return Point(self.part, \
	  self.x / scalar, self.y / scalar, self.z / scalar)

    def __eq__(self, point):
	""" Point: Return {True} if {self} is equal to {point}. """

	assert isinstance(point, Point)
	return self.x == point.x and self.y == point.y and self.z == point.z

    def __mul__(self, scalar):
	""" Point: Return the result of muliplying {self} by {scalar}. """

	return Point(self.part, \
	  self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar):
	""" Point: Return the result of muliplying {self} by {scalar}. """

	return Point(self.part, \
	  self.x * scalar, self.y * scalar, self.z * scalar)

    def __ne__(self, point):
	""" Point: Return {True} if {self} is not equal to {point}. """

	assert isinstance(point, Point)
	return self.x != point.x or self.y != point.y or self.z != point.z

    def __neg__(self):
	""" Point: Return the negative of {self}. """

	return Point(self.part, -self.x, -self.y, -self.z)

    def __str__(self):
	""" Point: Return {self} as a formatted string. """

	return "('{0}': {1}, {2}, {3})".format( \
	  self.part._name, self.x, self.y, self.z)

    def __sub__(self, point):
	""" Point: Subtract {point} from {self}. """

	assert isinstance(point, Point)
	assert self.part == point.part, \
	  "Can not subtract point for part '%s' from a point for part '%s'" % \
	   (point.part.name, self.part.name)

	return Point(self.part, \
	  self.x - point.x, self.y - point.y, self.z - point.z)

    def angle_between(self, point):
	""" Point dimensions: Return the angle between {self} and {point}. """

	# a . b = ||a|| ||b|| cos <AB		(1)
	# (a . b) / (||a|| ||b||) = cos <AB	(2)
	# acos [(a . b) / (||a|| ||b||)] = <AB	(3)

	x1 = self.x.inches()
	y1 = self.y.inches()
	z1 = self.z.inches()
	x2 = point.x.inches()
	y2 = point.y.inches()
	z2 = point.z.inches()
	dot_product = x1 * y1 + x2 * y2 + z1 * z2
	length1 = math.sqrt(x1 * x1 + y1 * y1 + z1 * z1)
	length2 = math.sqrt(x2 * x2 + y2 * y2 + z2 * z2)
	
	return Angle.rad(math.acos(dot_product / (length1 * length2)))

    def cross_product(self, point):
	""" Point dimensions: Return the cross product of {self}
	    with {point}. """

	ux = self.x.inches()
	uy = self.y.inches()
	uz = self.z.inches()
	vx = point.x.inches()
	vy = point.y.inches()
	vz = point.z.inches()

	assert self.part == point.part, \
	  "Point.cross_product: Mis-matched parts"

	inch = Length.inch
	return Point(self.part, inch(uy * vz - uz * vy),
	  inch(uz * vx - ux * vz), inch(ux * vy - uy * vx))

    def half(self):
	""" Point dimensions: Return {self} / 2. """

	result = self / 2.0
	return result	

    def length(self):
	""" Point dimensions: Return the length of self. """

	x = self.x.inches()
	y = self.y.inches()
	z = self.z.inches()
	return Length.inch(math.sqrt(x * x + y * y + z * z))

    def matrix_create(self):
	""" Matrix public: Create a matrix that corresponds to {self}. """

	result = Matrix(   [[ \
	  self.x.inches(), \
	  self.y.inches(), \
	  self.z.inches(), \
	  1                ]] )

	return result

    def points(self, dx, dy, dz):
	""" Part construct: Return a list of points centered around
	    {self} that are separated by {dx} in X, {dy} in Y and {dx}
	    in Z.  If all of {dx}, {dy}, {dz} are non-zero, 8 {Point}'s are
	    returned.  If one of {dx}, {dy}, and {dz} is zero, 4 {Point}'s
	    are returned.  If two of {dx}, {dy}, and {dz} are zero, only
	    2 {Point}'s are returned. """

	# Extract some values from {part}:
	part = self.part
	x = self.x
	y = self.y
	z = self.z

	# Construct {x_list}, {y_list}, {z_list} to have either 1 or 2 value
	# depending upon whether {dx}, {dy}, {dz} is zero, repsectively:
	zero = Length.inch(0)
	if dx == zero:
	    x_list = (x)
	else:
            half_dx = dx.half()
	    x_list = (x - half_dx, x + half_dx)

	if dy == zero:
	    y_list = (y)
	else:
            half_dy = dy.half()
	    y_list = (y - half_dy, y + half_dy)

	if dz == zero:
	    z_list = (z)
	else:
            half_dz = dz.half()
	    z_list = (z - half_dz, z + half_dz)

	# Now iterate over {x_list}, {y_list}, and {z_list}
	# to generate {result}:
	result = []
	for x in x_list:
	    for y in y_list:
		for z in z_list:
		    point = Point(part, x, y, z)
		    result.append(point)

	return result

    def twice(self):
	""" Point dimensions: Return {self} * 2. """

	return self * 2.0

    def x_adjust(self, x):
	""" Point dimensions: Return copy of {self} with {x} added to the
	    x field. """

	return Point(self.part, self.x + x, self.y, self.z)

    def xy_adjust(self, x, y):
	""" Point dimensions: Return copy of {self} with {x} added to the
	    x field and {y} added to the y field. """

	return Point(self.part, self.x + x, self.y + y, self.z)

    def xyz_adjust(self, x, y, z):
	""" Point dimensions: Return copy of {self} with {x} added to the
	    x field, {y} added to the y field, and {z} added to the z field. """

	return Point(self.part, self.x + x, self.y + y, self.z + z)

    def xz_adjust(self, x, z):
	""" Point dimensions: Return copy of {self} with {x} added to the
	    x field and {z} added to the z field. """

	return Point(self.part, self.x + x, self.y, self.z + z)

    def y_adjust(self, y):
	""" Point dimensions: Return copy of {self} with {y} added to the
	    y field. """

	return Point(self.part, self.x, self.y + y, self.z)

    def yz_adjust(self, y, z):
	""" Point dimensions: Return copy of {self} with {y} added to the
	    y field and {z} added to the z field. """

	return Point(self.part, self.x, self.y + y, self.z + z)

    def z_adjust(self, z):
	""" Point dimensions: Return copy of {self} with {z} added to the
	    z field. """

	return Point(self.part, self.x, self.y, self.z + z)

class Screw:
    """ Screw """

    def __init__(self, part, name, thread, direction):
	""" Screw internal: Initialize {self} with {thread} ..."""

	assert direction == "NS" or direction == "EW" or direction == "TB", \
	  "Screw direction '{0}' must be either 'NS', 'EW', or 'TB'"

	#print "Screw(part={0}, name={1}, thread={2}, dir={3})". \
	#  format(part.name, name, thread, direction)

	# Load up {self}:
	self.anchor_point_mapped = None
	self.anchor_point_original_part = None
	self.anchor_screw_level = None
	self.direction = direction
	self.name = name
	self.part = part
	self.screw_levels = {}
	self.thread = thread

    def anchor_set(self, anchor_point):
	""" Screw dimensions: Set the anchor point for {self} to
	    {anchor_point}. """

	trace = False
	#trace = self.name.find("skin_west_bottom") >= 0

	if trace:
	    print "=>Screw.anchor_set({0}, {1})".format(self.name, anchor_point)
	    anchor_part = anchor_point.part
	    bsw = anchor_part.point("$BSW")
	    tne = anchor_part.point("$TNE")
	    print "bsw={0}".format(bsw)
	    print "tne={0}".format(tne)

	part = self.part
	if part.dimensions_refine_mode():
	    # Grab some values from {self} and {anchor_point}:
            anchor_point_original = anchor_point
	    anchor_point_original_part = anchor_point_original.part
	    anchor_screw_level = self.anchor_screw_level

	    # If {anchor_screw_level} is not defined, search for it:
	    if anchor_screw_level == None:
		# Now find the {Screw_Level}} that matches
		# {anchor_point_original_part}:
		for screw_level in self.screw_levels.values():
		    assert screw_level.screw == self
		    if screw_level.part == anchor_point_original_part:
			anchor_screw_level = screw_level
			break

		# Make sure we found an anchor level that matched:
		assert anchor_screw_level != None, \
		  "Screw '{0}' is not attached to part '{1}'". \
		  format(self.name, anchor_point_original_part.name)
	    assert anchor_screw_level.screw == self

            # Make sure that we are not attempting to define 2 anchor points:
	    anchor_screw_level_part = anchor_screw_level.part
	    assert anchor_screw_level_part == anchor_point_original_part, \
	      "Screw anchor should be in part {0} instead of part {1}". \
	      format(anchor_screw_level_part.name, \
	      anchor_point_original_part.name)

            # Grab some values from {anchor_level}:
	    anchor_forward_matrix = anchor_screw_level.forward_matrix

	    # Perform the final subtraction and refernce to {part2}:
	    anchor_point_mapped = \
	      anchor_forward_matrix.point_multiply(anchor_point, part)
            if trace:
		print "anchor_point_mapped={0}".format(anchor_point_mapped)

	    # Get {screw} anchor point set:
	    if self.anchor_screw_level == None:
		self.anchor_screw_level = anchor_screw_level
		self.anchor_point_original_part = anchor_point_original_part
		self.anchor_point_mapped = anchor_point_mapped
		part.dimensions_changed("Screw.anchor_set 1")
	    else:
		if self.anchor_point_mapped != anchor_point_mapped:
                    self.anchor_point_original_part = \
		      anchor_point_original_part
		    self.anchor_point_mapped = anchor_point_mapped
		    part.dimensions_changed("Screw.anchor_set 2")

	if trace:
	    print "<=Screw.anchor_set({0}, {1})".format(self.name, anchor_point)
	    print ""

    def part_matrices_find(self, screw_path):
	""" Screw internal: Return a 2-tuple containing the {Part} and
	    forward matrix associated with {screw_path}. """

	trace = False
	#trace = self.name.find("grip_attach_bottom_south") >= 0

	if trace:
	    print "  =>Screw.part_matrix_find({0}, {1})". \
	      format(self.name, screw_path)
	forward_matrix = Matrix.identity_create()
	reverse_matrix = Matrix.identity_create()

	screw_part = self.part
	target_part = screw_part
	place_names = screw_path.split('/')

	if trace:
	    print "  target_part={0} place_names={1}". \
	      format(target_part.name, place_names)

	for place_name in place_names:
            places = target_part.places
            if not place_name in places:
		print "places=", places
		message = "Invalid place name '{0}'" + \
		  " in screw path '{1}' starting from part '{2}'"
		assert False, \
		  message.format(place_name, screw_path, screw_part.name)

            # Move forward by {place}:
            place = target_part.places[place_name]
	    if trace:
		print "  place={0} place_matrix=\n{1}". \
		  format(place_name, place.forward_matrix)
            forward_matrix = forward_matrix * place.forward_matrix
	    reverse_matrix = reverse_matrix * place.reverse_matrix
	    target_part = place.placed_part

	result = (target_part, forward_matrix, reverse_matrix)
	if trace:
	    print "  <=Screw.part_matrix_find({0}, {1})=>({2}, vvv)\n{3}". \
	      format(self.name, screw_path, target_part.name, forward_matrix)
	return result

    def attach(self, screw_path, surface, flags):
	""" Screw dimensions: Set the ... """

	#print "=>Screw.attach({0}, {1}, {2}, {3})". \
	#  format(self.name, screw_path, surface, flags)

	# Grab some values from {self}:
	screw_part = self.part
	screw_levels = self.screw_levels

	# Find {target_part} and {forward_matrix} associated with {screw_path}:
	part_matrices = self.part_matrices_find(screw_path)
	target_part = part_matrices[0]
	forward_matrix = part_matrices[1]
	reverse_matrix = part_matrices[2]

	if screw_part.dimensions_define_mode():
            # In define mode, we create the new screw level:
	    assert not screw_path in screw_levels, \
	      "Duplicate screw level path '{0}'".format(screw_path)
	    screw_level = Screw_Level(self, screw_path, surface, flags, \
	      target_part, forward_matrix, reverse_matrix)
	    screw_levels[screw_path] = screw_level

	    # Make sure that we store {screw_level} in {target_part}.
	    target_part_screw_levels = target_part.screw_levels
            target_part_screw_levels[surface][self.name] = screw_level
	elif screw_part.dimensions_refine_mode():
	    # Look up the {screw_path}:
	    assert screw_path in screw_levels, \
	      "Undefined screw level path '{0}' in part {1}". \
	      format(screw_path, screw_part.name)
	    screw_level = screw_levels[screw_path]

	    # Update {forward_matrix}:
	    if not screw_level.forward_matrix == forward_matrix:
		screw_level.forward_matrix = forward_matrix
		screw_level.reverse_matrix = reverse_matrix
		screw_part.dimensions_changed("Screw.attach")

	    # Check that anchor actually occured:
            if flags.find('A') >= 0:
		assert self.anchor_screw_level != None, \
		  "Screw '{0}' has no anchor point set".format(self.name)
		#print "anchor_point_map={0}".format(self.anchor_point_mapped)
		assert self.anchor_point_original_part == target_part, \
		  "Screw '{0}' has anchor set to part '{1}' instead of '{2}'".\
		  format(self.name, self.anchor_point_original_part.name, \
		  target_part.name)
	else:
            assert screw_part.construct_mode(), \
	      "Setting screw '{0}' level for '{1}' outside dimensions mode". \
	      format(self.name, screw_path)

	#print "<=Screw.attach({0}, {1}, {2}, {3})". \
	#  format(self.name, screw_path, surface, flags)

    def depth_set(self, target_part, depth):
	""" Screw dimensions: Set the screw hole depth for {self} to {depth}
	    for {part}. """

	root_part = self.part
	if root_part.dimensions_refine_mode():
	    screw_level_match = None
	    for screw_level in self.screw_levels.values():
		assert screw_level.screw == self
		if screw_level.part == target_part:
		    screw_level_match = screw_level
                    break

            # Make sure we found an anchor level that matched:
            assert screw_level_match != None, \
	      "Screw '{0}' is not attached to part '{1}'". \
		  format(self.name, target_part.name)

	    # Set the {depth}:
	    screw_level.depth_set(depth)

class Screw_Level:
    """ Screw Level """

    def __init__(self, screw, screw_path, surface, flags, part, \
      forward_matrix, reverse_matrix):
	""" Screw_Level internal: Initialize {self} with {screw},
	    {screw_path}, {surface}, {flags}, {part}, {forward_matrix}
	    and {reverse_matrix}. """

	#trace = True
	#if trace:
	#    print "Screw_Level({0} {1} {2} {3} {4}): fm=\n{5}\nrm=\n{6}\n". \
	#      format(screw.name, screw_path, surface, flags, part.name, \
	#      forward_matrix.mat, reverse_matrix.mat)

	self.depth = Length.inch(0)
	self.done = False
	self.flags = flags
	self.forward_matrix = forward_matrix
	self.part = part
	self.reverse_matrix = reverse_matrix
	self.screw = screw
	self.screw_path = screw_path
	self.surface = surface

    def __str__(self):
	""" Screw_Level internal: Return {self} as a {String}. """

	return "String_Level(scr={0} path={1} sur={2} flgs={3} part={4} *)". \
	  format(self.screw.name, self.screw_path, self.surface, \
	  self.flags, self.part.name)

    def depth_set(self, depth):
	""" Screw dimensions: Set screw hole depth for {self} to {depth}. """

	if self.depth != depth:
            self.depth = depth
	    self.screw.part.dimensions_changed("Screw_Level.depth_set")

# screw = part.screw_create("screw1", part.screw_new("thread", TB))
# screw.attach("path", "flags", "surface")
# screw.anchor_set(point)
# screw.depth_set(depth)

from numpy import matrix

class Matrix:

    def __init__(self, values):
	""" Matrix public: Initialize {self} to values. """

	self.mat = matrix(values)

    def __eq__(self, m):
	""" Matrix public:  Return {True} if {self} equals {m}. """

	return (self.mat == m.mat).all()

    def __mul__(self, m):
	""" Angle: Return {self} multiplied by {m}. """

	result_mat = self.mat * m.mat
	result = Matrix([[0]])
	result.mat = result_mat
	return result

    @staticmethod
    def identity_create():
	""" Matrix public: Return an identity matrix. """

	result = Matrix([ \
	  [1, 0, 0, 0],   \
	  [0, 1, 0, 0],   \
	  [0, 0, 1, 0],   \
	  [0, 0, 0, 1]  ])
	return result

    def inverse(self):
	""" Matrix public: Return the inverse matrix for {self}. """

	result = Matrix([[0]])
	result.mat = self.mat.I
	return result

    def point_create(self, part):
	""" Matrix public:  Return the {Point} the corresponds to {self}
	    using {part} as the returned {Point}'s reference frame.  {self}
	    must be a 1 x 4 matrix. """

	inch = Length.inch
	mat = self.mat
	x = mat[0, 0]
	y = mat[0, 1]
	z = mat[0, 2]
	point = Point(part, inch(x), inch(y), inch(z))

	return point

    def point_multiply(self, point, part):
	""" Matrix public: Return the point that results from mulitiplying
	    {point} by {self} and converting it back into a {Point} with
	    {part} as the reference frame. """

	point_matrix = point.matrix_create()
	result_matrix = point_matrix * self
	result_point = result_matrix.point_create(part)
	return result_point

    @staticmethod
    def rotate_create(nx, ny, nz, angle):
	""" Matrix public: Return a rotation matrix for rotating around
	    the normalized vector ({nx}, {ny}, {nz}) by {angle}.  {angle}
	    must be of type {Angle}."""

	# Create {rotate_matrix}:
	# 
	# The matrix for rotating by {angle} around the normalized vector
	# ({x},{y},{z}) is:
	#
	# [ xx(1-c)+c   yx(1-c)-zs  zx(1-c)+ys   0  ]
	# [ xy(1-c)+zs  yy(1-c)+c   zy(1-c)-xs   0  ]
	# [ xz(1-c)-ys  yz(1-c)+xs  zz(1-c)+c    0  ]
	# [      0           0          0        1  ]
	#
	# Where c = cos({angle}), s = sin({angle}), {angle} is measured
	# in radians and  vector ({nx}, {ny}, {nz}) must be normalized.

	# Compute some sub expressions:
	c = angle.cosine()
	s = angle.sine()
	omc = 1.0 - c
	x_omc = nx * omc
	y_omc = ny * omc
	z_omc = nz * omc
	xs = nx * s
	ys = ny * s
	zs = nz * s
    
	# Create the matrix:
	matrix = Matrix([ \
	  [nx * x_omc + c,  nx * y_omc - zs, nx * z_omc + ys, 0.0], \
	  [ny * x_omc + zs, ny * y_omc + c,  ny * z_omc - xs, 0.0], \
	  [nz * x_omc - ys, nz * y_omc + xs, nz * z_omc + c,  0.0], \
	  [0.0,             0.0,             0.0,             1.0] ])

	return matrix

    @staticmethod
    def translate_create(dx, dy, dz):
	""" Matrix public: Return a translate matrix containing {dx}, {dy}
	    and {dz}. """

	# Create the matrix:
	matrix = Matrix([ \
	  [1,  0,  0,  0], \
	  [0,  1,  0,  0], \
	  [0,  0,  1,  0], \
	  [dx, dy, dz, 1] ])

	return matrix

