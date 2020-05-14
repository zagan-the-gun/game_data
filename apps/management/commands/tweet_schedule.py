from django.core.management import BaseCommand
from ...models import TweetAccount, TweetSchedule

import datetime
import pytz
import tweepy


class Command(BaseCommand):
    help = 'マスク情報収集'

#    def add_arguments(self, parser):
#        parser.add_argument('-c', '--command', dest='command', help='add or del')
#        parser.add_argument('opt1', help='必須オプション')
#        parser.add_argument('--opt2', help='任意オプション')
#        parser.add_argument('--date', help='何日前')
 
    def handle(self, *args, **options):
#        print(options['command'])
        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG tweet_schedule: '))
#        self.stdout.write(options.__str__())

        START_DATE = datetime.datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Asia/Tokyo'))
        END_DATE = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))

        tweet_schedule = TweetSchedule.objects.filter(tweet_at__range=(START_DATE, END_DATE), tweeted=False, active=True).order_by('-tweet_at')
        for t in tweet_schedule:
            auth = tweepy.OAuthHandler(t.tweet_account.consumer_api_key, t.tweet_account.consumer_api_secret_key)
            auth.set_access_token(t.tweet_account.access_token, t.tweet_account.access_token_secret)
            api = tweepy.API(auth)
            api.update_status(status=t.tweet_content)
            t.tweeted=True
            t.save()

            continue

