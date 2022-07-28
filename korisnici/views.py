from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profil, Interesovanje
from vesti.models import Izvor
from .forms import KorisnikRegisterForm, InteresovanjeForm


def registerKorisnik(request):
    form = KorisnikRegisterForm()

    if request.method == 'POST':
        form = KorisnikRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            messages.success(request, 'Vaš nalog je kreiran')

            username = request.POST['username']
            password = request.POST['password1']
            authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('profil')
        else:
            messages.error(request, 'Došlo je do greške prilikom registracije')

    context = {'form': form}
    return render(request, 'korisnici/registracija.html', context)


def loginKorisnik(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('pocetna')
        return redirect('profil')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Korisnik ne postoji')

        user = authenticate(request, username=username, password=password) 

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('pocetna')
            return redirect(request.GET['next'] if 'next' in request.GET else 'profil')

        else:
            messages.error(request, 'Email ili šifra su pogrešni')

    return render(request, 'korisnici/login.html')


def logoutKorisnik(request):
    logout(request)
    messages.info(request, 'Uspešno ste se izlogovali')
    return redirect('pocetna')


@login_required(login_url='login')
def profil(request):
    profil = Profil.objects.get(korisnik=request.user.id)
    interesovanja = Interesovanje.objects.filter(profil=profil.id)
    context = {'profil': profil, 'interesovanja':interesovanja}

    return render(request, 'korisnici/profil.html', context)


@login_required(login_url='login')
def uredi_interesovanja(request):
    profil = request.user.profil
    form = InteresovanjeForm()

    if request.method == 'POST':
        form = InteresovanjeForm(request.POST)
        if form.is_valid():
            izvori = dict(request.POST)['izvori']
            
            Interesovanje.objects.filter(profil=profil).delete()

            for izvor_id in izvori:
                izvor = Izvor.objects.get(id=izvor_id)
                novo_int = Interesovanje(izvor=izvor, profil=profil)
                novo_int.save()
            messages.success(request, 'Uspešno je uredjana lista interesovanja!')
            return redirect('profil')

    context = {'form': form}
    return render(request, 'korisnici/uredi_interesovanja.html', context)
