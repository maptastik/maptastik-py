"""
Quick functions Ryan likes to use
Ryan Cooper
10/9/17
file location: C:\Python27\ArcGIS10.2\Lib\site-packages (or ArcGIS Pro environment)
"""

import arcpy
import statistics

def basic_fc_stats(fc, field):
	"""Return a dictionary of basic summary statistics for a field.

	Keyword arguments:
	fc -- Feature class containing the field to summarize
	field -- Field in feature class to summarize
	"""

	field_vals = []
	total = 0
	row_count = 0
	with arcpy.da.SearchCursor(fc, field) as cursor:
		for row in cursor:
			total = total + row[0]
			row_count+=1
			field_vals.append(row[0])
	mean = statistics.mean(field_vals)
	median = statistics.median(field_vals)
	stdev = statistics.stdev(field_vals)
	summary = {'sum': total, 'row_count': row_count, 'mean': mean, 'median': median, 'stdev': stdev}
	return summary

def layer_fields(fc, wild_card=None, field_type='All', field_info=False):
	"""Return a dictionary of information about fields in a feature class.

	Keyword arguments:
	fc -- Feature class to get field information about
	wild_card -- Limits the results returned (Default: None)
	field_type -- Specified type of field is returned (Default: 'All')
	field_info -- Prints returned fields with some info about them
	"""
	fields = arcpy.ListFields(fc, wild_card, field_type)
	field_names = [x.name for x in fields]
	if field_info == True:
		print("FIELDS")
		print("-----")
		for field in fields:
			print("""
Field:	{0}
Type:	{1}
Editable:	{2}
Domain:	{3}
-----
			""".format(field.name, field.type, field.editable, field.domain))
	return {"field_names": field_names, "field_amt": len(fields)}
