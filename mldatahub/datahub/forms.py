from django import forms


class RecordForm(forms.Form):
    float1 = forms.FloatField(label="Float Value 1")
    float2 = forms.FloatField(label="Float Value 2")
    int_value1 = forms.FloatField(label="Integer Value 1")
