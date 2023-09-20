from django.contrib import admin
from .models import Blog
from .models import Contact
from .models import Subscribers
from .models import MailMessage
from .models import Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "status", "created_on")
    list_filter = ("status",)
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "name", "status", "email", "publish")
    list_filter = ("status", "publish")
    search_fields = ["name", "email", "content"]


admin.site.register(Blog, BlogAdmin)


admin.site.register(Contact)
admin.site.register(Subscribers)
admin.site.register(MailMessage)
admin.site.register(Comment)
