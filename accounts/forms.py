from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Organizador

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    tipo = forms.ChoiceField(
        choices=CustomUser.TIPO_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    empresa = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Solo requerido para organizadores'
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'nombre', 'tipo', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        empresa = cleaned_data.get('empresa')

        if tipo == 'organizador' and not empresa:
            self.add_error('empresa', 'La empresa es requerida para organizadores')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.nombre = self.cleaned_data['nombre']
        
        if commit:
            user.save()
            if user.tipo == 'organizador':
                Organizador.objects.filter(user=user).update(empresa=self.cleaned_data['empresa'])
        
        return user

class CustomUserChangeForm(UserChangeForm):
    password = None
    
    class Meta:
        model = CustomUser
        fields = ('email', 'nombre', 'username')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }