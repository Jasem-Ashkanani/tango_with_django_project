import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_category('Python', views=128, likes=64)
    django_cat = add_category('Django', views=64, likes=32)
    other_cat = add_category('Other Frameworks', views=32, likes=16)

    add_page(cat=python_cat, title="Official Python Tutorial",
             url="http://docs.python.org/3/tutorial/")
    add_page(cat=python_cat, title="How to Think like a Computer Scientist",
             url="http://www.greenteapress.com/thinkpython/")
    add_page(cat=python_cat, title="Learn Python in 10 Minutes",
             url="http://www.korokithakis.net/tutorials/python/")

    add_page(cat=django_cat, title="Official Django Tutorial",
             url="https://docs.djangoproject.com/en/2.2/intro/tutorial01/")
    add_page(cat=django_cat, title="Django Rocks",
             url="http://www.djangorocks.com/")
    add_page(cat=django_cat, title="How to Tango with Django",
             url="http://www.tangowithdjango.com/")

    add_page(cat=other_cat, title="Bottle",
             url="http://bottlepy.org/docs/dev/")
    add_page(cat=other_cat, title="Flask",
             url="http://flask.pocoo.org")
    
    print("Database populated!")

def add_category(name, views=0, likes=0):
    category, created = Category.objects.get_or_create(name=name, defaults={'views': views, 'likes': likes})
    return category

def add_page(cat, title, url, views=0):
    if cat is None:
        print(f"Error: Category is None when adding page '{title}'")
        return None
    page, created = Page.objects.get_or_create(category=cat, title=title, url=url, views=views)
    return page
    


if __name__ == '__main__':
    print("Starting Rango populated script...")
    populate()