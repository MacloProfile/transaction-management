from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
    file_format = forms.ChoiceField(choices=(('csv','CSV'), ('xlsx','XLSX')), required=False)
