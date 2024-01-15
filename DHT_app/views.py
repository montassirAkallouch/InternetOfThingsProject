import csv
from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.utils import timezone
from .verifyDhtValues import *
from django.views.decorators.csrf import csrf_exempt
import json


def table(request):
    derniere_ligne = Dht11.objects.last()
    derniere_date = Dht11.objects.last().dt
    delta_temps = timezone.now() - derniere_date
    days = delta_temps.days
    seconds = delta_temps.seconds + days * 86400
    if seconds >= 60:
        minutes = seconds // 60
        seconds = seconds % 60
        if minutes >= 60:
            heures = minutes // 60
            minutes %= 60
            if heures >= 24:
                jours = heures // 24
                heures %= 24
                if jours == 1:
                    temps_ecoule = str(jours) + ' day ' + str(heures) + ' h ' + str(minutes) + ' min ' + str(
                        seconds) + ' sc' + ' ago'
                else:
                    temps_ecoule = str(jours) + ' days ' + str(heures) + ' h ' + str(minutes) + ' min ' + str(
                        seconds) + ' sc' + ' ago'
            else:
                temps_ecoule = str(heures) + ' h ' + str(minutes) + ' min ' + str(seconds) + ' sc ' + 'ago'
        else:
            temps_ecoule = str(minutes) + ' min ' + str(seconds) + ' sc' + ' ago'

    else:
        temps_ecoule = str(seconds) + ' sc' + ' ago'

    valeurs = {'date': temps_ecoule, 'id': derniere_ligne.id, 'temp': derniere_ligne.temp,
               'hum': derniere_ligne.hum}
    return render(request, 'value.html', {'valeurs': valeurs})


def download_csv(request):
    model_values = Dht11.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="dht.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'temp', 'hum', 'dt'])
    liste = model_values.values_list('id', 'temp', 'hum', 'dt')
    for row in liste:
        writer.writerow(row)
    return response


def index_view(request):
    return render(request, 'index.html')


def about_view(request):
    return render(request, 'about.html')


def notifications_view(request):
    data = Dht11.objects.all()
    corrupted_data = []
    for i in data:
        if i.hum > humidityThreshold or i.temp > temperatureThreshold:
            delta_temps = timezone.now() - i.dt
            days = delta_temps.days
            seconds = delta_temps.seconds + days * 86400
            if seconds >= 60:
                minutes = seconds // 60
                seconds = seconds % 60
                if minutes >= 60:
                    heures = minutes // 60
                    minutes %= 60
                    if heures >= 24:
                        jours = heures // 24
                        heures %= 24
                        if jours == 1:
                            temps_ecoule = str(jours) + ' day ' + ' ago'
                        else:
                            temps_ecoule = str(jours) + ' days ' + ' ago'
                    else:
                        temps_ecoule = str(heures) + ' h ' + str(minutes) + ' min ' + 'ago'
                else:
                    temps_ecoule = str(minutes) + ' min ' + ' ago'

            else:
                temps_ecoule = str(seconds) + ' sc' + ' ago'
            corrupted_data.append({'id': i.id, 'temp': i.temp, 'hum': i.hum, 'date': temps_ecoule})
        corrupted_data = corrupted_data[-5:]
    return render(request, 'notifications.html', {'valeurs': corrupted_data})


def graphique(request):
    return render(request, 'Chart.html')


def chart_data(request):
    dht = Dht11.objects.all()
    data = {
        'temps': [Dt.dt for Dt in dht],
        'temperature': [Temp.temp for Temp in dht],
        'humidity': [Hum.hum for Hum in dht],
        'CO2': [CO2.CO_2 for CO2 in dht]
    }
    return JsonResponse(data)


def chart_data_heure(request):
    now = timezone.now()
    dht = Dht11.objects.filter(dt__hour=now.time().hour, dt__day=now.date().day, dt__month=now.date().month,
                               dt__year=now.date().year)
    return JsonResponse(limitingPoints(dht))


def chart_data_jour(request):
    now = timezone.now().date()  # Assuming you want to filter by the current date
    dht = Dht11.objects.filter(dt__day=now.day, dt__month=now.month, dt__year=now.year)
    return JsonResponse(limitingPoints(dht))


def chart_data_mois(request):
    now = timezone.now().date()  # Assuming you want to filter by the current date
    dht = Dht11.objects.filter(dt__month=now.month, dt__year=now.year)
    return JsonResponse(limitingPoints(dht))


def limitingPoints(dht):
    temps = [Dt.dt for Dt in dht]
    temperatures = [Temp.temp for Temp in dht]
    humidities = [Hum.hum for Hum in dht]
    length = len(temps)
    print(length)
    if length >= 30:
        samplesRate = length // 30
        print(samplesRate)
        temps = temps[::samplesRate]
        print(len(temps))
        humidities = humidities[::samplesRate]
        print(len(humidities))
        temperatures = temperatures[::samplesRate]
        print(len(temperatures))
    return {
        'temps': temps,
        'temperature': temperatures,
        'humidity': humidities,
    }


@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            temperature = data['temperature']
            humidity = data['humidity']
            Dht11.objects.create(temp=temperature, hum=humidity)
            verifySensorsValues()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'})
