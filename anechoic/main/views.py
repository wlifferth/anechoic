from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Position, UserPosition
from django.contrib.auth.models import User

from urllib.parse import urlparse

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
    context = {}
    user = request.user
    positions_to_show = []
    for userPosition in UserPosition.objects.filter(user=user):
        if userPosition.rating < 5:
            positions_to_show.append(userPosition.position)
        elif userPosition.rating > 5:
            positions_to_show.append(userPosition.position)
    for position in positions_to_show:
        position.top_arguments = position.argument_set.all()
        for argument in position.top_arguments:
            parsed_uri = urlparse(argument.link)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            argument.domain = domain
    # Get the four "best" arguments
    context['positions'] = positions_to_show
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
