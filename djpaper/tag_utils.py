from djpaper.models import Tag 

import os
def tag_cloud_cal():
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('title')
	if not tags:
		return 
	min_count = max_count = tags[0].paper_set.count() 
	for tag in tags:
		tag.count = tag.paper_set.count()
		if tag.count < min_count:
			min_count = tag.count
		if tag.count > max_count:
			max_count = tag.count
	# calculate count range ,avoid dividing by zero.	
	range = float( max_count - min_count )
	if range == 0.0:
		range = 1.0
	#calculate tag weight
	for tag in tags:
		tag.weight = int(
			MAX_WEIGHT * (tag.count - min_count ) / range
		)
	return tags


