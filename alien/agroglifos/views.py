from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect # Funcao para redirecionar o usuario
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from .forms import AgroglifoForm
from .models import Agroglifos

import uuid


def index(request):
    """-------------------------------------------------------------------------
    View index principal do projeto.
    -------------------------------------------------------------------------"""
    return render_to_response("index.html")

def index2(request):
    """-------------------------------------------------------------------------
    View index pós login do projeto.
    -------------------------------------------------------------------------"""
    return render_to_response("index2.html")

def register(request):
    """-------------------------------------------------------------------------
    View de cadastro de usuário.
    -------------------------------------------------------------------------"""
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # cria um novo usuario a partir dos dados enviados
            form.save()
            # redireciona para a tela de login
            return HttpResponseRedirect("/login/")
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "register.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "register.html", {"form": UserCreationForm() })

def log_in(request):
    """-------------------------------------------------------------------------
    View de login.
    -------------------------------------------------------------------------"""
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # se o formulario for valido
        if form.is_valid():
            # significa que o Django encontrou o usuario no banco de dados
            login(request, form.get_user())
            # redireciona o usuario logado para a pagina inicial(index2)
            return HttpResponseRedirect("/home/")
        else:
            return render(request, "login.html", {"form": form})

    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "login.html", {"form": AuthenticationForm()})

def register_occur(request):
    """-------------------------------------------------------------------------
    View para cadastro de ocorrência.
    -------------------------------------------------------------------------"""
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = AgroglifoForm(request.POST)
        # se o formulario for valido
        if form.is_valid():
            # pego info do form
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            # gero codigo uuid para a criação da url de detalhes
            cod = uuid.uuid4().hex
            # persisto agroglifo
            try:
                Agroglifos.objects.create(
                    city=cidade,
                    state=estado,
                    date=data,
                    description=descricao,
                    uuid=cod
                    )
            # em caso de erro
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context = {
                  'erro': 'Informaçẽs incorretas!'
                }
                # retorno a pagina de cadastro com mensagem de erro
                return render(request, "register_occur.html", context)
            # se não houver erros redireciono para a lista de ocorrências
            return HttpResponseRedirect("/list_occurrences/")
        else:
            # se for um get, renderizo a pagina de cadastro de ocorrência
            return render(request, "register_occur.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "register_occur.html", {"form": UserCreationForm()})

def list_occurrences(request):
    """-------------------------------------------------------------------------
    View que lista ocorrências.
    -------------------------------------------------------------------------"""
    # faço um "SELECT *" ordenado pela data
    occurrences = Agroglifos.objects.all().order_by('-date')

    # Incluímos no context
    context = {
      'occurrences': occurrences
    }

    # Retornamos o template no qual as ocorrências serão dispostas
    return render(request, "list_occurrences.html", context)


def summary(request):
    """-------------------------------------------------------------------------
    View que mostra a quantidade de ocorrências por estado.
    -------------------------------------------------------------------------"""
    # inicio lista com siglas dos estados para que a busca seja oudenada alfabeticamente
    states_options = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
    # inicio a lista que sera inserida ao context
    occurrences = []
    # para cada estado na lista
    for i in states_options:
        # faço um "count" de ocorrências
        count = Agroglifos.objects.filter(state=i).count()
        # e se caso exista mais que 0 ocorrências
        if count > 0:
            # adiciono na lista que será disposta no template
            occurrences.append({"state":i, "count":count})
    # Incluímos no context
    context = {
      'occurrences': occurrences
    }

    # Retornamos o template no qual as ocorrências serão dispostas
    return render(request, "summary.html", context)

def details(request, uuid):
    """-------------------------------------------------------------------------
    View que mostra detalhes da ocorrência, inclusive descrição.
    -------------------------------------------------------------------------"""
    # Primeiro, buscamos a ocorrência
    occurrence = Agroglifos.objects.get(uuid=uuid)

    # Incluímos no contexto
    context = {
      'occurrence': occurrence
    }

    # Retornamos o template no qual ocorrência será disposta
    return render(request, "details.html", context)
