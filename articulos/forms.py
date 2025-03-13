from django import forms
from .models import Articulo
from django.utils.translation import gettext_lazy as _

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ['titulo', 'contenido', 'tema', 'etiquetas', 'imagen']
        
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': _('Introduce un título descriptivo (mínimo 5 caracteres).'),
                'class': 'form-control',
            }),
            'contenido': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': _('Escribe el contenido aquí...'),
                'class': 'form-control',
            }),
            'tema': forms.Select(attrs={
                'class': 'form-select',
            }),
            'etiquetas': forms.TextInput(attrs={
                'placeholder': _('Etiquetas separadas por comas, ej: filosofía, psicología.'),
                'class': 'form-control',
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
        }
        
        labels = {
            'titulo': _('Título'),
            'contenido': _('Contenido'),
            'tema': _('Tema'),
            'etiquetas': _('Etiquetas'),
            'imagen': _('Imagen'),
        }

        help_texts = {
            'etiquetas': _('Usa comas para separar las etiquetas. Ejemplo: filosofía, psicología, negocios.'),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError(_("El título debe tener al menos 5 caracteres."))
        return titulo

    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        if len(contenido) < 20:
            raise forms.ValidationError(_("El contenido debe tener al menos 20 caracteres."))
        return contenido

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            valid_extensions = ['jpg', 'jpeg', 'png']
            if not imagen.name.split('.')[-1].lower() in valid_extensions:
                raise forms.ValidationError(_("Solo se permiten archivos JPG, JPEG o PNG."))
            if imagen.size > 5 * 1024 * 1024:  # Tamaño máximo 5MB
                raise forms.ValidationError(_("La imagen no debe exceder 5MB."))
        return imagen