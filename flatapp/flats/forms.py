from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Flat, Meter, MeterType, MeterValues


def get_meters_per_flat():
    return Meter.objects.all()


class FlatForm(forms.ModelForm):

    class Meta:
        model = Flat
        fields = '__all__'


class MeterForm(forms.ModelForm):

    class Meta:
        model = Meter
        fields = '__all__'


class MeterValueForm(forms.ModelForm):

    class Meta:
        model = MeterValues
        fields = '__all__'
