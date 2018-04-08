from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Position, UserPosition
from django.contrib.auth.models import User

# Create your views here.

def hello(request):
    return HttpResponse("Hello!")

def getPositions(request, username):
    context = {}
    if request.method == 'POST':
        positions = Position.objects.all()
        user = User.objects.filter(username=username).get();
        for position in positions:
            if 'p' + str(position.id) in request.POST:
                newUserPosition = UserPosition(user=user, position=position, rating=int(request.POST['p' + str(position.id)]))
                newUserPosition.save()
        return HttpResponse("You successfully submitted the form!")
    else:
        context['positionQuestions'] = Position.objects.all()
        return render(request, 'main/positionSurvey.html', context=context)

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = UserCreationForm()

    return render(request, 'main/register.html', {'form': f})
