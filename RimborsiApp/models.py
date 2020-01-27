import datetime

from codicefiscale import codicefiscale
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from RimborsiApp.storage import OverwriteStorage

from django.core.files.storage import FileSystemStorage
from Rimborsi import settings

VALUTA_CHOICES = (
    ("AED", "AED"),
    ("AFN", "AFN"),
    ("ALL", "ALL"),
    ("AMD", "AMD"),
    ("ANG", "ANG"),
    ("AOA", "AOA"),
    ("ARS", "ARS"),
    ("AUD", "AUD"),
    ("AWG", "AWG"),
    ("AZN", "AZN"),
    ("BAM", "BAM"),
    ("BBD", "BBD"),
    ("BDT", "BDT"),
    ("BGN", "BGN"),
    ("BHD", "BHD"),
    ("BIF", "BIF"),
    ("BMD", "BMD"),
    ("BND", "BND"),
    ("BOB", "BOB"),
    ("BRL", "BRL"),
    ("BSD", "BSD"),
    ("BTN", "BTN"),
    ("BWP", "BWP"),
    ("BYN", "BYN"),
    ("BZD", "BZD"),
    ("CAD", "CAD"),
    ("CDF", "CDF"),
    ("CHF", "CHF"),
    ("CLP", "CLP"),
    ("CNY", "CNY"),
    ("COP", "COP"),
    ("CRC", "CRC"),
    ("CUC", "CUC"),
    ("CUP", "CUP"),
    ("CVE", "CVE"),
    ("CZK", "CZK"),
    ("DJF", "DJF"),
    ("DKK", "DKK"),
    ("DOP", "DOP"),
    ("DZD", "DZD"),
    ("EGP", "EGP"),
    ("ERN", "ERN"),
    ("ETB", "ETB"),
    ("EUR", "EUR"),
    ("FJD", "FJD"),
    ("FKP", "FKP"),
    ("GBP", "GBP"),
    ("GEL", "GEL"),
    ("GGP", "GGP"),
    ("GHS", "GHS"),
    ("GIP", "GIP"),
    ("GMD", "GMD"),
    ("GNF", "GNF"),
    ("GTQ", "GTQ"),
    ("GYD", "GYD"),
    ("HKD", "HKD"),
    ("HNL", "HNL"),
    ("HRK", "HRK"),
    ("HTG", "HTG"),
    ("HUF", "HUF"),
    ("IDR", "IDR"),
    ("ILS", "ILS"),
    ("IMP", "IMP"),
    ("INR", "INR"),
    ("IQD", "IQD"),
    ("IRR", "IRR"),
    ("ISK", "ISK"),
    ("JEP", "JEP"),
    ("JMD", "JMD"),
    ("JOD", "JOD"),
    ("JPY", "JPY"),
    ("KES", "KES"),
    ("KGS", "KGS"),
    ("KHR", "KHR"),
    ("KMF", "KMF"),
    ("KPW", "KPW"),
    ("KRW", "KRW"),
    ("KWD", "KWD"),
    ("KYD", "KYD"),
    ("KZT", "KZT"),
    ("LAK", "LAK"),
    ("LBP", "LBP"),
    ("LKR", "LKR"),
    ("LRD", "LRD"),
    ("LSL", "LSL"),
    ("LYD", "LYD"),
    ("MAD", "MAD"),
    ("MDL", "MDL"),
    ("MGA", "MGA"),
    ("MKD", "MKD"),
    ("MMK", "MMK"),
    ("MNT", "MNT"),
    ("MOP", "MOP"),
    ("MRU", "MRU"),
    ("MUR", "MUR"),
    ("MVR", "MVR"),
    ("MWK", "MWK"),
    ("MXN", "MXN"),
    ("MYR", "MYR"),
    ("MZN", "MZN"),
    ("NAD", "NAD"),
    ("NGN", "NGN"),
    ("NIO", "NIO"),
    ("NOK", "NOK"),
    ("NPR", "NPR"),
    ("NZD", "NZD"),
    ("OMR", "OMR"),
    ("PAB", "PAB"),
    ("PEN", "PEN"),
    ("PGK", "PGK"),
    ("PHP", "PHP"),
    ("PKR", "PKR"),
    ("PLN", "PLN"),
    ("PYG", "PYG"),
    ("QAR", "QAR"),
    ("RON", "RON"),
    ("RSD", "RSD"),
    ("RUB", "RUB"),
    ("RWF", "RWF"),
    ("SAR", "SAR"),
    ("SBD", "SBD"),
    ("SCR", "SCR"),
    ("SDG", "SDG"),
    ("SEK", "SEK"),
    ("SGD", "SGD"),
    ("SHP", "SHP"),
    ("SLL", "SLL"),
    ("SOS", "SOS"),
    ("SPL*", "SPL*"),
    ("SRD", "SRD"),
    ("STN", "STN"),
    ("SVC", "SVC"),
    ("SYP", "SYP"),
    ("SZL", "SZL"),
    ("THB", "THB"),
    ("TJS", "TJS"),
    ("TMT", "TMT"),
    ("TND", "TND"),
    ("TOP", "TOP"),
    ("TRY", "TRY"),
    ("TTD", "TTD"),
    ("TVD", "TVD"),
    ("TWD", "TWD"),
    ("TZS", "TZS"),
    ("UAH", "UAH"),
    ("UGX", "UGX"),
    ("USD", "USD"),
    ("UYU", "UYU"),
    ("UZS", "UZS"),
    ("VEF", "VEF"),
    ("VND", "VND"),
    ("VUV", "VUV"),
    ("WST", "WST"),
    ("XAF", "XAF"),
    ("XCD", "XCD"),
    ("XDR", "XDR"),
    ("XOF", "XOF"),
    ("XPF", "XPF"),
    ("YER", "YER"),
    ("ZAR", "ZAR"),
    ("ZMW", "ZMW"),
    ("ZWD", "ZWD"),
)

MEZZO_CHOICES = (
    ("AUTO", "Auto"),
    ("A_ALT", "Auto altrui"),
    ("AEREO", "Aereo"),
    ("TRENO", "Treno"),
    ("BUS", "Bus"),
    ("TAXI", "Taxi"),
)

TIPO_MISSIONE_CHOICES = (
    ("RICERCA", "Missione di Ricerca/Didattica"),
    ("PROGETTO", "Missione di Progetto"),
)

MOTIVAZIONE_AUTO_CHOICES = (
    ("Convenienza economica", "Convenienza economica (da dimostrare)"),
    ("Destinazione non servita da mezzi pubblici", "Destinazione non servita da mezzi pubblici"),
    ("Servizio pubblico particolarmente disagiato", "Servizio pubblico particolarmente disagiato"),
    ("Orari inconciliabili con i tempi della missione", "Orari inconciliabili con i tempi della missione"),
    ("Trasporto di materiali e/o strumenti", "Trasporto di materiali e/o strumenti"),
    ("Orari inconciliabili con necessità di rientro in sede", "Orari inconciliabili con necessità di rientro in sede"),
    # (7, "Vuoto"),
)


class Automobile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modello = models.CharField(max_length=100)
    targa = models.CharField(max_length=8)

    def __str__(self):
        return self.marca + ' ' + self.modello + ' ' + self.targa

    class Meta:
        verbose_name_plural = "Automobili"


class Categoria(models.Model):
    nome = models.CharField(max_length=1)
    massimale_docenti = models.FloatField()
    massimale_tecnici = models.FloatField()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorie"


class Stato(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Stati"


class Missione(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citta_destinazione = models.CharField(max_length=100)
    stato_destinazione = models.ForeignKey(Stato, on_delete=models.SET_NULL, null=True)
    inizio = models.DateField()
    inizio_ora = models.TimeField()
    fine = models.DateField()
    fine_ora = models.TimeField()
    fondo = models.CharField(max_length=100)
    motivazione = models.CharField(max_length=100)
    struttura_fondi = models.CharField(max_length=200)
    automobile = models.ForeignKey(Automobile, null=True, blank=True, on_delete=models.SET_NULL)
    automobile_altrui = models.CharField(max_length=100, null=True, blank=True)
    tipo = models.CharField(max_length=8, choices=TIPO_MISSIONE_CHOICES, null=True)

    scontrino = models.TextField(null=True, blank=True)
    pernottamento = models.TextField(null=True, blank=True)
    convegno = models.TextField(null=True, blank=True)
    altrespese = models.TextField(null=True, blank=True)

    mezzi_previsti = models.CharField(max_length=100, null=True, blank=True)
    motivazione_automobile = models.CharField(max_length=200, null=True, blank=True)

    missione_conclusa = models.BooleanField(default=False, blank=True)
    @property
    def durata_gg(self):
        return self.fine - self.inizio + datetime.timedelta(days=1)

    @property
    def data_richiesta(self):
        if datetime.date.today() < self.inizio:
            return datetime.date.today()
        else:
            return self.inizio - datetime.timedelta(days=1)

    class Meta:
        verbose_name_plural = "Missioni"

    def __str__(self):
        return f'{self.inizio} - {self.stato_destinazione} - {self.citta_destinazione}'


class Trasporto(models.Model):
    missione = models.ForeignKey(Missione, on_delete=models.CASCADE)
    data = models.DateField()
    da = models.CharField(max_length=100, null=True, blank=True)
    a = models.CharField(max_length=100, null=True, blank=True)
    mezzo = models.CharField(max_length=5, choices=MEZZO_CHOICES)
    tipo_costo = models.CharField(max_length=50, null=True, blank=True)
    costo = models.FloatField()
    valuta = models.CharField(max_length=3, choices=VALUTA_CHOICES, default="EUR")
    km = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Trasporti"


class Indirizzo(models.Model):
    via = models.CharField(max_length=100)
    n = models.CharField(max_length=20)
    comune = models.ForeignKey('comuni_italiani.Comune', on_delete=models.PROTECT, null=True)
    provincia = models.ForeignKey('comuni_italiani.Provincia', on_delete=models.PROTECT, null=True)
    comune_straniero = models.CharField(max_length=100, null=True)
    provincia_straniero = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.via} {self.n}, {self.comune.name}, {self.provincia.name} ({self.provincia.codice_targa})'

    class Meta:
        verbose_name_plural = "Indirizzi"


class Profile(models.Model):
    QUALIFICA_CHOICES = (
        ('DOTTORANDO', 'Dottorando'),
        ('ASSEGNISTA', 'Assegnista'),
        ('STUDENTE', 'Studente'),
        ('PO', 'Professore Ordinario'),
        ('PA', 'Professore Associato'),
        ('RU', 'Ric. Universitario'),
        ('RTDA', 'RTDA'),
        ('RTDB', 'RTDB'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascita = models.DateField(null=True)
    luogo_nascita = models.ForeignKey('comuni_italiani.Comune', on_delete=models.PROTECT, null=True, blank=True)

    luogo_nascita_straniero = models.CharField(max_length=100, null=True, default=None, blank=True)

    straniero = models.BooleanField(null=False, default=False)

    sesso = models.CharField(max_length=1, choices=(('M', 'Maschio'), ('F', 'Femmina')), null=True)
    qualifica = models.CharField(max_length=10, choices=QUALIFICA_CHOICES, null=True)
    datore_lavoro = models.CharField(max_length=100, blank=True, null=True)

    residenza = models.OneToOneField(Indirizzo, on_delete=models.SET_NULL, related_name='residenza', null=True, blank=True)
    domicilio = models.OneToOneField(Indirizzo, on_delete=models.SET_NULL, related_name='domicilio', null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=False, null=True)
    data_fine_rapporto = models.DateField(null=True, blank=True)
    cf = models.CharField(max_length=16, default='')

    # @property
    # def cf(self):
    #     if self.data_nascita is None:
    #         return ''
    #     date = str(self.data_nascita)
    #     if self.luogo_nascita is None or self.sesso is None:
    #         return ''
    #     try:
    #         cf = codicefiscale.encode(surname=self.user.last_name, name=self.user.first_name, sex=self.sesso,
    #                               birthdate=date,
    #                               birthplace=self.luogo_nascita.name)
    #     except:
    #         cf = ''
    #
    #     return cf

    # Campi per dottorando
    tutor = models.CharField(max_length=100, null=True, blank=True)
    anno_dottorato = models.IntegerField(null=True, blank=True)
    scuola_dottorato = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Profili"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ModuliMissione(models.Model):
    missione = models.OneToOneField(Missione, on_delete=models.CASCADE)

    parte_1 = models.DateField()
    parte_2 = models.DateField()
    kasko = models.DateField()
    atto_notorio = models.DateField()
    dottorandi = models.DateField(null=True, blank=True)

    parte_1_file = models.FileField(upload_to='moduli/', storage=OverwriteStorage(), null=True, blank=True)
    parte_2_file = models.FileField(upload_to='moduli/', storage=OverwriteStorage(), null=True, blank=True)
    kasko_file = models.FileField(upload_to='moduli/', storage=OverwriteStorage(), null=True, blank=True)
    atto_notorio_file = models.FileField(upload_to='moduli/', storage=OverwriteStorage(), null=True, blank=True)
    dottorandi_file = models.FileField(upload_to='moduli/', storage=OverwriteStorage(), null=True, blank=True)

    atto_notorio_dichiarazione = models.TextField(null=True, blank=True)

    def is_user_allowed(self, user):
        return self.missione.user == user

    class Meta:
        verbose_name = "Moduli missione"
        verbose_name_plural = "Moduli missioni"
