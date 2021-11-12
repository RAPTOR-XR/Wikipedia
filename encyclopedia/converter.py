from django import forms
from django.shortcuts import redirect, render
from django.forms.widgets import Textarea 
from markdown2 import Markdown
from . import util
from . import views
import random

converter = Markdown()

class NewSearch (forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs = {'placeholder':'Search'}))

class NewPost (forms.Form):
    title = forms.CharField(label="Title")
    textarea = forms.CharField(label="Content", widget=forms.Textarea())

class Edit_Existing (forms.Form):
    textarea = forms.CharField( widget=forms.Textarea())

def index(request):
    entry = util.list_entries()
    searched_list = []
    if request.method == "POST":
        form = NewSearch(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entry:
                if item in entry:
                    text = util.get_entry(item)
                    converted_lang = converter.convert(text)
                    nec_item = {'text':converted_lang, 'title':item,'form':NewSearch()}
                    return render(request, "encyclopedia/entry.html", nec_item)
            if item.lower() in i.lower():
                searched_list.append(i)
                nec_item = {'searched_list':searched_list,'form':NewSearch()}
            return render(request, "encyclopedia/search.html", nec_item)
        else:
            return render(request, "encyclopedia/index.html",{'form':form})
    else:
         return render(request, "encyclopedia/index.html",{"entries":util.list_entries(), "form": NewSearch()})

def search(request):
    q = request.GET.get('q')
    entry = util.list_entries()
    if q in entry:
        return redirect("entry", title = q)
    return render(request, "encyclopedia/search.html",{"entries": util.search(q), "q":q})

def entry_page(request, title):
    entry = util.list_entries()
    if title in entry:
        text = util.get_entry(title)
        converted_lang = converter.convert(text)
        nec_item = {'text':converted_lang,'title':title,'form':NewSearch()}
        return render(request, "encyclopedia/entry.html", nec_item)
    else:
        return render(request, "encyclopedia/error.html", {"error_message": "The requested page was not found", "form":NewSearch()})

def create_new_page(request):
    if request.method == "POST":
        form = NewPost(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entry = util.list_entries()
            if title in entry:
                nec_item = {"form":NewSearch(), "message": "Page already exist"}
                return render(request, "encyclopedia/error.html", nec_item)
            else:
                util.save_entry(title, textarea)
                text = util.get_entry(title)
                converted_lang = converter.convert(text)
                nec_item = {'form':NewSearch(), 'text':converted_lang,'title':title}
                return render(request, "encyclopedia/entry.html", nec_item)
    else:
        return render(request, "encyclopedia/create.html", {'from': NewSearch(), 'post': NewPost()} )

def edit(request, title):
    if request.method == "GET":
        text = util.get_entry(title)
        nec_item = {'form': NewSearch(), 'edit':Edit_Existing(initial={'textarea':text}), 'title':title}
        return render(request, "encyclopedia/edit.html", nec_item)
    else:
        form = Edit_Existing(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title, textarea)
            text = util.get_entry(title)
            converted_lang = converter.convert(text)
            nec_item = {'form': NewSearch(), 'text':converted_lang, 'title': title}
            return render(request, "encyclopedia/entry.html", nec_item)

def rand_page(request):
    if request.method == "GET":
        entry = util.list_entries()
        rand = random.randint(0, len(entry) - 1)
        random_page = entry[rand]
        text = util.get_entry(random_page)
        converted_lang = converter.convert(text)
        nec_item = {'form':NewSearch(), 'text':converted_lang,'title':random_page}
        return render(request, "encyclopedia/entry.html", nec_item)