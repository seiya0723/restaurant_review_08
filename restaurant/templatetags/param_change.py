from django import template

register = template.Library()

#テンプレートタグを作るため、.simple_tag()をデコレータとして使う。
#単に関数を指定するだけではテンプレートタグとして使えないので、デコレータを指定する。継承みたいなもの。
@register.simple_tag()
def url_replace(request, key, value):
    #引数として、リクエストオブジェクト、書き換えたいキー、書き換えたい値
    copied           = request.GET.copy()
    copied[key]      = value
    #copied["page"]   = 2 #指定されたキーに指定された値で書き換えられる。

    #最終的に出力するのが、クエリストリング( search=test&page=2 )を返す。
    return copied.urlencode()