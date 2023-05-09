from django.contrib import admin
from .models import Articles, Comments, ArticleImage

# Register your models here.


class ArticlesAdmin(admin.ModelAdmin):
    exclude = ('hearts', 'bookmarks',)


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(ArticleImage)
admin.site.register(Comments)
