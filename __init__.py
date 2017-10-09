"""
Quick functions Ryan likes to use
Ryan Cooper
10/9/17
file location: C:\Python27\ArcGIS10.2\Lib\site-packages (or ArcGIS Pro environment)
"""

import arcpy
import statistics

def basic_fc_stats(fc, field):
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