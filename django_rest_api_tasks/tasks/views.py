from django.shortcuts import render
from rest_framework.parsers import JSONParser # Importation qui permet d'analyser les données du client
from django.views.decorators.csrf import csrf_exempt # Importation qui permet d'éviter un jeton csrf 
from django.http import HttpResponse, JsonResponse # Importation qui permet d'envoyer la réponse du client
from .serializers import TaskSerializer # Importation qui permet de définir l'API pour la tâche
from .models import Task # Importation du model Task
# Create your views here.

@csrf_exempt 
def tasks(request): # Listes de tous les extraits de tâches
      if request.method == 'GET':
            # Récupère toutes les tâches
            tasks = Task.objects.all()  
            # Sérialiser les données de la tâche
            serializer = TaskSerializer(tasks, many=True) 
            # Renvoyer une réponse JsonReponse
            return JsonResponse(serializer.data, safe=False) 
      elif request.method == 'POST':
            # analyser les informations entrantes
            data = JSONParser().parse(request)
            # instancier avec le sérialiseur
            serializer = TaskSerializer(data=data) 
            if serializer.is_valid(): 
                  # vérifier si les informations envoyées sont correctes
                  serializer.save()
                  #fournir une réponse Json avec les données qui ont été enregistrées
                  return JsonResponse(serializer.data, status=201) 
            # fournir une réponse Json avec les informations d'erreur nécessaires
            return JsonResponse(serializer.errors, status=400) 

@csrf_exempt
def task_detail(request, pk):
      try:
            # Obtenez la tâche avec l'identifiant transmis.
            task = Task.objects.get(pk=pk)
      except Task.DoesNotExist:
            # répondre avec un message d'erreur 404
            return HttpResponse(status=404)
      if(request.method == 'PUT'):
            # analyser les informations entrantes
            data = JSONParser().parse(request)
            # instancier avec le sérialiseur
            serializer = TaskSerializer(task, data=data)
            # vérifier si les informations envoyées sont correctes
            if(serializer.is_valid()):
                  # si tout va bien, enregistrez-le dans la base de données
                  serializer.save()
                  # fournir une réponse JSON avec les données qui ont été soumises
                  return JsonResponse(serializer.data, status=201)
            # fournir une réponse JSON avec les informations d'erreur nécessaires
            return JsonResponse(serializer.data, status=400)
      elif(request.method == 'DELETE'):
            # supprimer la tâche
            task.delete()
            # renvoie une réponse sans contenu.
            return HttpResponse(status=204)

