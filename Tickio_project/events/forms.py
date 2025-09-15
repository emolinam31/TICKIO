from django import forms
from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'fecha',
            'lugar',
            'cupos_disponibles',
            'precio',
            'estado',
        ]

    def __init__(self, *args, **kwargs):
        self.organizador = kwargs.pop('organizador', None)
        super().__init__(*args, **kwargs)
        
        # Agregar clases de Bootstrap a todos los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Configuración específica para cada campo
        self.fields['nombre'].widget.attrs.update({
            'placeholder': 'Nombre del evento'
        })
        self.fields['descripcion'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Descripción del evento'
        })
        self.fields['categoria'].widget.attrs.update({
            'class': 'form-select'
        })
        self.fields['fecha'].widget = forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
        self.fields['lugar'].widget.attrs.update({
            'placeholder': 'Ubicación del evento'
        })
        self.fields['cupos_disponibles'].widget.attrs.update({
            'min': '1',
            'placeholder': 'Número de cupos disponibles'
        })
        self.fields['precio'].widget.attrs.update({
            'placeholder': 'Precio del evento',
            'step': '0.01'
        })
        self.fields['estado'].widget = forms.Select(
            choices=Evento.ESTADO_CHOICES,
            attrs={'class': 'form-select'}
        )

    def save(self, commit=True):
        evento = super().save(commit=False)
        if self.organizador:
            evento.organizador = self.organizador
        if commit:
            evento.save()
        return evento