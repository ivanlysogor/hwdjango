from django.shortcuts import render
from .models import Flat


def index_view(request):
    flats = Flat.objects.all()

    # animals = Animal.objects.select_related('kind', 'kind__family')
    # select_related - когда ForeignKey
    # prefetch_relate - когда ManyToMany
    context = {
        'flats': flats
    }
    return render(request, 'flats/index.html', context=context)
    # flask
    # return render(request, 'animals/index.html', animals=animals, zoo_name='Три поросенка')
    # return render(request, 'animals/index.html', **context)

