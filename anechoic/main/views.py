from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Position, UserPosition, Argument, ArgumentForm
from django.contrib.auth.models import User

from urllib.parse import urlparse
import requests

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
                try:
                    old_user_position = user.userposition_set.filter(position=position).get()
                    old_user_position.rating = int(request.POST['p' + str(position.id)])
                    old_user_position.save()
                    print("We updated the old one!")
                except:
                    new_user_position = UserPosition(user=user, position=position, rating=int(request.POST['p' + str(position.id)]))
                    new_user_position.save()
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
            userPosition.position.in_favor = True
            positions_to_show.append(userPosition.position)
        elif userPosition.rating > 5:
            userPosition.position.in_favor = False
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

def newArgument(request, positionID):
    context = {}
    if request.method == 'POST':
        position = Position.objects.filter(id=positionID).get()
        # process post data
        f = ArgumentForm(request.POST)
        rv = requests.get("http://api.linkpreview.net/?key={}&q={}".format("5ac98866364ea5848b84e5718149831a51c14e52c6e1f", f['link']))
        if rv.json()['image'] == "":
            preview_img = "http://www.google.com/s2/favicons?domain_url={}".format(f['link'])
        else:
            preview_img = rv.json()['image']
        f.preview_img = rv.json()['image']
        new_arg = f.save()
        new_arg.prewiew_img = rv.json()['image']
        new_arg.position = position
        new_arg.author = request.user
        new_arg.save()
        return redirect('/')
    else:
        context['position'] = Position.objects.filter(id=positionID).get()
        context['newArgumentForm'] = ArgumentForm()
        return render(request, 'main/newArgument.html', context)


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
