from django.http import JsonResponse
from .alerts import *
from .models import Dht11
from .parameters import *

temperatureAndHumidityTargetIndex = 0


def verifySensorsValues():
    global temperatureAndHumidityTargetIndex
    dataBaseLastRow = Dht11.objects.last()
    temperature = dataBaseLastRow.temp
    humidity = dataBaseLastRow.hum
    if temperature > temperatureThreshold or humidity > humidityThreshold:
        message = 'ALERT : la temperature = ' + str(temperature) + "l'humidité = " + str(humidity)
        targetingBaseOnIndex(temperatureAndHumidityTargetIndex, message)
        temperatureAndHumidityTargetIndex += 1
        if temperatureAndHumidityTargetIndex == 16:
            temperatureAndHumidityTargetIndex = 15
    else:
        temperatureAndHumidityTargetIndex = 0
    return JsonResponse({'targetIndex': temperatureAndHumidityTargetIndex, 'Temperature': temperature})


def targetingBaseOnIndex(targetIndex, message):
    if targetIndex == 0:
        sms_alert(message, targetNumbersDic[0])
    if targetIndex in [0, 1, 2, 3]:
        email_alert(message, targetEmailsDic[0])
        telegram_alert(message, targetBotsDic[0])
        wtsp_alert(message, targetNumbersDic[0])
    elif targetIndex in [4, 5, 6, 7]:
        email_alert(message, targetEmailsDic[0])
        email_alert(message, targetEmailsDic[1])
        telegram_alert(message, targetBotsDic[0])
        telegram_alert(message, targetBotsDic[1])
        wtsp_alert(message, targetNumbersDic[0])
        wtsp_alert(message, targetNumbersDic[1])
    elif targetIndex in [8, 9, 10, 11]:
        for index in range(3):
            telegram_alert(message, targetBotsDic[index])
            email_alert(message, targetEmailsDic[index])
            wtsp_alert(message, targetNumbersDic[index])
    elif targetIndex in [12, 13, 14, 15]:
        for index in range(4):
            telegram_alert(message, targetBotsDic[index])
            email_alert(message, targetEmailsDic[index])
            wtsp_alert(message, targetNumbersDic[index])
