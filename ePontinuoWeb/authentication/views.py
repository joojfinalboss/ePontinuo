from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
import requests
import datetime
from datetime import timedelta
from .forms import UserCreationForm, LoginForm, DemoForm
from .models import Perfil
# Create your views here.





def index(request):
    return render(request, 'index.html')

# Página de Cadastro
def usuario_cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Página de Login
def usuario_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('main')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Página de Logout
def usuario_logout(request):
    logout(request)
    return redirect('login')



# Página Main

def usuario_analista(request):

    if request.method == "POST":
        form = DemoForm(request.POST)
        if form.is_valid():
            dataPrazo = form.cleaned_data['Selecione_a_Data_para_Filtrar']
            request.user.perfil.dataStart = dataPrazo[0]
            request.user.perfil.dataEnd = (dataPrazo[1] + datetime.timedelta(days=1))
            dataPrazo = [request.user.perfil.dataStart, request.user.perfil.dataEnd]
            
    else:
        dataPrazo = [request.user.perfil.dataStart, request.user.perfil.dataEnd]
        print(request.user.perfil.dataEnd)



    # Calculate the number of days between the dates in dataPrazo

    print(dataPrazo)
    idAnalista = request.user.perfil.idAnalista
    form = DemoForm(initial={"date_range_normal" : dataPrazo})
    listaTiposAtividades = []
    quantiaAtividades = {
        'task': 0,
        'call': 0,
        'imp_acessorias_etapa_i': 0,
        'imp_etapa_ii': 0,
        'imp_acessorias_etapa_iii': 0,
        'imp_acessorias_etapa_iv': 0,
        'treinamento_adicional': 0,
        'acompanhamento_': 0,
        'loja_apple_': 0,
        'reagendar': 0,
        'imp_etapa_iii': 0,
        'chat': 0,
        'ps_venda': 0,
        'komunic': 0,
        'imp_komunic_': 0
    }

    difference = (dataPrazo[1] - dataPrazo[0]).days

    # If the date range is more than 14 days
    if difference > 14:
        # Calculate the number of periods
        num_periods = difference // 7

        # Create the date ranges
        date_ranges = [
            (dataPrazo[0] + timedelta(days=i*7), dataPrazo[0] + timedelta(days=(i+1)*7)) for i in range(num_periods)
        ]

        # Add the remaining days to the last period
        if difference % 7 != 0:
            date_ranges[-1] = (date_ranges[-1][0], dataPrazo[1])


        # Make the API requests
        for start_date, end_date in date_ranges:
            url = "https://api.pipedrive.com/v1/activities?limit=500000000&done=1&user_id={0}&start_date={1}&end_date={2}&api_token=d0f27a8c3a00dbd3bab46ead2a6d3bfc7fec6aa7".format(idAnalista, start_date, end_date)
            response = requests.get(url)
            resposta = response.json()['data']


            # Count the activities for this response
            if resposta is not None:
                listaTiposAtividades = [ atividade['type'] for atividade in resposta ]
            else:
                listaTiposAtividades = []

            for tipoAtividade in listaTiposAtividades:
                if tipoAtividade in quantiaAtividades:
                    quantiaAtividades[tipoAtividade] += 1
    else:
        # Convert the dates to strings in the format 'YYYY-MM-DD'
        start_date_str = dataPrazo[0].strftime('%Y-%m-%d')
        end_date_str = dataPrazo[1].strftime('%Y-%m-%d')

        url = "https://api.pipedrive.com/v1/activities?limit=500000000&done=1&user_id={0}&start_date={1}&end_date={2}&api_token=d0f27a8c3a00dbd3bab46ead2a6d3bfc7fec6aa7".format(idAnalista, start_date_str, end_date_str)
        response = requests.get(url)
        resposta = response.json()['data']

        # Count the activities for this response
        if resposta is not None:
            listaTiposAtividades = [ atividade['type'] for atividade in resposta ]
        else:
            listaTiposAtividades = []

        for tipoAtividade in listaTiposAtividades:
            if tipoAtividade in quantiaAtividades:
                quantiaAtividades[tipoAtividade] += 1




    context = {
        'tasks': quantiaAtividades['task'],
        'calls': quantiaAtividades['call'],
        'impUm': quantiaAtividades['imp_acessorias_etapa_i'],
        'impDois': quantiaAtividades['imp_etapa_ii'],
        'impTres': quantiaAtividades['imp_acessorias_etapa_iii'],
        'impQuatro': quantiaAtividades['imp_acessorias_etapa_iv'],
        'impAdc': quantiaAtividades['treinamento_adicional'],
        'acompanhamento': quantiaAtividades['acompanhamento_'],
        'lojaApple': quantiaAtividades['loja_apple_'],
        'reagendado': quantiaAtividades['reagendar'],
        'impGestao': quantiaAtividades['imp_etapa_iii'],
        'chat': quantiaAtividades['chat'],
        'posVenda': quantiaAtividades['ps_venda'],
        'komunic': quantiaAtividades['komunic'],
        'impKomunic': quantiaAtividades['imp_komunic_'],
        'form': form
    }



    return render(request, 'analista.html', context=context)





