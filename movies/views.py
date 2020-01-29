from django.shortcuts import render
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