from django import forms

class OrderForm(forms.Form):
    item_name = forms.CharField(min_length=1)
    plat = forms.IntegerField(min_value=0, required=False)
    quantity = forms.IntegerField(min_value=1, required=False)
    rank = forms.IntegerField(min_value=0, required=False)
