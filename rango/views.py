#from django.shortcuts import render
#from django.http import HttpResponse

# Create your views here.
#def index(request):
    #return HttpResponse("Rango says hey there partner! <a href='/rango/about/'>About</a>")

#def about(request):
    #return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>")

from django.shortcuts import render
from rango.models import Category, Page  

# Create your views here.
from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5] 
    page_list = Page.objects.order_by('-views')[:5]  

    context_dict = {
        'categories': category_list,
        'pages': page_list,
        'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!",  
    }

    return render(request, 'rango/index.html', context_dict)

from django.shortcuts import render, get_object_or_404
from rango.models import Category, Page

def show_category(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
    except Category.DoesNotExist:
        category = None
        pages = None

    context_dict = {'category': category, 'pages': pages}

    if category is None:
        context_dict['error_message'] = "The specified category does not exist."

    return render(request, 'rango/category.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')


