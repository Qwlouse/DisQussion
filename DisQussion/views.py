from django.http import HttpResponse
from django.shortcuts import render_to_response
from DisQussion.structure.models import *

def home(request):
    #return HttpResponse("Hello, world. You're at the poll index.")
    return render_to_response("node/show.html", {"pagename":"Root", "id":1, "slots":[{"name":"GP", "list":[{"id":2, "text":"Gibts noch nicht"}, {"id":3, "text":"Gibbet wohl"}]}, {"name":"WP", "list":[{"id":7, "text":"WP is doof"}, {"id":8, "text":"WP is toll"}]}]})
    
def path(request, path):
        current_node = StructureNode.objects.filter(parent=None)[0] # root
        for p in path.split("/"):
            short_title, local_id = p.split(".")
            slots = current_node.slot_set.filter(short_title=short_title)
            if len(slots) < 1:
                    return HttpResponse("Error: Slot not found")
            slot = slots[0]
                    
            
            text_node = slot.textnode_set.filter(nr_in_parent=local_id).first()
            text_node = slot.textnode_set.filter(nr_in_parent=local_id).first()
            
        return HttpResponse(str(path))
