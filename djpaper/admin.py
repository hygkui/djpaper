from django.contrib import admin
from djpaper.models import *

class PicInline(admin.StackedInline):
	model = Pic
	extra = 3
class PaperAdmin(admin.ModelAdmin):
	fieldsets =[
		(None , 		  {'fields':['title']}),
		('First author',  {'fields':['first_au']}),
		('Authors' ,	  {'fields':['other_au']}),
		('pub out Info' , {'fields':['publication','pub_date']}),
		('key words' ,    {'fields':['tag']}),
		('abstract of the paper',{'fields':['abstract']}),
	]
	list_display = ('title','first_au','other_authors','pub_date')
	search_fields = ['title','tag__title']
	raw_id_fields = ['publication',]
	inlines = [PicInline]

class TagAdmin(admin.ModelAdmin):
	fields = ('title',)

class CommitAdmin(admin.ModelAdmin):
	list_display = ('content','paper','people','time',)

admin.site.register(People)
admin.site.register(Department)
admin.site.register(Paper,PaperAdmin)
admin.site.register(Pic)
admin.site.register(Tag,TagAdmin)
admin.site.register(Publication)
admin.site.register(Publisher)
admin.site.register(Type)
admin.site.register(ShortMessage)
admin.site.register(Account)
admin.site.register(Commit,CommitAdmin)
