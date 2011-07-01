from django.contrib.syndication.feeds import Feed
from djpaper.models import Paper

class RecentPapers(Feed):
	title = 'Django Papers | Recent Papers '
	link = '/papers/recent/'
	description = 'Recent papers posted to Django Djpaer Papers'
	
	def items(self):
		return Paper.objects.order_by('-id')[:10]

