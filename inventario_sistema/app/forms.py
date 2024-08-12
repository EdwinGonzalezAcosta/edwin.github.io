from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Inventario

# Formulario para el registro de usuarios
class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Formulario para el modelo Inventario
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = [
            'cod_patrimonial', 'cod_interno', 'ano_ingreso', 'descripcion','denominacion','marca',
            'modelo', 'color', 'serie', 'dimensiones', 'estado_mueble', 'observaciones',
            'estado_logico', 'foto', 'qr_code', 'usuario'
        ]
        widgets = {
            'descripcion': forms.Select(attrs={'class': 'form-select'}),
            'denominacion': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_mueble': forms.Select(attrs={'class': 'form-select'}),
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'qr_code': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'cod_patrimonial': forms.TextInput(attrs={'class': 'form-control'}),
            'cod_interno': forms.TextInput(attrs={'class': 'form-control'}),
            'ano_ingreso': forms.DateInput(attrs={'type': 'date','class': 'form-control' }),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'serie': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'estado_logico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }