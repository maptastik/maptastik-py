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

def addRanks(table, sort_fields, category_field, rank_field='RANK'):
    """Use sort_fields and category_field to apply a ranking to the table.

	Source:
	ArcPy Cafe, "Ranking field values", 8/2/2013, https://arcpy.wordpress.com/2013/08/02/ranking-field-values

    Parameters:
        table: string
        sort_fields: list | tuple of strings
            The field(s) on which the table will be sorted.
        category_field: string
            All records with a common value in the category_field
            will be ranked independently.
        rank_field: string
            The new rank field name to be added.
    """

    # add rank field if it does not already exist
    if not arcpy.ListFields(table, rank_field):
        arcpy.AddField_management(table, rank_field, "SHORT")

    sort_sql = ', '.join(['ORDER BY ' + category_field] + sort_fields)
    query_fields = [category_field, rank_field] + sort_fields

    with arcpy.da.UpdateCursor(table, query_fields,
                               sql_clause=(None, sort_sql)) as cur:
        category_field_val = None
        i = 0
        for row in cur:
            if category_field_val == row[0]:
                i += 1
            else:
                category_field_val = row[0]
                i = 1
            row[1] = i
            cur.updateRow(row)
