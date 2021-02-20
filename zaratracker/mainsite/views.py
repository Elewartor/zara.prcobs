from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Reference, Region
from wpscripts.parser import ReferenceParser

# Create your views here.

def home_view(request):
    context = {}
    references = Reference.objects.all()
    context['references'] = references

    regions = Region.objects.all()
    context['regions'] = regions

    return render(request, 'home.html', context)

def create_reference_view(request):
    user = request.user

    ref_name = request.GET.get('name')
    ref = request.GET.get('ref')
    reg = Region.objects.get(pk=request.GET.get('reg'))
    reference = Reference()
    slug = str(reference.uuid) + ref + reg.shortcut
    reference.name = ref_name
    reference.reference = ref
    reference.region = reg
    reference.author = user
    reference.slug = slug
    reference.save()

    return redirect('home')

def reference_view(request, slug):
    context = {}
    regions = Region.objects.all()
    context['regions'] = regions

    references = Reference.objects.all()
    context['references'] = references

    reference_obj = Reference.objects.get(slug=slug)
    context['reference_obj'] = reference_obj

    host = 'https://www.zara.com/'
    region = reference_obj.region.shortcut
    language = '/en/'
    category = 'category/' + reference_obj.reference + '/products?ajax=true'
    url = host + region + language + category

    context['products'] = ReferenceParser(url, reference_obj).get_reference_data_set()

    return render(request, 'home.html', context)