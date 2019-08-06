from comuni_italiani import models as comuni_italiani_models
from crispy_forms.bootstrap import Div, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit, Button
from dal import autocomplete
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import formset_factory, inlineformset_factory

from .models import *
import datetime


class ProfileForm(forms.ModelForm):
    cf = forms.CharField(max_length=16, disabled=True, label='CF', required=False)
    nome = forms.CharField(max_length=30)
    cognome = forms.CharField(max_length=30)

    residenza_via = forms.CharField(max_length=100, label='Via')
    residenza_n = forms.CharField(max_length=20, label='Civico')
    residenza_comune = forms.ModelChoiceField(queryset=comuni_italiani_models.Comune.objects.all(), label='Comune',
                                              widget=autocomplete.ModelSelect2(url='comune-autocomplete',
                                                                               attrs={'data-html': True,
                                                                                      'data-theme': 'bootstrap4', }))
    residenza_provincia = forms.ModelChoiceField(queryset=comuni_italiani_models.Provincia.objects.all(),
                                                 label='Provincia',
                                                 widget=autocomplete.ModelSelect2(url='provincia-autocomplete',
                                                                                  attrs={'data-html': True,
                                                                                         'data-theme': 'bootstrap4', }))

    domicilio_via = forms.CharField(max_length=100, label='Via')
    domicilio_n = forms.CharField(max_length=20, label='Civico')
    domicilio_comune = forms.ModelChoiceField(queryset=comuni_italiani_models.Comune.objects.all(), label='Comune',
                                              widget=autocomplete.ModelSelect2(url='comune-autocomplete',
                                                                               attrs={'data-html': True,
                                                                                      'data-theme': 'bootstrap4', }))
    domicilio_provincia = forms.ModelChoiceField(queryset=comuni_italiani_models.Provincia.objects.all(),
                                                 label='Provincia',
                                                 widget=autocomplete.ModelSelect2(url='provincia-autocomplete',
                                                                                  attrs={'data-html': True,
                                                                                         'data-theme': 'bootstrap4', }))

    class Meta:
        model = Profile

        exclude = ['user', 'residenza', 'domicilio']
        widgets = {
            'data_nascita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tutor': forms.TextInput(attrs={'placeholder': 'Prof/Prof.ssa'}),
            'anno_dottorato': forms.NumberInput(attrs={'placeholder': '1, 2, 3'}),
            'luogo_nascita': autocomplete.ModelSelect2(url='comune-autocomplete',
                                                       attrs={'data-html': True, 'data-theme': 'bootstrap4', }),
        }
        labels = {
            'data_nascita': 'Data di nascita',
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

        if self.instance.residenza is not None:
            self.fields['residenza_via'].initial = self.instance.residenza.via
            self.fields['residenza_n'].initial = self.instance.residenza.n
            self.fields['residenza_comune'].initial = self.instance.residenza.comune
            self.fields['residenza_provincia'].initial = self.instance.residenza.provincia

        if self.instance.domicilio is not None:
            self.fields['domicilio_via'].initial = self.instance.domicilio.via
            self.fields['domicilio_n'].initial = self.instance.domicilio.n
            self.fields['domicilio_comune'].initial = self.instance.domicilio.comune
            self.fields['domicilio_provincia'].initial = self.instance.domicilio.provincia

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'RimborsiApp:profile'
        self.helper.add_input(Submit('submit', 'Aggiorna'))

        self.helper.layout = Layout(
            Row(Column('nome', css_class="col-6"), Column('cognome', css_class="col-6")),
            Row(Column('data_nascita', css_class="col-3"), Column('luogo_nascita', css_class="col-3"),
                Column('cf', css_class="col-3"), Column('sesso', css_class="col-3")),
            Fieldset("Residenza", Row(
                Column('residenza_via', css_class='col-4'),
                Column('residenza_n', css_class='col-2'),
                Column('residenza_comune', css_class='col-3'),
                Column('residenza_provincia', css_class='col-3'), css_id='residenza-row')),

            Fieldset("Domicilio", Row(
                Column('domicilio_via', css_class='col-4'),
                Column('domicilio_n', css_class='col-2'),
                Column('domicilio_comune', css_class='col-3'),
                Column('domicilio_provincia', css_class='col-3'), css_id='domicilio-row'), css_id='domicilio-fieldset'),

            Row(Column('qualifica', css_class="col-6"), Column('datore_lavoro', css_class="col-6")),
            Row(Column('tutor', css_class="col-4"), Column('anno_dottorato', css_class="col-2"),
                Column('scuola_dottorato', css_class="col-6"), css_id="dottorando-details"),

        )

    def save(self, commit=True):
        super(ProfileForm, self).save(commit)
        self.instance.user.first_name = self.cleaned_data.get('nome')
        self.instance.user.last_name = self.cleaned_data.get('cognome')
        if commit:
            self.instance.user.save()
        return self.instance


class MissioneForm(forms.ModelForm):
    mezzi_previsti = forms.MultipleChoiceField(choices=MEZZO_CHOICES, required=False)
    automobile = forms.ModelChoiceField(queryset=None, empty_label="---", required=False)
    motivazione_automobile = forms.MultipleChoiceField(choices=MOTIVAZIONE_AUTO_CHOICES, required=False,
                                                       widget=forms.CheckboxSelectMultiple)

    # automobile_altrui = forms.CharField(label='Proprietario auto', required=False)

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
            'automobile_altrui': 'Proprietario auto',
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
            Row(Div(InlineCheckboxes('mezzi_previsti'), css_class="col-6"), Div('automobile', css_class="col-6"),
                Div('automobile_altrui', css_class="col-6")),
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
    data = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'required': 'required', }))
    desc_label = 'Descrizione (numero fattura/ricevuta fiscale)'
    s1 = forms.DecimalField(decimal_places=2, label='Spesa', required=True,
                            widget=forms.NumberInput(attrs={'class': 'form-control', }))
    d1 = forms.CharField(required=False, label=desc_label, widget=forms.TextInput(attrs={'class': 'form-control', }), )


class TrasportoForm(forms.ModelForm):
    class Meta:
        model = Trasporto
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control trasporti-date', 'required': 'required', }),
            'da': forms.TextInput(attrs={'class': 'form-control', }),
            'a': forms.TextInput(attrs={'class': 'form-control', }),
            'mezzo': forms.Select(attrs={'class': 'form-control trasporti-mezzo', 'required': 'required', }),
            'tipo_costo': forms.TextInput(attrs={'class': 'form-control', }),
            'costo': forms.NumberInput(
                attrs={'class': 'form-control trasporti-costo', 'step': 0.01, 'required': 'required', }),
            'km': forms.NumberInput(attrs={'class': 'form-control trasporti-km', 'step': 0.01}),
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
    dichiarazione_check_std = forms.BooleanField(label='Dichiarazione precompilata di partecipazione evento',
                                                 required=False, initial=True)
    dichiarazione_check_pers = forms.BooleanField(label='Dichiarazione personalizzata:', required=False)

    class Meta:
        model = ModuliMissione
        fields = '__all__'
        exclude = ['missione', 'parte_1_file', 'parte_2_file', 'kasko_file', 'dottorandi_file']
        widgets = {
            'parte_1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }, ),
            'parte_2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'kasko': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'dottorandi': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'atto_notorio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', }),
            'atto_notorio_dichiarazione': forms.Textarea(attrs={'rows': 4, }, )
        }
        labels = {
            'parte_1': 'Data Richiesta',
            'parte_2': 'Data Richiesta',
            'kasko': 'Data Richiesta',
            'dottorandi': 'Data Richiesta',
            'atto_notorio': 'Data Richiesta',
        }

    def clean(self):
        cleaned_data = super(ModuliMissioneForm, self).clean()
        missione_inizio = self.instance.missione.inizio
        missione_fine = self.instance.missione.fine
        parte_1_data = cleaned_data.get("parte_1")
        parte_2_data = cleaned_data.get("parte_2")
        atto_notorio_data = cleaned_data.get("atto_notorio")
        dottorandi_data = cleaned_data.get("dottorandi")
        kasko_data = cleaned_data.get("kasko")

        errors = {}
        if atto_notorio_data.weekday() >= 5:
            errors['atto_notorio'] = \
                f"Atto notorio deve avere una data di compilazione che non sia sabato o domenica"

        if parte_2_data.weekday() >= 5:
            errors['parte_2'] = \
                f"Missione parte II deve avere una data di compilazione che non sia sabato o domenica"

        if parte_1_data.weekday() >= 5:
            errors['parte_1'] = f"Missione parte I deve avere una data di compilazione che non sia sabato o domenica"

        if self.instance.missione.user.profile.qualifica == 'DOTTORANDO' and dottorandi_data.weekday() >= 5:
            errors['dottorandi'] = \
                f"Autorizzazione dottorandi deve avere una data di compilazione che non sia sabato o domenica"

        if kasko_data.weekday() >= 5:
            errors['kasko'] = f"Kasko deve avere una data di compilazione che non sia sabato o domenica"

        if atto_notorio_data < missione_fine:
            errors['atto_notorio'] = \
                f"Atto notorio deve avere una data di compilazione successiva a quella di fine missione ({missione_fine.strftime('%d/%m/%Y')})"

        if parte_2_data < missione_fine:
            errors['parte_2'] = \
                f"Missione parte II deve avere una data di compilazione successiva a quella di fine missione ({missione_fine.strftime('%d/%m/%Y')})"

        if parte_1_data > missione_inizio:
            errors['parte_1'] = \
                f"Missione parte I deve avere una data di compilazione antecedente a quella di inizio missione ({missione_inizio.strftime('%d/%m/%Y')})"

        if self.instance.missione.user.profile.qualifica == 'DOTTORANDO' and dottorandi_data > missione_inizio:
            errors['dottorandi'] = \
                f"Autorizzazione dottorandi deve avere una data di compilazione antecedente a quella di inizio missione ({missione_inizio.strftime('%d/%m/%Y')})"

        if kasko_data > missione_inizio:
            errors['kasko'] = \
                f"Kasko deve avere una data di compilazione antecedente a quella di inizio missione ({missione_inizio.strftime('%d/%m/%Y')})"

        if len(errors) > 0:
            raise forms.ValidationError(errors)
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ModuliMissioneForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # self.helper.field_template = 'bootstrap4/layout/inline_field.html'
        # self.helper.form_class = 'form-inline'
        self.helper.form_tag = False
        self.fields['atto_notorio_dichiarazione'].label = ''
        if self.instance.atto_notorio_dichiarazione != '':
            self.fields['dichiarazione_check_pers'].initial = True
        else:
            self.fields['atto_notorio_dichiarazione'].disable = True


automobile_formset = inlineformset_factory(User, Automobile, AutomobileForm, extra=0, can_delete=True,
                                           exclude=('user',), min_num=1)
trasporto_formset = inlineformset_factory(Missione, Trasporto, TrasportoForm, extra=0, can_delete=True,
                                          fields='__all__', min_num=1)
scontrino_formset = formset_factory(ScontrinoForm, extra=0)
scontrino_extra_formset = formset_factory(ScontrinoExtraForm, can_delete=True, extra=0, min_num=1)
