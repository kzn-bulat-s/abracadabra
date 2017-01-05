from django.shortcuts import render, get_or_404

def test(request, *args, **kwargs):
    return HttpResponse('OK')

def page(request, page_no):
    pass

def popular(request, page_no):
    pass


