from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    #return HttpResponse("Hello, world. You're at the poll index.")
    return render_to_response("node/show.html", {"pagename":"Root", "id":1, "slots":[{"name":"GP", "text":"Gibts noch nicht"}, {"name":"WP", "text":"Inhalte statt Knoten"}]})
