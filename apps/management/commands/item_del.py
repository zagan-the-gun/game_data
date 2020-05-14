from django.core.management import BaseCommand
from ...models import Item

import requests
import datetime
import pytz


class Command(BaseCommand):
    help = 'マスク情報収集'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--day', dest='day', type=int, help='"--day 30" delete more than 30 days ago')
#        parser.add_argument('opt1', help='必須オプション')
#        parser.add_argument('--opt2', help='任意オプション')
#        parser.add_argument('--date', help='何日前')
 
    def handle(self, *args, **options):
        #END_DATE=datetime.date.today()-datetime.timedelta(days=options['day'])
        tstr = '2020-01-01 00:00:00'
        START_DATE = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S').replace(tzinfo=pytz.timezone('Asia/Tokyo'))

        END_DATE=datetime.datetime.now(pytz.timezone('Asia/Tokyo'))-datetime.timedelta(days=options['day'])
        print(str(END_DATE))

        self.stdout.write(self.style.SUCCESS('DEBUG DEBUG DEBUG item_del: '))
#        self.stdout.write(options.__str__())

        # 削除
        item = Item.objects.filter(updated_at__range=(START_DATE, END_DATE)).delete()
        print(item)

