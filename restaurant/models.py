from django.db import models

from django.utils import timezone
from django.core.validators import MinValueValidator,MaxValueValidator
from django.conf import settings


#カテゴリモデル(ここに店舗のカテゴリが格納される)
class Category(models.Model):

    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)
    name        = models.CharField(verbose_name="カテゴリ名",max_length=50)

    #TODO:ここに地図のアイコンを表示させるため、アイコン画像を記録する
    icon        = models.ImageField(verbose_name="カテゴリアイコン",upload_to="icon/")

    def __str__(self):
        return self.name


#店舗モデル(ここに店舗の情報が格納される)
class Restaurant(models.Model):

    name        = models.CharField(verbose_name="店名",max_length=50)
    description = models.CharField(verbose_name="店舗紹介文",max_length=2000)

    #後に店舗のカテゴリを指定するフィールドを作る(1対多を意味するmodels.ForeignKey()を使用)
    category    = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.PROTECT)
    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

    prefecture  = models.CharField(verbose_name="都道府県",choices=settings.PREFECTURES,max_length=4)
    city        = models.CharField(verbose_name="市",max_length=50)
    address     = models.CharField(verbose_name="町・番地",max_length=200)

    #店舗の画像を指定するフィールドを作る(ImageField())
    image       = models.ImageField(verbose_name="店舗画像",upload_to="restaurant/restaurant/image")

    #後に店舗のマップ位置(緯度と経度)を記録するフィールドを作る(FloatField()を使用する)
    lat         = models.DecimalField(verbose_name="緯度",max_digits=9, decimal_places=6)
    lon         = models.DecimalField(verbose_name="経度",max_digits=9, decimal_places=6)

    #ここで投稿者のIPアドレスを記録する
    ip          = models.GenericIPAddressField(verbose_name="店舗投稿者のIPアドレス")

    #店舗情報を受け取り、審査をするため、ここに店舗を表示させるかどうかのブーリアンフィールドを追加する。(審査してOKならTrue、だめならFalseのまま)
    #ブーリアンではなく、審査して合格した日時をセットする。
    judge_dt    = models.DateTimeField(verbose_name="審査日時",null=True,blank=True)

    def __str__(self):
        return self.name


#(ここにレビュー情報が格納される)
class Review(models.Model):

    title       = models.CharField(verbose_name="タイトル",max_length=100)
    content     = models.CharField(verbose_name="本文",max_length=1000)
    dt          = models.DateTimeField(verbose_name="投稿日時",default=timezone.now)

    #ここに星の上限と下限を指定する(例えば5つ星なら上限5、下限1など)
    #レビューの星を描画する方法 → https://noauto-nolife.com/post/django-template-integer-for-loop/
    star        = models.IntegerField(verbose_name="星の数",validators=[MinValueValidator(1),MaxValueValidator(5)])
    
    #レビュー対象の店舗に対して1対多野リレーションを組む。models.CASCADEを指定することで、店舗が削除された時、同時にレビューもまとめて削除できる
    restaurant  = models.ForeignKey(Restaurant,verbose_name="店舗",on_delete=models.CASCADE)

    #ここで投稿者のIPアドレスを記録する
    ip          = models.GenericIPAddressField(verbose_name="レビュー投稿者のIPアドレス")



    #TODO:レビューにも画像を投稿できるようにしても良いかも


    def __str__(self):
        return self.title

#ここにお問い合わせ用のモデルを作る(店舗の情報が間違っている、誹謗中傷などの相談を受け付ける)、ここでもIPアドレスを記録する
class Contact(models.Model):
    title       = models.CharField(verbose_name="お問い合わせタイトル",max_length=100)
    content     = models.CharField(verbose_name="お問い合わせ本文", max_length=1000)
    dt          = models.DateTimeField(verbose_name="お問い合わせ日時", default=timezone.now)

    #メールアドレスのフィールド。ここにお問い合わせした内容の返信を送信する。
    email       = models.EmailField(verbose_name="メールアドレス")
    ip          = models.GenericIPAddressField(verbose_name="お問い合わせ投稿者のIPアドレス")

    #管理サイトではお問い合わせのタイトルを表示する
    def __str__(self):
        return self.title
