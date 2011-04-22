from django.contrib import admin
from djpaper.models import *



##class AuthorAdmin(admin.ModelAdmin):
##	list_display = ( 'first_name' , 'last_name' , 'email' )
##	search_fields = ( 'first_name', 'last_name')
##class BookAdmin(admin.ModelAdmin):
##	list_display = ( 'title','publisher','publication_date')
##	list_filter = ( 'publication_date' , )
##	date_hierarchy = 'publication_date'
##	ordering = ('-publication_date',)
##	fields = ('title','author','publisher','publication_date')
##	filter_horizontal = ('author',)
##	raw_id_fields = ('publisher',)
##class PublisherAdmin(admin.ModelAdmin):
##	search_fields = ('name',)
##

class TagAdmin(admin.ModelAdmin):
	fields = ('title',)
admin.site.register(People)
admin.site.register(Department)
admin.site.register(DepartmentChild)
admin.site.register(Paper)
admin.site.register(Pic)
admin.site.register(Tag,TagAdmin)
admin.site.register(Publication)
admin.site.register(Publisher)
admin.site.register(Type)
admin.site.register(ShortMessage)


