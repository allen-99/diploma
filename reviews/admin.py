from django.contrib import admin
from reviews.models.models import Text, Theme, TextBlock, Company

admin.site.register(Theme)
admin.site.register(Text)
admin.site.register(TextBlock)
admin.site.register(Company)
