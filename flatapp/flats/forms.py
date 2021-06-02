from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Flat, Meter, MeterType, MeterValues, \
    Provider, ProviderType


def get_meters_per_flat():
    return Meter.objects.all()


class FlatForm(forms.ModelForm):
    class Meta:
        model = Flat
        fields = '__all__'


class ProviderTypeForm(forms.ModelForm):
    class Meta:
        model = ProviderType
        fields = '__all__'


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'


class MeterForm(forms.ModelForm):
    class Meta:
        model = Meter
        fields = '__all__'


class MeterValueForm(forms.ModelForm):
    class Meta:
        model = MeterValues
        fields = '__all__'
