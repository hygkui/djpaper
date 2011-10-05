from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
ITEMS_PER_PAGE = 15

def paginator_maker(query_set,page):
	paginator = Paginator(query_set,ITEMS_PER_PAGE)
	try:
		obj_list = paginator.page(page)
	except PageNotAnInteger:
		obj_list = paginator.page(1)
	except EmptyPage:
		obj_list = paginator.page(paginator.num_pages)
	return obj_list
		 
