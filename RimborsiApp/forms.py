from crispy_forms.bootstrap import Div, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import formset_factory, inlineformset_factory

from .models import *


class ProfileForm(forms.ModelForm):
    cf = forms.CharField(max_length=16, disabled=True, label='CF', required=False)
    nome = forms.CharField(max_length=30)
    cognome = forms.CharField(max_length=30)

    # luogo_nascita = forms.ModelChoiceField(queryset=Comune.objects.all(), empty_label="---")

    class Meta:
        model = Profile

        exclude = ['user', ]  # todo uncomment
        # exclude = ['user', 'luogo_nascita']  # todo uncomment
        widgets = {
            'data_nascita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tutor': forms.TextInput(attrs={'disabled': 'disabled', 'placeholder': 'Prof/Prof.ssa'}),
            'anno_dottorato': forms.NumberInput(attrs={'disabled': 'disabled', 'placeholder': '1, 2, 3'}),
            'scuola_dottorato': forms.TextInput(attrs={'disabled': 'disabled'}, ),
        }
        labels = {
            'data_nascita': 'Data di nascita',
            'domicilio_fiscale_provincia': 'Domicilio fiscale Provincia',
            'datore_lavoro': 'Datore di lavoro',
            'tutor': 'Nome e cognome del tutor',
            'anno_dottorato': 'Anno di dottorato',
            'scuola_dottorato': 'Nome della scuola di dottorato',
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = self.instance.user.first_name
        self.fields['cognome'].initial = self.instance.user.last_name
        self.fields['cf'].initial = self.instance.cf

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'profile'
        self.helper.add_input(Submit('submit', 'Aggiorna'))

        self.helper.layout = Layout(
            Row(Div('nome', css_class="col-6"), Div('cognome', css_class="col-6")),
            Row(Div('data_nascita', css_class="col-3"), Div('luogo_nascita', css_class="col-3"),
                Div('cf', css_class="col-3"), Div('sesso', css_class="col-3")),
            Row(Div('domicilio_fiscale', css_class="col-6"), Div('domicilio_fiscale_provincia', css_class="col-6")),
            Row(Div('qualifica', css_class="col-6"), Div('datore_lavoro', css_class="col-6")),
            Row(Div('tutor', css_class="col-4"), Div('anno_dottorato', css_class="col-2"),
                Div('scuola_dottorato', css_class="col-6")),

        )

    def save(self, *args, **kwargs):
        super(ProfileForm, self).save(*args, **kwargs)
        self.instance.user.first_name = self.cleaned_data.get('nome')
        self.instance.user.last_name = self.cleaned_data.get('cognome')
        self.instance.user.save()


class MissioneForm(forms.ModelForm):
    automobile = forms.ModelChoiceField(queryset=None, empty_label="---", required=False)
    mezzi_previsti = forms.MultipleChoiceField(choices=MEZZO_CHOICES, required=False)
    motivazione_automobile = forms.MultipleChoiceField(choices=MOTIVAZIONE_AUTO_CHOICES, required=False,
                                                       widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Missione
        fields = '__all__'
        exclude = ('user', 'scontrino', 'pernottamento', 'altrespese')

        widgets = {
            'inizio': forms.DateInput(attrs={'type': 'date'}),
            'fine': forms.DateInput(attrs={'type': 'date'}),
            'inizio_ora': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
            'fine_ora': forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        }
        labels = {
            'stato_destinazione': 'Stato di destinazione',
            'citta_destinazione': 'Città di destinazione',
            'mezzi_previsti': 'Mezzi',
        }

    def clean(self):
        cleaned_data = super(MissioneForm, self).clean()
        inizio = cleaned_data.get("inizio")
        fine = cleaned_data.get("fine")
        inizio_ora = cleaned_data.get("inizio_ora")
        fine_ora = cleaned_data.get("fine_ora")

        if fine < inizio:
            raise forms.ValidationError("La data di inizio deve essere antecedente a quella di fine.")
        if inizio == fine and fine_ora < inizio_ora:
            raise forms.ValidationError("L'ora di inizio deve essere antecedente a quella di fine.")
        return cleaned_data

    def __init__(self, user=None, *args, **kwargs):
        super(MissioneForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['automobile'].queryset = Automobile.objects.filter(user=user)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_action = 'missione'
        try:
            _ = kwargs['instance']
            self.helper.add_input(Submit('submit', 'Aggiorna'))
        except KeyError:
            self.helper.add_input(Submit('submit', 'Crea'))

        self.helper.layout = Layout(
            Row(Div('citta_destinazione', css_class="col-6"), Div('stato_destinazione', css_class="col-6")),
            Row(Div('inizio', css_class="col-3"), Div('inizio_ora', css_class="col-3"),
                Div('fine', css_class="col-3"), Div('fine_ora', css_class="col-3")),
            Row(Div('fondo', css_class="col-6"), Div('struttura_fondi', css_class="col-6")),
            Row(Div('motivazione', css_class="col-12")),
            Row(Div(InlineCheckboxes('mezzi_previsti'), css_class="col-6"), Div('automobile', css_class="col-6")),
            Row(Div(InlineCheckboxes('motivazione_automobile'), css_class="col-12")),
        )


class ScontrinoForm(forms.Form):
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    desc_label = 'Descrizione (numero fattura/ricevuta fiscale)'
    s1 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', }))
    d1 = forms.CharField(required=False, label=desc_label, widget=forms.TextInput(attrs={'class': 'form-control', }))
    s2 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', }))
    d2 = forms.CharField(required=False, label=desc_label, widget=forms.TextInput(attrs={'class': 'form-control', }))
    s3 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', }))
    d3 = forms.CharField(required=False, label=desc_label, widget=forms.TextInput(attrs={'class': 'form-control', }))


class ScontrinoExtraForm(forms.Form):
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    desc_label = 'Descrizione (numero fattura/ricevuta fiscale)'
    s1 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control', }))
    d1 = forms.CharField(required=False, label=desc_label, widget=forms.TextInput(attrs={'class': 'form-control', }), )


class TrasportoForm(forms.ModelForm):
    class Meta:
        model = Trasporto
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control trasporti-date', }),
            'da': forms.TextInput(attrs={'class': 'form-control', }),
            'a': forms.TextInput(attrs={'class': 'form-control', }),
            'mezzo': forms.Select(attrs={'class': 'form-control trasporti-mezzo', }),
            'km': forms.NumberInput(attrs={'class': 'form-control trasporti-km', }),
            'tipo_costo': forms.TextInput(attrs={'class': 'form-control', }),
            'costo': forms.NumberInput(attrs={'class': 'form-control trasporti-costo', }),
        }
        labels = {
            'costo': 'Spesa',
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False


class AutomobileForm(forms.ModelForm):
    class Meta:
        model = Automobile
        fields = ('marca', 'modello', 'targa',)
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control', }),
            'modello': forms.TextInput(attrs={'class': 'form-control', }),
            'targa': forms.TextInput(attrs={'class': 'form-control', }),
        }


class ModuliMissioneForm(forms.ModelForm):
    class Meta:
        model = ModuliMissione
        fields = '__all__'
        exclude = ['missione', 'parte_1_file', 'parte_2_file', 'kasko_file', 'dottorandi_file']
        widgets = {
            'parte_1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }, ),
            'parte_2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'kasko': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'dottorandi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
        }
        labels = {
            'parte_1': 'Data Richiesta',
            'parte_2': 'Data Richiesta',
            'kasko': 'Data Richiesta',
            'dottorandi': 'Data Richiesta',
        }

    def __init__(self, *args, **kwargs):
        super(ModuliMissioneForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        # self.helper.form_class = 'form-inline'
        self.helper.form_tag = False


automobile_formset = inlineformset_factory(User, Automobile, AutomobileForm, extra=1, can_delete=True,
                                           exclude=('user',))
trasporto_formset = inlineformset_factory(Missione, Trasporto, TrasportoForm, extra=1, can_delete=True,
                                          fields='__all__')
scontrino_formset = formset_factory(ScontrinoForm, extra=0)
scontrino_extra_formset = formset_factory(ScontrinoExtraForm, can_delete=True)
