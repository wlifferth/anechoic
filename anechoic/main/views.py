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

def getPositions(request):
    user = request.user
    context = {}
    if request.method == 'POST':
        positions = Position.objects.all()
        for position in positions:
            if 'p' + str(position.id) in request.POST:
                newUserPosition = UserPosition(user=user, position=position, rating=int(request.POST['p' + str(position.id)]))
                newUserPosition.save()
        return redirect('/')
    else:
        context['positionQuestions'] = Position.objects.all()
        return render(request, 'main/positionSurvey.html', context=context)

def dashboard(request):
    user = request.user
    context = {}
    return render(request, 'main/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            new_user = authenticate(username=f.cleaned_data['username'], password=f.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('/getPositions/')

    else:
        f = UserCreationForm()

    return render(request, 'main/register.html', {'form': f})
