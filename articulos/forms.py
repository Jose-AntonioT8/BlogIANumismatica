from datetime import date

from django import forms

from .models import Article
from .text import TIPOS, is_real_date


class ArticleForm(forms.ModelForm):
    title = forms.CharField(
        required=False,
        label='Título',
        widget=forms.TextInput(attrs={'maxlength': '120', 'autocomplete': 'off'}),
    )
    piece_type = forms.CharField(
        required=False,
        label='Tipo de pieza',
        widget=forms.Select(choices=[('', 'Elegir…'), *[(name, name) for name in TIPOS]]),
    )
    published_on = forms.CharField(
        required=False,
        label='Fecha de publicación',
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    body = forms.CharField(
        required=False,
        label='Cuerpo',
        widget=forms.Textarea,
    )

    class Meta:
        model = Article
        fields = ['title', 'piece_type', 'published_on', 'body']

    def clean_title(self):
        title = (self.cleaned_data.get('title') or '').strip()
        if not title:
            raise forms.ValidationError('El título es obligatorio')
        if len(title) > 120:
            raise forms.ValidationError('El título admite como máximo 120 caracteres')
        return title

    def clean_body(self):
        body = (self.cleaned_data.get('body') or '').strip()
        if not body:
            raise forms.ValidationError('El cuerpo es obligatorio')
        if len(body) > 20000:
            raise forms.ValidationError('El cuerpo admite como máximo 20000 caracteres')
        return body

    def clean_published_on(self):
        raw = (self.cleaned_data.get('published_on') or '').strip()
        if not raw:
            raise forms.ValidationError('La fecha es obligatoria')
        if not is_real_date(raw):
            raise forms.ValidationError('La fecha debe ser un día real con el formato AAAA-MM-DD')
        year, month, day = (int(part) for part in raw.split('-'))
        return date(year, month, day)

    def clean_piece_type(self):
        piece_type = (self.cleaned_data.get('piece_type') or '').strip()
        if not piece_type:
            raise forms.ValidationError('El tipo es obligatorio')
        if piece_type not in TIPOS:
            raise forms.ValidationError('El tipo debe ser Moneda, Billete o Medalla')
        return piece_type
