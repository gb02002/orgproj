from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Organisation, Locations, LocationMedia
from django.core.validators import RegexValidator


class OrgForm(ModelForm):
    """форма для новой org"""

    class Meta:
        model = Organisation
        fields = ['title', 'desc', 'mail', 'phone', 'web']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'desc': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        label = {'desc': 'Description', 'web': 'Web-page of organisation'}


class LocationsForm(forms.ModelForm):
    """Форма для местоположений"""

    open_hours = forms.CharField(widget=forms.TextInput
    (attrs={'validators': [RegexValidator(r'^\d{2}:\d{2} - \d{2}:\d{2}$', message='HH:MM - HH:MM')]}))

    class Meta:
        model = Locations
        fields = ['location_name', 'related_org', 'address', 'open_hours', 'point', 'filter']
        widget = {
            'point': GooglePointFieldWidget,
            # 'open_hours': forms.CharField(attrs={'validators': [RegexValidator(r'^\d{2}:\d{2} - \d{2}:\d{2}$',
            #                                                                    message='HH:MM - HH:MM')]})
        }

    def clean_point(self):
        point = self.cleaned_data.get('point')
        if not isinstance(point, Point):
            point = Point(point)  # Преобразуем текстовое значение в объект Point
        validate_within_bounds(point)  # Проверка на соответствие границам
        return point


def validate_within_bounds(value):
    bounds_dict = {"north": 54.0270141, "south": 50.0819879, "west": 2.90730629, "east": 7.6831597}

    # Получаем координаты точки
    longitude = value.x
    latitude = value.y

    # Получаем границы
    min_longitude = bounds_dict['west']
    max_longitude = bounds_dict['east']
    min_latitude = bounds_dict['south']
    max_latitude = bounds_dict['north']

    # Проверяем, находится ли точка внутри заданных границ
    if not (min_longitude <= longitude <= max_longitude and min_latitude <= latitude <= max_latitude):
        raise ValidationError('Координаты должны находиться в заданных границах')


class LocationMediaForm(forms.ModelForm):
    class Meta:
        model = LocationMedia
        fields = ['image', 'description']
        widget = {
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'accept': 'media/*'}),
        }
# class BaseMediaLocationFormSet(BaseInlineFormSet):
#     def add_fields(self, form, index):
#         super().add_fields(form, index)
#         form.fields['image'].widget.attrs['class'] = 'your-image-class'
#         form.fields['description'].widget.attrs['class'] = 'your-description-class'
#
#
# locations_formset_class = inlineformset_factory(
#     parent_model=Organisation,
#     model=Locations,
#     form=LocationsForm,
#     fields=['location_name', 'related_org', 'address', 'open_hours', 'point', 'filter'],
#     can_delete=True,
#     widgets={
#         'open_hours': forms.CharField(
#             validators=[RegexValidator(r'^\d{2}:\d{2} - \d{2}:\d{2}$', message='HH:MM - HH:MM')]),
#     }
# )
#
#
# location_media_formset_class = inlineformset_factory(
#     parent_model=Locations,
#     model=LocationMedia,
#     fields=['image', 'description'],
#     extra=1,
#     can_delete=False,
#     widgets={
#         'description': forms.Textarea(attrs={'rows': 2, 'cols': 40}),
#     },
#     formset=BaseMediaLocationFormSet,  # Используем кастомный класс formset
# )
