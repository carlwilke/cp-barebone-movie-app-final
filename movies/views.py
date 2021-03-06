from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
import os

AIRTABLE_MOVIESTABLE_BASE_ID="apps32WF86cqq9GSf"
AIRTABLE_API_KEY="keykTFReyKJRWZTg4"

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),
 'Movies',
  api_key=os.environ.get('AIRTABLE_API_KEY', AIRTABLE_API_KEY))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    data_for_frontend = {'search_result': search_result}
   # print(data_for_frontend.items)
    return render(request, 'movies/movies_stuff.html', data_for_frontend)

# Trigger create view
def create(request):
  if request.method == 'POST':
    data = {
      'Name': request.POST.get('name'),
      'Pictures': [{'url': request.POST.get('url')}],
      'Rating': int(request.POST.get('rating')),
      'Notes': request.POST.get('notes')
    }
    response = AT.insert(data)
    # Notify on create
    messages.success(request, 'New Movie Added {}'.format(response['fields'].get('Name')))
  return redirect('/')

def edit(request, movie_id):
  if request.method == 'POST':
    data = {
      'Name': request.POST.get('name'),
      'Pictures': [{'url': request.POST.get('url')}],
      'Rating': int(request.POST.get('rating')),
      'Notes': request.POST.get('notes'),
    }
    response = AT.update(movie_id, data)
    # Notify on update
    messages.success(request, 'Updated Movie: {}'.format(response['fields'].get('Name')))
  return redirect('/')

def delete(request, movie_id):
  movie_name = AT.get(movie_id)['fields']
  AT.delete(movie_id)
  # Notify on delete
  messages.warning(request, 'Deleted Movie: {}'.format(movie_name['fields'].get('Name')))
  return redirect('/')