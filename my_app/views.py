import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from requests.compat import quote_plus
import django
from .models import Search

BASE_CRAIGLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    search = request.POST.get('search')
    if not search:
        search = ''
    Search.objects.create(search=search)
    final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
    print(final_url)
    # Getting the webpage, creating a Response object
    response = requests.get(final_url)
    # Extracting the source code of the page.
    data = response.text
    # passing the source code to Beautiful soup to create a BeautifulSoup object for it
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craoglist.org/image/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))

    #print("\n\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>", final_postings)

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'base.html', stuff_for_frontend)

def new_search(request):
    return render(request, 'my_app/new_search.html')
