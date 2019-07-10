import datetime
import os

from codicefiscale import codicefiscale
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

MEZZO_CHOICES = (
    ("AUTO", "Auto"),
    ("AEREO", "Aereo"),
    ("TRENO", "Treno"),
    ("BUS", "Bus"),
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
    motivazione = models.CharField(max_length=100, null=True, blank=True)
    struttura_fondi = models.CharField(max_length=200)
    automobile = models.ForeignKey(Automobile, null=True, blank=True, on_delete=models.SET_NULL)
    scontrino = models.TextField(null=True, blank=True)
    pernottamento = models.TextField(null=True, blank=True)
    convegno = models.TextField(null=True, blank=True)
    altrespese = models.TextField(null=True, blank=True)

    mezzi_previsti = models.CharField(max_length=100, null=True, blank=True)
    motivazione_automobile = models.CharField(max_length=200, null=True, blank=True)

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
    da = models.CharField(max_length=100)
    a = models.CharField(max_length=100)
    mezzo = models.CharField(max_length=5, choices=MEZZO_CHOICES)
    tipo_costo = models.CharField(max_length=50)
    costo = models.FloatField()
    km = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Trasporti"


class Comune(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Comuni"


class Profile(models.Model):
    PROVINCIA_CHOICES = (
        ('AG', 'Agrigento'),
        ('AL', 'Alessandria'),
        ('AN', 'Ancona'),
        ('AO', 'Aosta'),
        ('AR', 'Arezzo'),
        ('AP', 'Ascoli Piceno'),
        ('AT', 'Asti'),
        ('AV', 'Avellino'),
        ('BA', 'Bari'),
        ('BT', 'Barletta-Andria-Trani'),
        ('BL', 'Belluno'),
        ('BN', 'Benevento'),
        ('BG', 'Bergamo'),
        ('BI', 'Biella'),
        ('BO', 'Bologna'),
        ('BZ', 'Bolzano/Bozen'),
        ('BS', 'Brescia'),
        ('BR', 'Brindisi'),
        ('CA', 'Cagliari'),
        ('CL', 'Caltanissetta'),
        ('CB', 'Campobasso'),
        ('CI', 'Carbonia-Iglesias'),
        ('CE', 'Caserta'),
        ('CT', 'Catania'),
        ('CZ', 'Catanzaro'),
        ('CH', 'Chieti'),
        ('CO', 'Como'),
        ('CS', 'Cosenza'),
        ('CR', 'Cremona'),
        ('KR', 'Crotone'),
        ('CN', 'Cuneo'),
        ('EN', 'Enna'),
        ('FM', 'Fermo'),
        ('FE', 'Ferrara'),
        ('FI', 'Firenze'),
        ('FG', 'Foggia'),
        ('FC', 'Forli-Cesena'),
        ('FR', 'Frosinone'),
        ('GE', 'Genova'),
        ('GO', 'Gorizia'),
        ('GR', 'Grosseto'),
        ('IM', 'Imperia'),
        ('IS', 'Isernia'),
        ('SP', 'La Spezia'),
        ('AQ', 'L\'Aquila'),
        ('LT', 'Latina'),
        ('LE', 'Lecce'),
        ('LC', 'Lecco'),
        ('LI', 'Livorno'),
        ('LO', 'Lodi'),
        ('LU', 'Lucca'),
        ('MC', 'Macerata'),
        ('MN', 'Mantova'),
        ('MS', 'Massa-Carrara'),
        ('MT', 'Matera'),
        ('VS', 'Medio Campidano'),
        ('ME', 'Messina'),
        ('MI', 'Milano'),
        ('MO', 'Modena'),
        ('MB', 'Monza e della Brianza'),
        ('NA', 'Napoli'),
        ('NO', 'Novara'),
        ('NU', 'Nuoro'),
        ('OG', 'Ogliastra'),
        ('OT', 'Olbia-Tempio'),
        ('OR', 'Oristano'),
        ('PD', 'Padova'),
        ('PA', 'Palermo'),
        ('PR', 'Parma'),
        ('PV', 'Pavia'),
        ('PG', 'Perugia'),
        ('PU', 'Pesaro e Urbino'),
        ('PE', 'Pescara'),
        ('PC', 'Piacenza'),
        ('PI', 'Pisa'),
        ('PT', 'Pistoia'),
        ('PN', 'Pordenone'),
        ('PZ', 'Potenza'),
        ('PO', 'Prato'),
        ('RG', 'Ragusa'),
        ('RA', 'Ravenna'),
        ('RC', 'Reggio di Calabria'),
        ('RE', 'Reggio nell\'Emilia'),
        ('RI', 'Rieti'),
        ('RN', 'Rimini'),
        ('RM', 'Roma'),
        ('RO', 'Rovigo'),
        ('SA', 'Salerno'),
        ('SS', 'Sassari'),
        ('SV', 'Savona'),
        ('SI', 'Siena'),
        ('SR', 'Siracusa'),
        ('SO', 'Sondrio'),
        ('TA', 'Taranto'),
        ('TE', 'Teramo'),
        ('TR', 'Terni'),
        ('TO', 'Torino'),
        ('TP', 'Trapani'),
        ('TN', 'Trento'),
        ('TV', 'Treviso'),
        ('TS', 'Trieste'),
        ('UD', 'Udine'),
        ('VA', 'Varese'),
        ('VE', 'Venezia'),
        ('VB', 'Verbano-Cusio-Ossola'),
        ('VC', 'Vercelli'),
        ('VR', 'Verona'),
        ('VV', 'Vibo Valentia'),
        ('VI', 'Vicenza'),
        ('VT', 'Viterbo'),
    )
    QUALIFICA_CHOICES = (
        ('DOTTORANDO', 'Dottorando'),
        ('ASSEGNISTA', 'Assegnista'),
        ('STUDENTE', 'Studente'),
        ('DOCENTE', 'Docente'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data_nascita = models.DateField(null=True)
    luogo_nascita = models.ForeignKey(Comune, on_delete=models.SET_NULL, null=True)
    sesso = models.CharField(max_length=1, choices=(('M', 'Maschio'), ('F', 'Femmina')), null=True)
    domicilio_fiscale = models.CharField(max_length=300, null=True)
    domicilio_fiscale_provincia = models.CharField(max_length=2, choices=PROVINCIA_CHOICES, null=True)
    qualifica = models.CharField(max_length=10, choices=QUALIFICA_CHOICES, null=True)
    datore_lavoro = models.CharField(max_length=100, blank=True, null=True)

    @property
    def cf(self):
        if self.data_nascita is None:
            return ''
        date = str(self.data_nascita)
        cf = codicefiscale.encode(surname=self.user.last_name, name=self.user.first_name, sex=self.sesso,
                                  birthdate=date,
                                  birthplace=str(self.luogo_nascita))
        return cf

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
    dottorandi = models.DateField()

    parte_1_file = models.FileField(upload_to='moduli/', null=True, blank=True)
    parte_2_file = models.FileField(upload_to='moduli/', null=True, blank=True)
    kasko_file = models.FileField(upload_to='moduli/', null=True, blank=True)
    dottorandi_file = models.FileField(upload_to='moduli/', null=True, blank=True)

    class Meta:
        verbose_name = "Moduli missione"
        verbose_name_plural = "Moduli missioni"
