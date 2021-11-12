from django.shortcuts import render

from . import util
from . import converter


def index(request):
    return converter.index(request)

def new_entry(request, title):
    return converter.entry_page(request, title)

def search(request):
    return converter.search(request)

def create_new(request):
    return converter.create_new_page(request)

def edit_page(request, title):
    return converter.edit(request, title)

def random(request):
    return converter.rand_page(request)