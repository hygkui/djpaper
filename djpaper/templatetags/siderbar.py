from django.template import Library
from django import template
from django.shortcuts import get_object_or_404
from djpaper.models import Tag,Paper
from djpaper.tag_utils import tag_cloud_cal

register = Library()

@register.inclusion_tag('top_10.html',takes_context=True)
def get_top_10_paper(context,number=10):
	papers = Paper.objects.all().order_by('-id')
	if number > len(papers):
		number = len(papers)
	return {'top_10_papers':papers[:number]}

@register.inclusion_tag('tag_cloud_page.html',takes_context=True)
def get_tag_cloud(context):
	tags = tag_cloud_cal()
	return {'tags':tags}
