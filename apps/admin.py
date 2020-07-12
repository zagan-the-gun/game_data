from django.contrib import admin
from .models import Item, TweetAccount, TweetSchedule, LargeCategory, MediumCategory, SmallCategory, SearchWord, Site


class ItemAdmin(admin.ModelAdmin):
#    fieldsets = [
#        (None,               {'fields': ['uid']}),
#        (None,               {'fields': ['aid']}),
#        (None,               {'fields': ['name']}),
#        (None,               {'fields': ['ad_type']}),
#        (None,               {'fields': ['platform']}),
#        (None,               {'fields': ['strategy_type']}),
#        (None,               {'fields': ['genre']}),
#        (None,               {'fields': ['officer']}),
#        ('Date information', {'fields': ['release_date'], 'classes': ['collapse']}),
#    ]
#    inlines = [PlatformInline]
    list_display = ('pk', 'title', 'amino_price', 'price', 'distributor', 'tag_list', 'created_at', 'updated_at', 'active')
#    list_filter = ['release_date']
    search_fields = ['title', 'description_text', 'distributor', 'tags__name', 'site_url']

    actions = ['deactive', 'active']
    def deactive(self, request, queryset):
        queryset.update(active=False)
    deactive.short_description = 'ActiveをFalseに'

    def active(self, request, queryset):
        queryset.update(active=True)
    active.short_description = 'ActiveをTrueに'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

class TweetAccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'active')
    search_fields = ['name', 'consumer_api_key', 'consumer_api_secret_key', 'access_token', 'access_token_secret']

class TweetScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tweet_account', 'tweet_at', 'tweet_content', 'tweeted', 'active')
    search_fields = ['tweet_account', 'tweet_content']

class LargeCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'label', 'is_view')
    search_fields = ['name', 'label']

class MediumCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'label', 'is_view')
    search_fields = ['name', 'label']

class SmallCategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'medium_category', 'name', 'label', 'tag_list', 'notation_per_unit', 'is_view']
    search_fields = ['name', 'label', 'tags__name', 'notation_per_unit']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

#class TagAdmin(admin.ModelAdmin):
#    list_display = ('pk', 'name')
#    search_fields = ['name']

class SearchWordAdmin(admin.ModelAdmin):
    list_display = ('pk', 'word', 'tag_list', 'notation_unit')
    search_fields = ['word', 'tags__name', 'notation_unit']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

class SiteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'image', 'created_at', 'updated_at')
    search_fields = ['name', 'image']


admin.site.register(Item, ItemAdmin)
admin.site.register(TweetAccount, TweetAccountAdmin)
admin.site.register(TweetSchedule, TweetScheduleAdmin)
admin.site.register(LargeCategory, LargeCategoryAdmin)
admin.site.register(MediumCategory, MediumCategoryAdmin)
admin.site.register(SmallCategory, SmallCategoryAdmin)
#admin.site.register(Tag, TagAdmin)
admin.site.register(SearchWord, SearchWordAdmin)
admin.site.register(Site, SiteAdmin)

