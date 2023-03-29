from django.http import JsonResponse


def custom404(request, exception=None):
    response = {
        'code': 404,
        'message': 'The resource was not found',
        'status': False,
        'data': {}
    }
    return JsonResponse(response)

from django.http import HttpResponse
# from .celery import my_first_task
from apps.contents.models import TranslateData
from googletrans import Translator
from django.db.models import F

# def index(request):
#     print("cron job started")
#     my_first_task.delay()
#     # my_first_task(duration=10)
#
#     print("cron job ended")
#     return HttpResponse('response done')

# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def start_jobs():
#     scheduler = BackgroundScheduler()
#
#     # Set cron to runs every 20 min.
#     cron_job = {'month': '*', 'day': '*', 'hour': '*', 'minute': '*/60'}
#
#     # Add our task to scheduler.
#     scheduler.add_job(index(), 'cron', **cron_job)
#     # And finally start.
#     scheduler.start()

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
import googletrans


class Redis(APIView):
    def get(self, request, *args, **kwargs):
        print("inside gett")
        payload=[]
        db=None


        # print(googletrans.LANGUAGES)

        if cache.get('data'):
            payload=cache.get('data')
            print("redis",payload)
            db='redis'
            result=translate(payload)
            if result:
                null = TranslateData.objects.filter(translated__isnull=True).values_list('id', 'data')
                print(null)
            cache.set('data', null)
            payload = cache.get('data')
            print("redisssss",payload)



        else:
            objs=TranslateData.objects.filter(translated__isnull=True).values_list('id', 'data')
            # print(objs)
            for obj in objs:
                print(obj)
                payload.append(obj)
            db='sqlite'
            cache.set('data',payload)

        return Response({'status':200,'db':db,'data':payload})

    def post(self, request, *args, **kwargs):
        print("inside post")
        translate=TranslateData()
        data=self.request.POST['data']
        print(data)
        #-print(TranslateData.objects.filter(data=data))
        db_data=TranslateData.objects.filter(data=data).values_list("data")
        print(db_data)

        # print(db_data.exists())
        if db_data.exists() is False:
            # print("data not present")
            db_data="new data added into db"
            translate.data=data
            translate.save()
            # cache.set('data', data)
            null=TranslateData.objects.filter(translated__isnull=True).values_list('id','data')
            print("null",null)
            cache.set('data',null)


        return Response({'status':200,'data':db_data})


from apps.contents.models import TranslatedUser
from apps.cook.models import Cook
from apps.courier.models import Courier
from apps.customer.models import Customer
from rest_framework.permissions import IsAuthenticated

class Translated(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        try:
            print("get")
            cook = Cook.objects.filter(user_id=self.request.user.user_id)
            courier = Courier.objects.filter(user_id=self.request.user.user_id)
            customer = Customer.objects.filter(user_id=self.request.user.user_id)
            if cook:
                cook_pk=list(cook.values_list("pk", flat=True))[0]
                queryset = list(TranslatedUser.objects.filter(cook_pk=cook_pk).values('cook_pk', 'cook_id', 'language'))

            if courier:
                courier_pk = list(courier.values_list("pk", flat=True))[0]
                queryset = list(TranslatedUser.objects.filter(courier_pk=courier_pk).values('courier_pk', 'courier_id', 'language'))
            if customer:
                customer_pk = list(customer.values_list("pk", flat=True))[0]
                queryset = list(TranslatedUser.objects.filter(customer_pk=customer_pk).values('customer_pk', 'customer_id', 'language'))



            return Response(queryset)
        except:
            return Response({"data":None})

    def post(self, request, *args, **kwargs):
        try:
            lang = self.request.POST['data']
            cook = Cook.objects.filter(user_id=self.request.user.user_id)
            courier=Courier.objects.filter(user_id=self.request.user.user_id)
            customer=Customer.objects.filter(user_id=self.request.user.user_id)
            translateuser=TranslatedUser()



            if cook:
                cook_pk = list(cook.values_list("pk", flat=True))[0]
                cook_id = list(cook.values_list("cook_id", flat=True))[0]
                translateuser.cook_pk = cook_pk

                if TranslatedUser.objects.filter(cook_pk=cook_pk):
                    TranslatedUser.objects.filter(cook_pk=cook_pk).update(cook_id=cook_id,language=lang)
                else:
                    translateuser.save()
            if courier:
                courier_pk = list(courier.values_list("pk", flat=True))[0]
                courier_id = list(courier.values_list("courier_id", flat=True))[0]
                translateuser.courier_pk = courier_pk

                if TranslatedUser.objects.filter(courier_pk=courier_pk):
                    TranslatedUser.objects.filter(courier_pk=courier_pk).update(courier_id=courier_id,language=lang)

                else:
                    translateuser.save()
            if customer:
                customer_pk = list(customer.values_list("pk", flat=True))[0]
                customer_id = list(customer.values_list("customer_id", flat=True))[0]
                translateuser.customer_pk = customer_pk

                if TranslatedUser.objects.filter(customer_pk=customer_pk):
                    TranslatedUser.objects.filter(customer_pk=customer_pk).update(customer_id=customer_id, language=lang)
                else:
                    translateuser.save()
            # lang=self.request.GET.get('data', None)
            names={'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-cn': 'chinese (simplified)', 'zh-tw': 'chinese (traditional)', 'co': 'corsican', 'hr': 'croatian', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian','is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish (kurmanji)', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar (burmese)', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots_gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa','yo': 'yoruba', 'zu': 'zulu'}
            for key, value in names.items():
                if lang == key:
                    lang_name=value
            data=TranslateData.objects.values("data",lang_name)


            return Response({"language":lang_name,'data':data})
        except:
            return Response({"language":"not available",'data':None})


def translate(payload):
    Translator_data=TranslateData()
    print(payload)
    # data = TranslateData.objects.filter(translated__isnull=True)
    for i in payload.values():
        # print(i)
        langs={'af': 'afrikaans', 'sq': 'albanian', 'am': 'amharic', 'ar': 'arabic', 'hy': 'armenian', 'az': 'azerbaijani', 'eu': 'basque', 'be': 'belarusian', 'bn': 'bengali', 'bs': 'bosnian', 'bg': 'bulgarian', 'ca': 'catalan', 'ceb': 'cebuano', 'ny': 'chichewa', 'zh-tw': 'chinese_traditional', 'co': 'corsican', 'cs': 'czech', 'da': 'danish', 'nl': 'dutch', 'en': 'english', 'eo': 'esperanto', 'et': 'estonian', 'tl': 'filipino', 'fi': 'finnish', 'fr': 'french', 'fy': 'frisian', 'gl': 'galician', 'ka': 'georgian', 'de': 'german', 'el': 'greek', 'gu': 'gujarati', 'ht': 'haitian_creole', 'ha': 'hausa', 'haw': 'hawaiian', 'iw': 'hebrew', 'he': 'hebrew', 'hi': 'hindi', 'hmn': 'hmong', 'hu': 'hungarian','is': 'icelandic', 'ig': 'igbo', 'id': 'indonesian', 'ga': 'irish', 'it': 'italian', 'ja': 'japanese', 'jw': 'javanese', 'kn': 'kannada', 'kk': 'kazakh', 'km': 'khmer', 'ko': 'korean', 'ku': 'kurdish_kurmanji', 'ky': 'kyrgyz', 'lo': 'lao', 'la': 'latin', 'lv': 'latvian', 'lt': 'lithuanian', 'lb': 'luxembourgish', 'mk': 'macedonian', 'mg': 'malagasy', 'ms': 'malay', 'ml': 'malayalam', 'mt': 'maltese', 'mi': 'maori', 'mr': 'marathi', 'mn': 'mongolian', 'my': 'myanmar_burmese', 'ne': 'nepali', 'no': 'norwegian', 'or': 'odia', 'ps': 'pashto', 'fa': 'persian', 'pl': 'polish', 'pt': 'portuguese', 'pa': 'punjabi', 'ro': 'romanian', 'ru': 'russian', 'sm': 'samoan', 'gd': 'scots_gaelic', 'sr': 'serbian', 'st': 'sesotho', 'sn': 'shona', 'sd': 'sindhi', 'si': 'sinhala', 'sk': 'slovak', 'sl': 'slovenian', 'so': 'somali', 'es': 'spanish', 'su': 'sundanese', 'sw': 'swahili', 'sv': 'swedish', 'tg': 'tajik', 'ta': 'tamil', 'te': 'telugu', 'th': 'thai', 'tr': 'turkish', 'uk': 'ukrainian', 'ur': 'urdu', 'ug': 'uyghur', 'uz': 'uzbek', 'vi': 'vietnamese', 'cy': 'welsh', 'xh': 'xhosa', 'yo': 'yoruba', 'zu': 'zulu','en':'translated'}
        try:
            for key, value in langs.items():
                print(key)
                translator = Translator()
                print(translator)
                print(i['data'])
                translation = translator.translate(i['data'],src='en',dest=key)
                print(translation.text)
                if translation:
                    print(translation)
                    TranslateData.objects.filter(id=i['id']).update(**{value: translation.text})
                else:
                    pass
        except StopIteration:
            pass

            # print(TranslateData.objects.get(id=i['id']))
    # sleep(duration)
    return True