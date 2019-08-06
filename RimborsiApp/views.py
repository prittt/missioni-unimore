import decimal
import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum
from django.http import Http404, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.core.mail import send_mail
from .forms import *
from .models import *
from .utils import *
from Rimborsi import settings


def home(request):
    if request.user.is_authenticated:
        missioni_passate = Missione.objects.filter(user=request.user).order_by('-inizio')
        return render(request, 'Rimborsi/index.html', {'missioni_passate': missioni_passate})
    else:
        return render(request, 'Rimborsi/index.html')


def load_json(missione, field_name):
    field_value = getattr(missione, field_name)
    if isinstance(field_value, str) and field_value != '':
        db_field = json.loads(field_value, parse_float=decimal.Decimal)
        for d in db_field:
            d['data'] = datetime.datetime.strptime(d['data'], '%Y-%m-%d').date()
    else:
        db_field = []
    return db_field


def resoconto_data(missione):
    db_dict = {
        'scontrino': ['s1', 's2', 's3', ],
        'pernottamento': ['s1'],
        'convegno': ['s1'],
        'altrespese': ['s1'],
    }

    totali = {
        'scontrino': 0.,
        'pernottamento': 0.,
        'convegno': 0.,
        'altrespese': 0.,
        'trasporto': 0,

        'totale': 0.,
        'totale_indennita': 0.,
    }

    # Sommo le spese per questa missione
    for k, sub_dict in db_dict.items():
        tmp = load_json(missione, k)
        for entry in tmp:
            for sub_k in sub_dict:
                totali[k] += float(entry[sub_k] or 0.)

    # Aggiungo il trasporto
    totali['trasporto'] = float(missione.trasporto_set.all().aggregate(Sum('costo'))['costo__sum'] or 0.)
    totali['totale'] = sum(totali.values())

    # Recupero il totale dei km in auto
    km = float(missione.trasporto_set.filter(mezzo='AUTO').aggregate(Sum('km'))['km__sum'] or 0.)
    prezzo = get_prezzo_carburante()
    indennita = float(prezzo / 5 * km)

    totali['totale_indennita'] = totali['totale'] + indennita

    return km, indennita, totali


@login_required
def resoconto(request, id):
    if request.method == 'GET':
        missione = get_object_or_404(Missione, pk=id, user=request.user)

        try:
            moduli_missione = ModuliMissione.objects.get(missione=missione)
        except ObjectDoesNotExist:
            today = datetime.date.today()
            parte_1 = today - datetime.timedelta(days=(today.weekday() // 4) * (today.weekday() % 4))
            if missione.inizio - parte_1 <= datetime.timedelta(days=0):
                parte_1 = missione.inizio - datetime.timedelta(days=1)
                parte_1 -= datetime.timedelta(days=(parte_1.weekday() // 4) * (parte_1.weekday() % 4))

            parte_2 = today + datetime.timedelta(days=(today.weekday() // 4) * (today.weekday() % 2 + 1))
            if missione.fine - parte_2 >= datetime.timedelta(days=0):
                parte_2 = missione.fine + datetime.timedelta(days=1)
                parte_2 += datetime.timedelta(days=(parte_2.weekday() // 4) * (parte_2.weekday() % 2 + 1))

            moduli_missione = ModuliMissione.objects.create(missione=missione, parte_1=parte_1, parte_2=parte_2,
                                                            kasko=parte_1, dottorandi=parte_1, atto_notorio=parte_2)

        moduli_missione_form = ModuliMissioneForm(instance=moduli_missione)

        km, indennita, totali = resoconto_data(missione)

        return render(request, 'Rimborsi/resoconto.html', {'missione': missione,
                                                           'moduli_missione_form': moduli_missione_form,
                                                           'km': km,
                                                           'indennita': indennita,
                                                           'totali': totali,
                                                           })
        # else:
        #     return render(request, 'Rimborsi/resoconto.html')


@login_required
def profile(request):
    profile = Profile.objects.get(id=request.user.profile.id)
    if request.method == 'GET':
        profile_form = ProfileForm(instance=profile)
        automobili = Automobile.objects.filter(user=request.user)

        afs = automobile_formset(instance=request.user, queryset=automobili)
        return render(request, 'Rimborsi/profile.html', {'profile_form': profile_form,
                                                         'automobili_formset': afs})
    elif request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            if profile.residenza is None:
                # Residenza mai creata
                residenza = Indirizzo()
            else:
                residenza = profile.residenza

            if profile.domicilio is None:
                # Domicilio mai creato
                domicilio = Indirizzo()
            else:
                domicilio = profile.domicilio
            residenza.via = profile_form.cleaned_data['residenza_via']
            residenza.n = profile_form.cleaned_data['residenza_n']
            residenza.comune = profile_form.cleaned_data['residenza_comune']
            residenza.provincia = profile_form.cleaned_data['residenza_provincia']
            residenza.save()
            domicilio.via = profile_form.cleaned_data['domicilio_via']
            domicilio.n = profile_form.cleaned_data['domicilio_n']
            domicilio.comune = profile_form.cleaned_data['domicilio_comune']
            domicilio.provincia = profile_form.cleaned_data['domicilio_provincia']
            domicilio.save()
            profile.residenza = residenza
            profile.domicilio = domicilio

            profile.save()
            return redirect('RimborsiApp:profile')
        else:
            return HttpResponseServerError()
    else:
        return HttpResponseBadRequest()


@login_required
def automobili(request):
    if request.method == 'POST':
        automobili = Automobile.objects.filter(user=request.user)
        afs = automobile_formset(request.POST, instance=request.user, queryset=automobili)
        if afs.is_valid():
            afs.save()
        return redirect('RimborsiApp:profile')
    else:
        return HttpResponseBadRequest()


@login_required
def crea_missione(request):
    if request.method == 'GET':
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        dayaftertomorrow = tomorrow + datetime.timedelta(days=1)
        missione_form = MissioneForm(user=request.user,
                                     initial={'user': request.user,
                                              'inizio': tomorrow,
                                              'fine': dayaftertomorrow,
                                              'inizio_ora': '09:00',
                                              'fine_ora': '09:00',
                                              })
        missione_form.helper.form_action = 'RimborsiApp:crea_missione'

        response = {'missione_form': missione_form}
        return render(request, 'Rimborsi/crea_missione.html', response)
    elif request.method == 'POST':
        missione_form = MissioneForm(request.user, request.POST)
        if missione_form.is_valid():
            missione = missione_form.save(commit=False)
            missione.user = request.user
            missione.automobile = missione_form.cleaned_data['automobile']
            # missione.mezzo = '+'.join(m for m in missione_form.cleaned_data['mezzo'])
            missione.save()
            return redirect('home')
        else:
            response = {'missione_form': missione_form}
            return render(request, 'Rimborsi/crea_missione.html', response)
    else:
        raise Http404


@login_required
def missione(request, id):
    def missione_response(missione):

        missione_form = MissioneForm(user=request.user, instance=missione,
                                     initial={'automobile': missione.automobile})
        missione_form.helper.form_action = reverse('RimborsiApp:missione', args=[id])

        db_dict = {
            'scontrino': [],  # pasti
            'pernottamento': [],
            'convegno': [],
            'altrespese': [],
        }

        # Load the default values for each field in db_dict
        for k, _ in db_dict.items():
            db_dict[k] = load_json(missione, k)

        # Create list of days for each meal
        giorni = (missione.fine - missione.inizio).days
        for current_date in (missione.inizio + datetime.timedelta(n) for n in range(giorni + 1)):
            if not list(filter(lambda d: d['data'] == current_date, db_dict['scontrino'])):
                db_dict['scontrino'].append({'data': current_date,
                                             's1': None, 'd1': None,
                                             's2': None, 'd2': None,
                                             's3': None, 'd3': None,
                                             })
        # Order by date and create the formset
        pasti_sorted = sorted(db_dict['scontrino'], key=lambda k: k['data'])
        pasti_formset = scontrino_formset(initial=pasti_sorted, prefix='pasti')

        pernottamenti_sorted = sorted(db_dict['pernottamento'], key=lambda k: k['data'])
        pernottamenti_formset = scontrino_extra_formset(initial=pernottamenti_sorted, prefix='pernottamenti')

        trasporti = Trasporto.objects.filter(missione=missione)
        trasporti_formset = trasporto_formset(instance=missione, queryset=trasporti.order_by('data'))

        convegni_sorted = sorted(db_dict['convegno'], key=lambda k: k['data'])
        convegni_formset = scontrino_extra_formset(initial=convegni_sorted, prefix='convegni')

        altrespese_sorted = sorted(db_dict['altrespese'], key=lambda k: k['data'])
        altrespese_formset = scontrino_extra_formset(initial=altrespese_sorted, prefix='altrespese')

        response = {
            'missione': missione,
            'missione_form': missione_form,
            'pasti_formset': pasti_formset,
            'trasporti_formset': trasporti_formset,
            'pernottamenti_formset': pernottamenti_formset,
            'convegni_formset': convegni_formset,
            'altrespese_formset': altrespese_formset,
        }
        return response

    try:
        missione = Missione.objects.get(user=request.user, id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'GET':
        response = missione_response(missione)
        return render(request, 'Rimborsi/missione.html', response)
    elif request.method == 'POST':
        # missione = Missione.objects.get(user=request.user, id=id)
        missione_form = MissioneForm(request.user, request.POST, instance=missione)
        # missione_form = MissioneForm(request.user, request.POST)
        if missione_form.is_valid():
            missione_form.save()
            return redirect('RimborsiApp:missione', id)
        else:
            response = missione_response(missione)
            response['missione_form'] = missione_form
            return render(request, 'Rimborsi/missione.html', response)
    else:
        raise Http404


@login_required
def salva_pasti(request, id):
    if request.method == 'POST':
        missione = Missione.objects.get(user=request.user, id=id)
        pasti_formset = scontrino_formset(request.POST, prefix='pasti')
        if pasti_formset.is_valid():
            pasti = [f.cleaned_data for f in pasti_formset.forms]
            missione.scontrino = json.dumps(pasti, cls=DjangoJSONEncoder)
            missione.save()
            return redirect('RimborsiApp:missione', id)
        else:
            return HttpResponseServerError('Form non valido')
    else:
        raise Http404


@login_required
def salva_pernottamenti(request, id):
    if request.method == 'POST':
        missione = Missione.objects.get(user=request.user, id=id)
        pernottamenti_formset = scontrino_extra_formset(request.POST, prefix='pernottamenti')
        if pernottamenti_formset.is_valid():
            pernottamenti = [f.cleaned_data for f in pernottamenti_formset.forms if f.cleaned_data != {}
                             and not f.cleaned_data['DELETE']]
            missione.pernottamento = json.dumps(pernottamenti, cls=DjangoJSONEncoder)
            missione.save()
            return redirect('RimborsiApp:missione', id)
        else:
            return HttpResponseServerError('Form non valido')
    else:
        raise Http404


@login_required
def salva_trasporti(request, id):
    if request.method == 'POST':
        missione = Missione.objects.get(id=id)
        trasporti_formset = trasporto_formset(request.POST, instance=missione)
        if trasporti_formset.is_valid():
            trasporti_formset.save()
            return redirect('RimborsiApp:missione', id)
        else:
            return HttpResponseServerError('Form non valido')
    else:
        return HttpResponseBadRequest()


@login_required
def salva_altrespese(request, id):
    if request.method == 'POST':
        missione = Missione.objects.get(user=request.user, id=id)
        altrespese_formset = scontrino_extra_formset(request.POST, prefix='altrespese')
        if altrespese_formset.is_valid():
            altrespese = [f.cleaned_data for f in altrespese_formset.forms if f.cleaned_data != {}
                          and not f.cleaned_data['DELETE']]
            missione.altrespese = json.dumps(altrespese, cls=DjangoJSONEncoder)
            missione.save()
            return redirect('RimborsiApp:missione', id)
        else:
            return HttpResponseServerError('Form non valido')
    else:
        raise Http404


@login_required
def salva_convegni(request, id):
    if request.method == 'POST':
        missione = Missione.objects.get(user=request.user, id=id)
        convegni_formset = scontrino_extra_formset(request.POST, prefix='convegni')
        if convegni_formset.is_valid():
            convegni = [f.cleaned_data for f in convegni_formset.forms if f.cleaned_data != {}
                        and not f.cleaned_data['DELETE']]
            missione.convegno = json.dumps(convegni, cls=DjangoJSONEncoder)
            missione.save()
            return redirect('RimborsiApp:missione', id)
        else:
            return HttpResponseServerError('Form non valido')
    else:
        raise Http404


@login_required
def cancella_missione(request, id):
    try:
        missione = Missione.objects.get(user=request.user, id=id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound()
    missione.delete()
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/registration.html', {'user_form': form})


def regolamento(request):
    if request.method == 'GET':
        return render(request, 'Rimborsi/regolamento.html')


@login_required
def invia_email_autorizzazione(request, id):
    if request.method == 'GET':
        return redirect('home')
    elif request.method == 'POST':
        data = request.POST
        emails = data.get('emails')
        text = data.get('textarea-email')

        emails = emails.split(' ')
        send_mail(
            'Autorizzazione missione',
            text,
            settings.EMAIL_HOST_USER,
            emails,
            fail_silently=False,
        )
        return redirect('RimborsiApp:resoconto', id)
