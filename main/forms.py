import re
from django import forms

from .models import Listing


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field
from crispy_forms.bootstrap import PrependedText

class ListingForm(forms.ModelForm):
    image = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('brand', css_class='form-group col-md-6 mb-0'),
                Column('model', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'vin',
            Row(
                Column('mileage', css_class='form-group col-md-6 mb-0'),
                Column(PrependedText('price', '$'), css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'color', 'description', 'engine', 'transmission', 'image'
        )

    class Meta:
        model = Listing
        fields = ('brand', 'model', 'vin', 'mileage', 'price',
                  'color', 'description', 'engine', 'transmission', 'image')