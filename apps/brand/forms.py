from django import forms
from django.core.exceptions import ValidationError

from apps.brand.models import Filial


class FilialForm(forms.ModelForm):
    class Meta:
        model = Filial
        fields = '__all__'

    def clean(self):
        super().clean()
        errors = {}
        start_work = self.cleaned_data['start_work']
        end_work = self.cleaned_data['end_work']
        is_around_the_clock = self.cleaned_data['is_around_the_clock']

        if not (is_around_the_clock or (start_work and end_work)):
            errors['is_around_the_clock'] = ValidationError(
                'Обязательно заполнить дату начала и конца рабочего времени'
                'или указать как круглосуточно'
            )
        if errors:
            raise ValidationError(errors)
