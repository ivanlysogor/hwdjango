from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, \
    FormView, CreateView, UpdateView, DeleteView
from .models import Flat
from .forms import FlatForm


def index_view(request):
    flats = Flat.objects.all()

    context = {
        'object_list': flats
    }
    return render(request, 'flats/index.html', context=context)


class FlatListView(ListView):
    model = Flat
    template_name = 'flats/index.html'


class AboutTemplateView(TemplateView):
    template_name = 'flats/about.html'


class FlatCreateView(CreateView):

    model = Flat
    template_name = 'flats/create.html'
    success_url = '/'
    form_class = FlatForm

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class FlatUpdateView(UpdateView):
    model = Flat
    template_name = 'flats/update.html'
    success_url = '/'
    form_class = FlatForm


class FlatDeleteView(DeleteView):
    model = Flat
    success_url = '/'
    # страница для подтверждения удаления
    template_name = 'flats/delete_confirm.html'


class FlatDetailView(DetailView):
    model = Flat
    template_name = 'flats/flat.html'