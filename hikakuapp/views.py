from django.http import request
from django.shortcuts import render
from django.views import generic
# Create your views here.
from . import scraping 

import time

#拒否したいURLのリスト
DENY_URL_LIST   = [ "https://qiita.com/",]

DENY_TITLE_LIST = [ "Qiita",]


#Viewを継承してGET文、POST文の関数を作る
class SearchView(generic.View):

    def get(self, request, *args, **kwargs):

        if "search_word" in request.GET:
            if request.GET["search_word"] != "":

                start_time  = time.time()

                word                    = request.GET["search_word"]

                #検索結果を表示
                link_list,title_list    = scraping.search_google(word)

                #テンプレートで扱いやすいように整形
                data        = []
                link_list_length    = len(link_list)

                #ここで特定URL、タイトルのサイトを除外する。
                for i in range(link_list_length):
                    allow_flag = True

                    for deny in DENY_URL_LIST:
                        if deny in link_list[i]:
                            allow_flag   = False
                            break

                    if allow_flag:
                        for deny in DENY_TITLE_LIST:
                            if deny in title_list[i]:
                                allow_flag   = False
                                break

                    if allow_flag:
                        data.append( { "url":link_list[i] , "title":title_list[i] } )



                end_time    = int(time.time() - start_time)

                context = { "search_word"   : word,
                            "data"          : data,
                            "time"          : end_time
                            }

                return render(request,"hikakuapp/result.html",context)

        return render(request,"hikakuapp/base.html")

    def post(self, request, *args, **kwargs):

        pass

