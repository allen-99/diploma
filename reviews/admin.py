from django.contrib import admin

from reviews.models.models import Text, Theme, ReviewTextBlock, Company

admin.site.register(Theme)
admin.site.register(Text)
admin.site.register(ReviewTextBlock)
admin.site.register(Company)
