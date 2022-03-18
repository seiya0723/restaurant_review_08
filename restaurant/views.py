from django.shortcuts import render,redirect
from django.views import View

from .models import Restaurant,Review,Category
from .forms import RestaurantForm,ReviewForm,CategoryForm,ContactForm


#スペース区切りの検索をする。
#https://noauto-nolife.com/post/django-or-and-search/
from django.db.models import Q

#Djangoでページネーションを実装させる。
#https://noauto-nolife.com/post/django-paginator/
from django.core.paginator import Paginator

class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        #ここで検索処理を実行する。ページネーション
        #request.GETの中にsearchがあるかチェック。クエリパラメータにsearchがあるかチェック。
        if "search" in request.GET:
            #ここで検索の処理をする
            print(request.GET["search"])
            #=を使用すると完全一致の検索
            #context["restaurants"]  = Restaurant.objects.filter(name=request.GET["search"])

            #指定した文字を含む場合の検索(スペースも文字列の一部として考えて検索される。スペース区切りにならない)
            #context["restaurants"]  = Restaurant.objects.filter(name__icontains=request.GET["search"])

            #スペース区切りで検索を実装
            #ページ移動(ページネーション)と検索を両立させる

            #(1)キーワードが空欄もしくはスペースのみの場合、ページにリダイレクト
            if request.GET["search"] == "" or request.GET["search"].isspace():
                return redirect("restaurant:index")


            #(2)キーワードをリスト化させる(複数指定の場合に対応させるため)
            search      = request.GET["search"].replace("　"," ")
            search_list = search.split(" ")

            #(3)クエリを作る
            query       = Q()
            for word in search_list:

                #空欄の場合は次のループへ
                if word == "":
                    continue

                #TIPS:AND検索の場合は&を、OR検索の場合は|を使用する。
                query &= Q(name__contains=word)

            restaurants  = Restaurant.objects.filter(query).order_by("-dt")
        else:
            #飲食店一覧を表示させる(新しい順に)
            restaurants  = Restaurant.objects.order_by("-dt")

        #Paginatorにページ区切りにしたいモデルオブジェクトと1ページに表示させる個数を指定
        paginator   = Paginator(restaurants,2)

        if "page" in request.GET:
            #?page=2であればrequest.GET["page"]は2になる。.get_page(2)となり、2ページ目を表示する。
            #?page=hogeなどの文字列、?page=3などの存在しないページ番号を指定された場合、1ページ目,最終ページを表示する
            context["restaurants"] = paginator.get_page(request.GET["page"])
        else:
            #1ページ目がでる
            context["restaurants"] = paginator.get_page(1)



        return render(request,"restaurant/index.html",context)

index   = IndexView.as_view()

class SingleView(View):

    def get(self, request, pk, *args, **kwargs):

        #飲食店に投稿されたレビューを表示
        context                 = {}
        #単一のモデルオブジェクトを手に入れる。これはテンプレートでforループを行う必要はない。
        context["restaurant"]   = Restaurant.objects.filter(id=pk).first()

        #context["reviews"]      = Review.objects.filter(restaurant=pk).order_by("-dt")
        reviews                 = Review.objects.filter(restaurant=pk).order_by("-dt")

        #TODO:ここでレビューのページネーションを実現させる

        #Paginatorにページ区切りにしたいモデルオブジェクトと1ページに表示させる個数を指定
        paginator   = Paginator(reviews,2)

        if "page" in request.GET:
            #?page=2であればrequest.GET["page"]は2になる。.get_page(2)となり、2ページ目を表示する。
            #?page=hogeなどの文字列、?page=3などの存在しないページ番号を指定された場合、1ページ目,最終ページを表示する
            context["reviews"] = paginator.get_page(request.GET["page"])
        else:
            #1ページ目がでる
            context["reviews"] = paginator.get_page(1)


        return render(request,"restaurant/single.html",context)

    def post(self, request, pk, *args, **kwargs):

        #飲食店にレビューを投稿

        #リクエストオブジェクトに対象の店舗のidをセットする必要がある
        #だが、リクエストオブジェクトは書き換え不可能なデータである。
        #そのため、コピーを作って対象の店舗idをセットし、バリデーションする。

        copied                  = request.POST.copy()
        copied["restaurant"]    = pk

        #デプロイした後でも、利用者のIPアドレスを取得できる
        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_list:
            ip = ip_list.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        #ユーザーのIPアドレスをセットする。
        copied["ip"]            = ip

        print(copied)
        form    = ReviewForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        #リダイレクトする時は対象のidを指定する。
        return redirect("restaurant:single", pk )

single  = SingleView.as_view()

class RestaurantCreateView(View):
    def get(self, request, *args, **kwargs):
        #店舗登録フォームを表示させる
        context = {}
        #選択肢のデータを手に入れる(都道府県文字列のリストを作る。リストの内包表記)
        context["prefectures"]  = [ p[0] for p in Restaurant.prefecture.field.choices ]
        context["categories"]   = Category.objects.order_by("-dt")

        #リストの内包表記は下記と等価
        """
        p_list  = []
        for p in Restaurant.prefecture.field.choices:
            p_list.append(p[0])
        """

        return render(request,"restaurant/restaurant_create.html",context)

    def post(self, request, *args, **kwargs):
        #店舗情報を受け取る

        copied  = request.POST.copy()
        #デプロイした後でも、利用者のIPアドレスを取得できる
        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_list:
            ip = ip_list.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        #店舗情報投稿者のIPアドレスをセットする。
        copied["ip"]            = ip

        #画像データもバリデーションする必要がある。バリデーションの後画像も保存する
        form = RestaurantForm(copied, request.FILES)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")

        return redirect("restaurant:index")

restaurant_create   = RestaurantCreateView.as_view()


class ContactView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_list:
            ip = ip_list.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        context["ip"]   = ip
        #お問い合わせフォームを表示させる

        return render(request,"restaurant/contact.html",context)

    def post(self, request, *args, **kwargs):
        #TODO:お問い合わせを受け付け、バリデーションしてDBに保存する
        ip_list = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_list:
            ip = ip_list.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        #IPアドレスもセットする
        copied  = request.POST.copy()
        copied["ip"]  = ip

        form = ContactForm(copied)

        if form.is_valid():
            print("バリデーションOK")
            form.save()
        else:
            print("バリデーションNG")
            print(form.errors)


        return redirect("restaurant:contact")


contact = ContactView.as_view()
