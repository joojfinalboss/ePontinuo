from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
import requests
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
            dataPrazo = form.cleaned_data['date_range_normal']
            request.user.perfil.dataStart = dataPrazo[0]
            request.user.perfil.dataEnd = dataPrazo[1]
            
    else:
        dataPrazo = [request.user.perfil.dataStart, request.user.perfil.dataEnd]


    idAnalista = request.user.perfil.idAnalista

    form = DemoForm(initial={"date_range_normal" : dataPrazo})

    url = "https://api.pipedrive.com/v1/activities?limit=500000000&done=1&user_id={0}&start_date={1}&end_date={2}&api_token=d0f27a8c3a00dbd3bab46ead2a6d3bfc7fec6aa7".format(idAnalista, dataPrazo[0], dataPrazo[1])
    response = requests.get(url)
    respostaUm = response.json()
    resposta = respostaUm['data']

    try:
        listaTiposAtividades = [ atividade['type'] for atividade in resposta ]
    except:
        listaTiposAtividades = []

    quantasTasks = 0
    quantasCalls = 0
    quantasImpUm = 0
    quantasImpDois = 0
    quantasImpTres = 0
    quantasImpQuatro = 0
    quantasImpAdicional = 0
    quantasAcompanhamento = 0
    quantasLojaApple = 0
    quantasReagendado = 0
    quantasGestao = 0
    quantasChat = 0
    quantasPos = 0
    quantasKomunic = 0
    quantasImpKomunic = 0


    for tipoAtividade in listaTiposAtividades:
        if tipoAtividade == None:
            pass
        elif tipoAtividade == 'task':
            quantasTasks = quantasTasks + 1
        elif tipoAtividade == 'call':
            quantasCalls = quantasCalls + 1
        elif tipoAtividade == 'imp_acessorias_etapa_i':
            quantasImpUm = quantasImpUm + 1
        elif tipoAtividade == 'imp_etapa_ii':
            quantasImpDois = quantasImpDois + 1
        elif tipoAtividade == 'imp_acessorias_etapa_iii':
            quantasImpTres = quantasImpTres + 1
        elif tipoAtividade == 'imp_acessorias_etapa_iv':
            quantasImpQuatro = quantasImpQuatro + 1
        elif tipoAtividade == 'treinamento_adicional':
            quantasImpAdicional = quantasImpAdicional + 1
        elif tipoAtividade == 'acompanhamento_':
            quantasAcompanhamento = quantasAcompanhamento + 1
        elif tipoAtividade == "loja_apple_":
            quantasLojaApple = quantasLojaApple + 1
        elif tipoAtividade == 'reagendar':
            quantasReagendado = quantasReagendado + 1
        elif tipoAtividade == 'imp_etapa_iii':
            quantasGestao = quantasGestao + 1    
        elif tipoAtividade == 'chat':
            quantasChat = quantasChat + 1   
        elif tipoAtividade == 'ps_venda':
            quantasPos = quantasPos + 1 
        elif tipoAtividade == 'komunic':
            quantasKomunic = quantasKomunic + 1
        elif tipoAtividade == 'imp_komunic_':
            quantasImpKomunic = quantasImpKomunic + 1
        else:
            pass


    context = {'tasks' : quantasTasks, 'calls' : quantasCalls, 'impUm' : quantasImpUm, 'impDois' : quantasImpDois, 'impTres' : quantasImpTres, 
               'impQuatro' : quantasImpQuatro, 'impAdc' : quantasImpAdicional, 'acompanhamento' : quantasAcompanhamento, 'lojaApple' : quantasLojaApple, 
               'reagendado' : quantasReagendado, 'impGestao' : quantasGestao, 'chat' : quantasChat, 'posVenda' : quantasPos, 'komunic' : quantasKomunic,
               'impKomunic' : quantasImpKomunic,'form' : form}



    return render(request, 'analista.html', context=context)

