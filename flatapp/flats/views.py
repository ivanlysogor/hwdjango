from django.shortcuts import render
from django.views.generic import ListView, TemplateView, DetailView, \
    FormView, CreateView, UpdateView, DeleteView
from django_celery_results.models import TaskResult
from django.urls import reverse, reverse_lazy
from django.forms import inlineformset_factory
from .models import Flat, Meter, MeterType, MeterValues, Provider, \
    ProviderType
from .forms import FlatForm, MeterForm, MeterValueForm, ProviderForm, \
    ProviderTypeForm, MeterTypeForm
from .tasks import send_meter_values
from flatapp.celery import app as celery_app
from .tasks import extract_param


def index_view(request):
    flats = Flat.objects.order_by('flat_name')

    context = {
        'object_list': flats
    }
    return render(request, 'flats/index.html', context=context)


class FlatListView(ListView):

    model = Flat
    template_name = 'flats/index.html'
    ordering = ['flats.flat_name']

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['contact_info'] = 'ilysogor@gmail.com'
        return context


class AboutTemplateView(TemplateView):
    template_name = 'flats/about.html'


class MeterCreateView(CreateView):
    model = Meter
    template_name = 'meters/create.html'
    success_url = reverse_lazy('flats')
    form_class = MeterForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if 'pk' in self.kwargs.keys():
            context['flat_id'] = self.kwargs['pk']
        else:
            context['flat_id'] = -1
        return context

    def get_initial(self):
        initial = super().get_initial()
        if 'pk' in self.kwargs.keys():
            initial['flat_id'] = self.kwargs['pk']
        return initial

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class MeterUpdateView(UpdateView):
    model = Meter
    template_name = 'meters/update.html'
    form_class = MeterForm
    success_url = reverse_lazy('flats')



class MeterTypeCreateView(CreateView):
    model = MeterType
    fields = '__all__'
    template_name = 'metertypes/create.html'
    success_url = reverse_lazy('metertypes')

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class MeterTypeDeleteView(DeleteView):
    model = MeterType
    success_url = reverse_lazy('metertypes')
    # страница для подтверждения удаления
    template_name = 'metertypes/delete_confirm.html'


class MeterTypeListView(ListView):
    model = MeterType
    template_name = 'metertypes/index.html'
    ordering = ['meter_types.metertype_name']


class MeterTypeUpdateView(UpdateView):
    model = MeterType
    template_name = 'metertypes/update.html'
    form_class = MeterTypeForm
    success_url = reverse_lazy('metertypes')

    def get_success_url(self, **kwargs):
        if kwargs:
            return reverse_lazy('metertype-update', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('metertype-update', args=(self.object.id,))


class FlatCreateView(CreateView):

    model = Flat
    template_name = 'flats/create.html'
    success_url = reverse_lazy('flats')
    form_class = FlatForm

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class MeterValueUpdateView(UpdateView):
    pass


class FlatUpdateView(UpdateView):
    model = Flat
    template_name = 'flats/update.html'
    form_class = FlatForm
    success_url = reverse_lazy('flat-update')

    def get_success_url(self, **kwargs):
        if kwargs:
            return reverse_lazy('flat-update', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('flat-update', args=(self.object.id,))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        flat_meters = []
        meters = Meter.objects.filter(flat_id=self.kwargs['pk'])
        i = 0
        for meter in meters:
            meter_values = MeterValues.objects.filter(meter_id=meter.pk).order_by("-mv_date")[:5]
            if meter.metertype_id.meter_type_params:
                num_values = extract_param("values", meter.metertype_id.meter_type_params)
            else:
                num_values = 1
            if num_values == "":
                num_values = 1
            else:
                num_values = int(num_values)
            flat_meters.append({
                'meter': meter,
                'index': i,
                'num_values': num_values,
                'values': meter_values
            })
            i = i + 1

        context.update({
            'id': self.kwargs['pk'],
            'flat_meters': flat_meters,
            'meters_count': i
        })
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()

        for i in range(int(request.POST['meters_count'])):
            if request.POST[f'meter_{i}_v1'] != '':
                v1 = request.POST[f'meter_{i}_v1']
                v2 = None
                if f'meter_{i}_v2' in request.POST.keys():
                    if request.POST[f'meter_{i}_v2'] != '':
                        v2 = request.POST[f'meter_{i}_v2']
                v3 = None
                if f'meter_{i}_v3' in request.POST.keys():
                    if request.POST[f'meter_{i}_v3'] != '':
                        v3 = request.POST[f'meter_{i}_v3']

                meter = Meter.objects.get(pk=request.POST[f'meter_{i}'])
                meter_values = MeterValues(meter_id=meter,
                                           mv_v1=v1,
                                           mv_v2=v2,
                                           mv_v3=v3)
                meter_values.save()
                send_meter_values.delay(meter.pk, meter_values.pk, v1, v2, v3)

        return super(FlatUpdateView, self).post(request, **kwargs)


class FlatDeleteView(DeleteView):
    model = Flat
    success_url = reverse_lazy('flats')
    # страница для подтверждения удаления
    template_name = 'flats/delete_confirm.html'


class FlatDetailView(DetailView):
    model = Flat
    template_name = 'flats/flat.html'


class MeterDeleteView(DeleteView):
    model = Meter
    success_url = reverse_lazy('flats')
    # страница для подтверждения удаления
    template_name = 'meters/delete_confirm.html'


class ProviderTypeCreateView(CreateView):
    model = ProviderType
    fields = '__all__'
    template_name = 'providertypes/create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class ProviderTypeDeleteView(DeleteView):
    model = ProviderType
    success_url = reverse_lazy('providertypes')
    # страница для подтверждения удаления
    template_name = 'providertypes/delete_confirm.html'


class ProviderTypeListView(ListView):
    model = ProviderType
    template_name = 'providertypes/index.html'
    ordering = ['provider_types.providertype_name']


class ProviderTypeUpdateView(UpdateView):
    model = ProviderType
    template_name = 'providertypes/update.html'
    form_class = ProviderTypeForm
    success_url = reverse_lazy('providertypes')

    def get_success_url(self, **kwargs):
        if kwargs:
            return reverse_lazy('providertype-update', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('providertype-update', args=(self.object.id,))


class ProviderCreateView(CreateView):
    model = Provider
    fields = '__all__'
    template_name = 'providers/create.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        return super().post(request, args, kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class ProviderDeleteView(DeleteView):
    model = Provider
    success_url = reverse_lazy('providers')
    # страница для подтверждения удаления
    template_name = 'providers/delete_confirm.html'


class ProviderListView(ListView):
    model = Provider
    template_name = 'providers/index.html'
    ordering = ['providers.provider_name']


class ProviderUpdateView(UpdateView):
    model = Provider
    template_name = 'providers/update.html'
    form_class = ProviderForm
    success_url = reverse_lazy('providers')

    def get_success_url(self, **kwargs):
        if kwargs:
            return reverse_lazy('provider-update', kwargs={'pk': kwargs['pk']})
        else:
            return reverse_lazy('provider-update', args=(self.object.id,))



class TasksListView(ListView):
    template_name = 'tasks/index.html'
    ordering = []
    model = TaskResult
    paginate_by = 10

