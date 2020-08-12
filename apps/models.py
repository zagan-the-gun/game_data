from django.db import models
from enum import Enum
from taggit.managers import TaggableManager


class Site(models.Model):
    class Meta:
        verbose_name_plural='サイト'

    name = models.CharField(
             verbose_name='サイト名',
             max_length=200,
             blank=False,
             null=False,
           )
    site_url=models.URLField(
                 verbose_name='サイトURL',
                 max_length=512,
                 blank=True,
                 null=True,
             )
    image = models.ImageField(
              verbose_name='スクエアロゴ',
              upload_to='images/',
            )
    favicon_32x32 = models.ImageField(
              verbose_name='ファビコン32x32',
              upload_to='images/',
            )
    favicon_16x16 = models.ImageField(
              verbose_name='ファビコン16x16',
              upload_to='images/',
            )
    created_at=models.DateTimeField(
                   verbose_name='作成日時',
                   auto_now_add=True,
               )
    updated_at=models.DateTimeField(
                   verbose_name='更新日時',
                   auto_now=True,
               )
    def __str__(self):
       return str(self.name)


class LargeCategory(models.Model):
    class Meta:
        verbose_name_plural='ラージカテゴリ'

    name = models.CharField(
             verbose_name='ラージカテゴリ名',
             max_length=200,
             blank=False,
             null=False,
           )
    label = models.CharField(
              verbose_name='ラージカテゴリラベル',
              max_length=200,
              blank=False,
              null=False,
            )
    image = models.ImageField(
              verbose_name='画像',
              upload_to='images/',
            )
    is_view = models.BooleanField(
                verbose_name='表示フラグ',
                default=True,
              )

    def __str__(self):
       return str(self.label)

class MediumCategory(models.Model):
    class Meta:
        verbose_name_plural='ミディアムカテゴリ'

    # ラージカテゴリ
    large_category = models.ForeignKey(
            'LargeCategory', 
            verbose_name='ラージカテゴリ',
            on_delete=models.DO_NOTHING
          )
    name = models.CharField(
             verbose_name='ミディアムカテゴリ名',
             max_length=200,
             blank=False,
             null=False,
           )
    label = models.CharField(
              verbose_name='ミディアムカテゴリラベル',
              max_length=200,
              blank=False,
              null=False,
            )
    is_view = models.BooleanField(
                verbose_name='表示フラグ',
                default=True,
              )

    def __str__(self):
       return str(self.label)

class SmallCategory(models.Model):
    class Meta:
        verbose_name_plural='スモールカテゴリ'

    # ミディアムカテゴリ
    medium_category = models.ForeignKey(
            'MediumCategory', 
            verbose_name='ミディアムカテゴリ',
            on_delete=models.DO_NOTHING
          )
    name = models.CharField(
             verbose_name='スモールカテゴリ名',
             max_length=200,
             blank=False,
             null=False,
           )
    label = models.CharField(
              verbose_name='スモールカテゴリラベル',
              max_length=200,
              blank=False,
              null=False,
            )
    hashtag = models.CharField(
              verbose_name='ハッシュタグ',
              max_length=20,
              blank=True,
              null=True,
            )
    tags = TaggableManager(
             blank=True
           )
    notation_per_unit = models.CharField(
                          verbose_name='単位あたりの表記',
                          blank=True,
                          null=True,
                          max_length=10,
                        )
    image = models.ImageField(
              verbose_name='画像',
              upload_to='images/',
              blank=True,
              null=True,
            )
    is_view = models.BooleanField(
                verbose_name='表示フラグ',
                default=True,
              )

    def __str__(self):
       return str(self.label)

class ItemType(models.IntegerChoices):
    XXX_GAME = 1, 'エロゲ'
    XXX_BOOK = 2, 'エロ本'
    XXX_MOVIE = 3, 'エロ動画'
    KAISEN_KANI = 10, 'カニ'
    KAISEN_EBI = 11, 'エビ'
    KAISEN_KAKI = 12, 'カキ'

class Distributor(models.IntegerChoices):
    all     = 1, '全て'
    rakuten = 2, '楽天'
    yahoo   = 3, 'ヤフー '
    amazon  = 4, 'アマゾン'

class SearchWord(models.Model):
    class Meta:
        verbose_name_plural='検索ワード'

    word = models.CharField(
             verbose_name='検索ワード',
             max_length=200,
             blank=False,
             null=False,
           )
    #タグ
    tags = TaggableManager(
             blank=True
           )
    notation_unit = models.CharField(
                      verbose_name='表記単位',
                      blank=True,
                      null=True,
                      max_length=10,
                    )
    exclusion_word = models.CharField(
                       verbose_name='除外ワード',
                       max_length=20,
                       blank=True,
                       null=True,
                     )
    distributor = models.PositiveIntegerField(
                    verbose_name='販売元',
                    choices=Distributor.choices,
                  )

    def __int__(self):
       return str(self.tag)

class Item(models.Model):
    class Meta:
        verbose_name_plural='アイテム'

    class ItemType(models.IntegerChoices):
        XXX_GAME = 1, 'エロゲ'
        XXX_BOOK = 2, 'エロ本'
        XXX_MOVIE = 3, 'エロ動画'
        KAISEN_KANI = 10, 'カニ'
        KAISEN_EBI = 11, 'エビ'
        KAISEN_KAKI = 12, 'カキ'

    title=models.CharField(
              verbose_name='商品タイトル',
              max_length=200,
              blank=True,
              null=True,
          )
    #画像URL
    image_url=models.URLField(
                  verbose_name='画像URL',
                  max_length=512,
                  blank=True,
                  null=True,
              )
    #サイトURL
    site_url=models.URLField(
                 verbose_name='サイトURL',
                 max_length=512,
                 blank=True,
                 null=True,
             )
    #説明文
    description_text=models.TextField(
                    verbose_name='説明文',
                    max_length=2000,
                    blank=True,
                    null=True,
                )
    #単価
    amino_price=models.PositiveIntegerField(
                   verbose_name='単価',
                   default=0,
               )
    #売価
    price=models.PositiveIntegerField(
              verbose_name='売価',
              default=0,
          )
    # 元値
    original_price=models.PositiveIntegerField(
              verbose_name='元価',
              default=0,
          )
    #販売元
    distributor=models.CharField(
                    verbose_name='販売元',
                    blank=True,
                    null=True,
                    max_length=10,
                )
    #アイテムタイプ
#    item_type=models.PositiveIntegerField(
#                verbose_name='アイテムタイプ',
#                choices=ItemType.choices,
#              )
    # サイズ
    size=models.PositiveIntegerField(
             verbose_name='サイズ',
             default=0,
         )
    # 割引率
    discount_rate=models.PositiveIntegerField(
                      verbose_name='割引率  ',
                      default=0,
                  )
    # 割引終了日時
    period_at=models.DateTimeField(
                   verbose_name='割引終了日時',
                   blank=True,
                   null=True,
              )
    # 送料
    shipping_price=models.PositiveIntegerField(
                      verbose_name='送料',
                      blank=True,
                      null=True,
                  )
    # 売り切れ
    sold_out=models.BooleanField(
               verbose_name='売り切れ',
               default=False,
           )
    tags = TaggableManager(
             blank=True
           )
    # 作成日時
    created_at=models.DateTimeField(
                   verbose_name='作成日時',
                   auto_now_add=True,
               )
    # 更新日時
    updated_at=models.DateTimeField(
                   verbose_name='更新日時',
                   auto_now=True,
               )
    # 死活
    active=models.BooleanField(
               verbose_name='Active',
               default=True,
           )

    def __str__(self):
       return self.title


class TweetAccount(models.Model):
    class Meta:
        verbose_name_plural='ツイートアカウント'

    # 名前
    name=models.CharField(
             verbose_name='名前',
             max_length=200,
             blank=False,
             null=False,
         )
    # コンシューマAPIキー
    consumer_api_key=models.CharField(
                         verbose_name='コンシューマAPIキー',
                         max_length=200,
                         blank=False,
                         null=False,
                     )
    # コンシューマAPIシークレットキー
    consumer_api_secret_key=models.CharField(
                                verbose_name='コンシューマAPIシークレットキー',
                                max_length=200,
                                blank=False,
                                null=False,
                            )
    # アクセストークン
    access_token=models.CharField(
                     verbose_name='アクセストークン',
                     max_length=200,
                     blank=False,
                     null=False,
                 )
    # アクセストークンシークレット
    access_token_secret=models.CharField(
                            verbose_name='アクセストークンシークレット',
                            max_length=200,
                            blank=False,
                            null=False,
                        )
    # 作成日時
    created_at=models.DateTimeField(
                   verbose_name='作成日時',
                   auto_now_add=True,
               )

    # 更新日時
    updated_at=models.DateTimeField(
                   verbose_name='更新日時',
                   auto_now=True,
               )
    # 死活
    active=models.BooleanField(
               verbose_name='Active',
               default=True,
           )

    def __str__(self):
       return self.name


class TweetSchedule(models.Model):
    class Meta:
        verbose_name_plural='ツイートスケジュール'

    # ツイートアカウント
    tweet_account=models.ForeignKey(
                      'TweetAccount', 
                      on_delete=models.DO_NOTHING
                  )
    # ツイート内容
    tweet_content=models.TextField(
                      verbose_name='ツイート内容',
                      max_length=2000,
                      blank=False,
                      null=False,
                  )
    # ツイート日時
    tweet_at=models.DateTimeField(
                 verbose_name='ツイート日時',
             )
    # ツイート済
    tweeted=models.BooleanField(
                verbose_name='ツイート済',
                default=False,
            )
    # 作成日時
    created_at=models.DateTimeField(
                   verbose_name='作成日時',
                   auto_now_add=True,
               )
    # 更新日時
    updated_at=models.DateTimeField(
                   verbose_name='更新日時',
                   auto_now=True,
               )
    # 死活
    active=models.BooleanField(
               verbose_name='Active',
               default=True,
           )

    def __str__(self):
       return str(self.tweet_at)

