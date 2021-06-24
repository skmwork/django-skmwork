from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def main_page(request):
    return HttpResponse('Инфестиции в фонды одно из самых надежных вложений на фондовый рынок\r\n Мы поможем сделать индексный портфель сбалансированным по странам и сферам')