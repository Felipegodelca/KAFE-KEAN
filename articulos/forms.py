from django import forms

from .models import Articulo


class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ["titulo", "descripcion", "contenido", "imagen"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
