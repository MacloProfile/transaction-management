from django import forms


class GenerateQRForm(forms.Form):
    product_id = forms.IntegerField(label="ID товара")
