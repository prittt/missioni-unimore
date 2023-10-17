from comuni_italiani import models as comuni_italiani_models
from crispy_forms.bootstrap import Div, InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Fieldset, Layout, Row, Submit
from dal import autocomplete
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import formset_factory, inlineformset_factory

from .models import *


class ForeignProfileForm(forms.ModelForm):
    nome = forms.CharField(max_length=30, label='Name')
    cognome = forms.CharField(max_length=30, label='Surname')

    luogo_nascita_straniero = forms.CharField(max_length=100, label='Birth place')

    residenza_via = forms.CharField(max_length=100, label='Street')
    residenza_n = forms.CharField(max_length=20, label='Street number')
    residenza_comune = forms.CharField(max_length=100, label='Municipality')
    residenza_provincia = forms.CharField(max_length=100, label='Province')

    domicilio_via = forms.CharField(max_length=100, label='Street')
    domicilio_n = forms.CharField(max_length=20, label='Street number')
    domicilio_comune = forms.CharField(max_length=100, label='Municipality')
    domicilio_provincia = forms.CharField(max_length=100, label='Province')

    class Meta:
        model = Profile

        exclude = ['user', 'residenza', 'domicilio']
        widgets = {
            'data_nascita': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fine_rapporto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tutor': forms.TextInput(attrs={'placeholder': 'Prof/Prof.ssa'}),
            'anno_dottorato': forms.NumberInput(attrs={'placeholder': '1, 2, 3'}),
            # 'luogo_nascita': autocomplete.ModelSelect2(url='comune-autocomplete',
            #                                           attrs={'data-html': True, 'data-theme': 'bootstrap4', }),
        }
        labels = {
            'nome': 'Name',
            'cognome': 'Surname',
            'data_nascita': 'Birth Date',
            'datore_lavoro': 'Employer',
            'tutor': 'Tutor name and surname',
            'anno_dottorato': 'Doctorate year',
            'scuola_dottorato': 'Name of the doctoral school',
            'telefono': 'Phone (internal number)',
            'data_fine_rapporto': 'Employment end date',
            'cf': 'CF',
            'luogo_nasciata': 'Birth Place',
            'sesso': 'Sex',
            'qualifica': 'Position',
        }

    def __init__(self, *args, **kwargs):
        super(ForeignProfileForm, self).__init__(*args, **kwargs)
        self.fields['nome'].initial = self.instance.user.first_name
        self.fields['cognome'].initial = self.instance.user.last_name
        self.fields['cf'].initial = self.instance.cf

        if self.instance.residenza is not None:
            self.fields['residenza_via'].initial = self.instance.residenza.via
            self.fields['residenza_n'].initial = self.instance.residenza.n
            self.fields['residenza_comune'].initial = self.instance.residenza.comune_straniero
            self.fields['residenza_provincia'].initial = self.instance.residenza.provincia_straniero

        if self.instance.domicilio is not None:
            self.fields['domicilio_via'].initial = self.instance.domicilio.via
            self.fields['domicilio_n'].initial = self.instance.domicilio.n
            self.fields['domicilio_comune'].initial = self.instance.domicilio.comune_straniero
            self.fields['domicilio_provincia'].initial = self.instance.domicilio.provincia_straniero

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'RimborsiApp:foreign_profile'
        self.helper.add_input(Submit('submit', 'Update'))

        self.helper.layout = Layout(
            Row(Column('nome', css_class="col-6"), Column('cognome', css_class="col-6")),
            Row(Column('data_nascita', css_class="col-3"), Column('luogo_nascita_straniero', css_class="col-3"),
                Column('cf', css_class="col-3"), Column('sesso', css_class="col-3")),
            Fieldset("Residence", Row(
                Column('residenza_via', css_class='col-4'),
                Column('residenza_n', css_class='col-2'),
                Column('residenza_comune', css_class='col-3'),
                Column('residenza_provincia', css_class='col-3'), css_id='residenza-row')),

            Fieldset("Domicile", Row(
                Column('domicilio_via', css_class='col-4'),
                Column('domicilio_n', css_class='col-2'),
                Column('domicilio_comune', css_class='col-3'),
                Column('domicilio_provincia', css_class='col-3'), css_id='domicilio-row'), css_id='domicilio-fieldset'),

            Fieldset("Working position",
                     Row(
                         Column('qualifica', css_class="col-6"),
                         Column('datore_lavoro', css_class="col-6")),
                     Row(Column('telefono', css_class="col-6"),
                         Column('data_fine_rapporto', css_class="col-6")),
                     Row(Column('tutor', css_class="col-4"),
                         Column('anno_dottorato', css_class="col-2"),
                         Column('scuola_dottorato', css_class="col-6"), css_id="dottorando-details"),
                     )
        )

    def save(self, commit=True):
        self.straniero = True
        super(ForeignProfileForm, self).save(commit)
        self.instance.user.first_name = self.cleaned_data.get('nome')
        self.instance.user.last_name = self.cleaned_data.get('cognome')
        if commit:
            self.instance.user.save()
        return self.instance


class ProfileForm(forms.ModelForm):
    # cf = forms.CharField(max_length=16, disabled=True, label='CF', required=False)
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
            'data_fine_rapporto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
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
            'telefono': 'Telefono (interno)',
            'data_fine_rapporto': 'Data di fine rapporto (se contratto a tempo determinato)',
            'cf': 'CF',
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
        self.helper.form_action = 'RimborsiApp:italian_profile'
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

            Fieldset("Posizione lavorativa",
                     Row(
                         Column('qualifica', css_class="col-6"),
                         Column('datore_lavoro', css_class="col-6")),
                     Row(Column('telefono', css_class="col-6"),
                         Column('data_fine_rapporto', css_class="col-6")),
                     Row(Column('tutor', css_class="col-4"),
                         Column('anno_dottorato', css_class="col-2"),
                         Column('scuola_dottorato', css_class="col-6"), css_id="dottorando-details"),
                     )
        )

    def save(self, commit=True):
        self.straniero = False
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
            'tipo': 'Tipologia di missione <a tabindex="0" class="popover-dismiss" role="button" data-toggle="popover" \
               data-trigger="focus" title="Tipologia di missione" \
               data-content="La tipologia missione serve per distinguere missioni di pura ricerca da missioni di \
               progetto, ovvero missioni correlate ad un progetto di ricerca. Il campo è obbligatorio!"> \
               <i class="fa fa-info-circle fa-1x" aria-hidden="true"></i></a>',
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
            Row(Div('fondo', css_class="col-3"), Div('struttura_fondi', css_class="col-3"),
                Div('tipo', css_class="col-3"), Div('anticipo', css_class="col-3")),
            Row(Div('motivazione', css_class="col-12")),
            Row(Div(InlineCheckboxes('mezzi_previsti'), css_class="col-6"), Div('automobile', css_class="col-6"),
                Div('automobile_altrui', css_class="col-6")),
            Row(Div(InlineCheckboxes('motivazione_automobile'), css_class="col-12")),
        )


# Pasti
class ScontrinoForm(forms.Form):
    data = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}))
    desc_label = 'Descrizione (numero fattura/ricevuta fiscale)'
    s1 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', }))
    v1 = forms.ChoiceField(initial="EUR", choices=VALUTA_CHOICES, required=False, label='Valuta',
                           widget=forms.Select(
                               attrs={'class': 'form-control form-control-sm', 'style': 'min-width: 55px;'}))
    d1 = forms.CharField(required=False, label=desc_label,
                         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))

    s2 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', }))
    v2 = forms.ChoiceField(initial="EUR", choices=VALUTA_CHOICES, required=False, label='Valuta',
                           widget=forms.Select(
                               attrs={'class': 'form-control form-control-sm', 'style': 'min-width: 55px;'}))
    d2 = forms.CharField(required=False, label=desc_label,
                         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))

    s3 = forms.DecimalField(decimal_places=2, label='Spesa', required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', }))
    v3 = forms.ChoiceField(initial="EUR", choices=VALUTA_CHOICES, required=False, label='Valuta',
                           widget=forms.Select(
                               attrs={'class': 'form-control form-control-sm', 'style': 'min-width: 55px;'}))
    d3 = forms.CharField(required=False, label=desc_label,
                         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))

    # def __init__(self, *args, **kwargs):
    #     super(ScontrinoForm, self).__init__(*args, **kwargs)
    #     self.initial['v1'] = 'EUR'
    #     self.initial['v2'] = 'EUR'
    #     self.initial['v3'] = 'EUR'


# Pernottamenti, iscrizione convegni, altre spese
class ScontrinoExtraForm(forms.Form):
    data = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control form-control-sm', 'required': 'required', }))
    desc_label = 'Descrizione (numero fattura/ricevuta fiscale)'
    s1 = forms.DecimalField(decimal_places=2, label='Spesa', required=True,
                            widget=forms.NumberInput(attrs={'class': 'form-control form-control-sm', }))
    v1 = forms.ChoiceField(initial="EUR", choices=VALUTA_CHOICES, required=False, label='Valuta',
                           widget=forms.Select(
                               attrs={'class': 'form-control form-control-sm', 'style': 'min-width: 55px;'}))
    d1 = forms.CharField(required=False, label=desc_label,
                         widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }), )


class TrasportoForm(forms.ModelForm):
    class Meta:
        model = Trasporto
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control form-control-sm', 'required': 'required', }),
            'da': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'a': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'mezzo': forms.Select(attrs={'class': 'form-control form-control-sm', 'required': 'required', }),
            'tipo_costo': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'costo': forms.NumberInput(
                attrs={'class': 'form-control form-control-sm', 'step': 0.01, 'required': 'required', }),
            # 'valuta': forms.Select(
            #     attrs={'class': 'form-control trasporti-costo', 'required': 'required', }),
            'valuta': forms.Select(attrs={'class': 'form-control form-control-sm', 'style': 'min-width: 55px;'}),
            'km': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'step': 0.01}),
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
            'marca': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'modello': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
            'targa': forms.TextInput(attrs={'class': 'form-control form-control-sm', }),
        }


class ModuliMissioneForm(forms.ModelForm):
    dichiarazione_check_std = forms.BooleanField(label='Dichiarazione precompilata di partecipazione evento',
                                                 required=False, initial=True)
    dichiarazione_check_pers = forms.BooleanField(label='Dichiarazione personalizzata:', required=False)

    class Meta:
        model = ModuliMissione
        fields = '__all__'
        exclude = ['missione', 'parte_1_file', 'parte_2_file', 'kasko_file', 'dottorandi_file', 'anticipo_file']
        widgets = {
            'anticipo': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }, ),
            'parte_1': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }, ),
            'parte_2': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }),
            'kasko': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }),
            'dottorandi': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }),
            'atto_notorio': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date', }),
            'atto_notorio_dichiarazione': forms.Textarea(attrs={'rows': 4, 'readonly': 'readonly'})
        }
        labels = {
            'anticipo': 'Data Richiesta',
            'parte_1': 'Data Richiesta',
            'parte_2': 'Data Richiesta',
            'kasko': 'Data Richiesta',
            'dottorandi': 'Data Richiesta',
            'atto_notorio': 'Data Richiesta',
            'atto_notorio_dichiarazione': '',
        }

    def clean(self):
        cleaned_data = super(ModuliMissioneForm, self).clean()
        missione_inizio = self.instance.missione.inizio
        missione_fine = self.instance.missione.fine
        anticipo_data = cleaned_data.get("anticipo")
        parte_1_data = cleaned_data.get("parte_1")
        parte_2_data = cleaned_data.get("parte_2")
        atto_notorio_data = cleaned_data.get("atto_notorio")
        dottorandi_data = cleaned_data.get("dottorandi")
        kasko_data = cleaned_data.get("kasko")

        errors = {}

        if anticipo_data is None:
            errors['anticipo'] = f"Inserisci una data"

        if anticipo_data.weekday() >= 5:
            errors['anticipo'] = \
                f"Anticipo deve avere una data di compilazione che non sia sabato o domenica"

        if anticipo_data - missione_inizio > datetime.timedelta(days=12):
            errors['anticipo'] = \
                f"Anticipo deve avere una data di compilazione di almeno dieci giorni lavorativi antecedenti l'inizio della missione ({missione_inizio.strftime('%d/%m/%Y')})"

        if atto_notorio_data is None:
            errors['atto_notorio'] = f"Inserisci una data"

        if atto_notorio_data.weekday() >= 5:
            errors['atto_notorio'] = \
                f"Atto notorio deve avere una data di compilazione che non sia sabato o domenica"

        if parte_2_data is None:
            errors['parte_2'] = f"Inserisci una data"

        if parte_2_data.weekday() >= 5:
            errors['parte_2'] = \
                f"Missione parte II deve avere una data di compilazione che non sia sabato o domenica"

        if parte_1_data is None:
            errors['parte_1'] = f"Inserisci una data"

        if parte_1_data.weekday() >= 5:
            errors['parte_1'] = f"Missione parte I deve avere una data di compilazione che non sia sabato o domenica"

        if self.instance.missione.user.profile.qualifica == 'DOTTORANDO':
            if dottorandi_data is None:
                errors['dottorandi'] = f"Inserisci una data"
            elif dottorandi_data.weekday() >= 5:
                errors['dottorandi'] = \
                    f"Autorizzazione dottorandi deve avere una data di compilazione che non sia sabato o domenica"

        if kasko_data is None:
            errors['kasko'] = f"Inserisci una data"

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

        if self.instance.missione.user.profile.qualifica == 'DOTTORANDO':
            if dottorandi_data is None:
                errors['dottorandi'] = f"Inserisci una data"
            elif dottorandi_data > missione_inizio:
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
        self.helper.form_tag = False

        if self.instance.atto_notorio_dichiarazione != '':
            self.fields['dichiarazione_check_pers'].initial = True
            del self.fields['atto_notorio_dichiarazione'].widget.attrs['readonly']  # Enable the textarea


automobile_formset = inlineformset_factory(User, Automobile, AutomobileForm, extra=0, can_delete=True,
                                           exclude=('user',), min_num=1)
trasporto_formset = inlineformset_factory(Missione, Trasporto, TrasportoForm, extra=0, can_delete=True,
                                          fields='__all__', min_num=1)
scontrino_formset = formset_factory(ScontrinoForm, extra=0)
scontrino_extra_formset = formset_factory(ScontrinoExtraForm, can_delete=True, extra=0, min_num=1)
