from django.shortcuts import render, redirect, get_object_or_404
from hesap.models import Hesap
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.http import HttpResponse
import pdfkit

# pip install pdfkit -> pdf yazmamızı kolaylaştıran kütüphane
# https://pypi.org/project/pdfkit/ kütüphane için detaylı kılavuz
# https://wkhtmltopdf.org/  -> incelemekte faydalı olan site (html to pdf)
# indirdiğin MXE versiyonu çıkart ve bin klasörünün yolunu ortam değişkenlerine ekle ( windows için )

def index(request):
    hesaplar = Hesap.objects.all()
    context = {
        'hesaplar': hesaplar
    }
    return render(request, 'index.html', context=context)


@require_http_methods(['POST'])
def kayit(request):
    if request.method == 'POST':
        isim = request.POST.get('isim')
        email = request.POST.get('email')
        telefon = request.POST.get('telefon')
        unvan = request.POST.get('unvan')
        ozet = request.POST.get('ozet')
        resim = request.FILES.get('resim')
        yeni_kayit = Hesap(isim=isim, email=email, telefon=telefon, unvan=unvan, ozet=ozet, resim=resim)
        yeni_kayit.save()
        return redirect('index')


def goster(request, pk):
    hesap = get_object_or_404(Hesap, pk=pk)
    context = {
        'hesap': hesap
    }
    return render(request, 'cv.html', context=context)


def pdf_generate(request, pk):
    hesap = get_object_or_404(Hesap, pk=pk)
    context = {
        'hesap': hesap
    }
    template = loader.get_template('cv.html') # template'i değişkene atadık
    html = template.render(context) # templateimiz data aldığından içeri data olarak context'i yolladık
    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8'
    } # ayarları belirledik.
    css = ['static/style.css'] # ilgili css dosyalarımızın yolunu veriyoruz
    pdf = pdfkit.from_string(html, False, options,css=css) # html değişkenini pdf olarak yazacak, ayarları options olacak, False -> oluşturduğum bu pdf'i şimdilik bellekte tutmak istiyorum anlamına gelir
    response = HttpResponse(pdf, content_type='application/pdf') # response instance oluşturduk
    response['Content-Disposition'] = 'attachment; filename=gelencv.pdf' # header'da response dönerken yanında bir de file dönecek dedik
    return response
