from django.shortcuts import render
from acorta.models import ShortenUrls
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.parse
from django.shortcuts import redirect

# Create your views here.


@csrf_exempt
def show(request, resourceName):
    if request.method == "GET" and resourceName == "":
        lista = showUrls()
        response = "<form method='POST' action=''>" + \
                   "<h1>URL que desea acortar: </h1><br>" + \
                   "<input type='text' name='url' value=''>" + \
                   "<input type='submit' value='Enviar'></form>" + \
                   "<h1><u>Lista de URLs acortadas</u></h1>" + \
                   "<h3>" + lista + "</h3>"

    elif request.method == "GET" and resourceName.isdigit():
        shortUrl = "http://localhost:1234/" + resourceName
        try:
            entry = ShortenUrls.objects.get(shortUrl=shortUrl)
            urlRedirect = entry.longUrl
            return redirect(urlRedirect, status=301)
        except ShortenUrls.DoesNotExist:
            response = "<h1>Recurso no disponible<h1>"
            return HttpResponse(response, status=404)

    elif request.method == "POST":
        qs = (request.body).decode('utf-8')
        qsUnquote = urllib.parse.unquote(qs)
        if len(qsUnquote) > 4:     # Due to "url="
            entry = addUrl(qsUnquote)
            response = "<h1><a href=" + entry.longUrl + ">URL original" + \
                       "<br></a>"
            response += "<a href=" + entry.shortUrl + ">URL acortada" + \
                        "<br></a></h1>"
        else:
            response = "<h1>No hay query string</h1>"
            return HttpResponse(response, status=400)

    else:
        response = "<h1>Metodo no valido</h1>"
        return HttpResponse(response, status=405)

    return HttpResponse(response)


def error(request):
    response = "<h1>La pagina solicitada no se encuentra disponible</h1>"

    return HttpResponse(response, status=400)


def showUrls():
    """Show all the long URLs stored in the database and their related
    short URL"""

    lista = ''
    urls = ShortenUrls.objects.all()
    for url in urls:
        lista = lista + url.longUrl + " => " + url.shortUrl + '<br>'

    return lista


def addUrl(qs):
    """Add the URL to the database (if it was not) and return that entry"""

    url = qs.split('=')[-1]
    if "http" not in url:
        url = "http://" + url
    try:
        entry = ShortenUrls.objects.get(longUrl=url)
    except ShortenUrls.DoesNotExist:
        partialUrl = "http://localhost:1234/"
        dbContent = ShortenUrls.objects.all()
        num = len(dbContent)
        shortUrl = partialUrl + str(num)
        content = ShortenUrls(longUrl=url, shortUrl=shortUrl)
        content.save()

    return ShortenUrls.objects.get(longUrl=url)
