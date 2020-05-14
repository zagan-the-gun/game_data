from django.contrib import admin
from .models import Item, TweetAccount, TweetSchedule


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
    list_display = ('pk', 'title', 'amino_price', 'price', 'distributor', 'created_at', 'updated_at', 'active')
#    list_filter = ['release_date']
    search_fields = ['title', 'description_text', 'distributor']

class TweetAccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'active')
    search_fields = ['name', 'consumer_api_key', 'consumer_api_secret_key', 'access_token', 'access_token_secret']


class TweetScheduleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tweet_account', 'tweet_at', 'tweet_content', 'tweeted', 'active')
    search_fields = ['tweet_account', 'tweet_content']


admin.site.register(Item, ItemAdmin)
admin.site.register(TweetAccount, TweetAccountAdmin)
admin.site.register(TweetSchedule, TweetScheduleAdmin)
