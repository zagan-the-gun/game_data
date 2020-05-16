from django.db import models
from enum import Enum


class Item(models.Model):
    class Meta:
        verbose_name_plural="アイテム"

    class ItemType(models.IntegerChoices):
        XXX_GAME = 1, 'エロゲ'
        XXX_BOOK = 2, 'エロ本'
        XXX_MOVIE = 3, 'エロ動画'

    #商品タイトル
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
    item_type=models.PositiveIntegerField(
                  verbose_name='アイテムタイプ',
                  choices=ItemType.choices,
              )
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
        verbose_name_plural="ツイートアカウント"

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
        verbose_name_plural="ツイートスケジュール"

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

