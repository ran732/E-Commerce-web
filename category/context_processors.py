from . models import Catogery

def menu_links(request):
    links = Catogery.objects.all()
    return dict(links=links)