from django.contrib import admin
from djpaper.models import *


class TagAdmin(admin.ModelAdmin):
	fields = ('title',)
admin.site.register(People)
admin.site.register(Department)
admin.site.register(Paper)
admin.site.register(Pic)
admin.site.register(Tag,TagAdmin)
admin.site.register(Publication)
admin.site.register(Publisher)
admin.site.register(Type)
admin.site.register(ShortMessage)
admin.site.register(Account)
admin.site.register(ModeAuth)

