from rango.models import Category, Page  
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import render, redirect
from django.urls import reverse 
from rango.models import Category, Page
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from _datetime import datetime
def index(request):
    category_list = Category.objects.order_by('-likes')[:5] 
    page_list = Page.objects.order_by('-views')[:5]  

    if 'visits' not in request.session:
        request.session['visits'] = 1
        request.session['last_visit'] = str(datetime.now())

    visits = request.session.get('visits', 1)  
    last_visit = request.session.get('last_visit', str(datetime.now()))

    try:
        last_visit_time = datetime.strptime(last_visit, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        last_visit_time = datetime.strptime(last_visit, "%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session['visits'] = visits
        request.session['last_visit'] = str(datetime.now())

    request.session.modified = True 

   
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
    visits = request.session.get('visits', 1) 
    return render(request, 'rango/about.html', {'visits': visits})


@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect(reverse('rango:index'))
    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    return render(request, 'rango/add_page.html', {'form':form, 'category':category})
        

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return render(request, 'rango/login.html', {'error': 'Your account is disabled.'})
        else:
            return render(request, 'rango/login.html', {'error': 'Invalid login details.'})

    return render(request, 'rango/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')