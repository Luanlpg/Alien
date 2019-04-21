from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect # Funcao para redirecionar o usuario
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from .forms import AgroglifoForm
from .models import Agroglifos

import uuid

# pagina inicial do projeto
def index(request):
    return render_to_response("index.html")

def index2(request):
    return render_to_response("index2.html")

# pagina de cadastro
def register(request):
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid(): # se o formulario for valido
            form.save() # cria um novo usuario a partir dos dados enviados
            return HttpResponseRedirect("/login/") # redireciona para a tela de login
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "register.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "register.html", {"form": UserCreationForm() })


# pagina de login
def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            #se o formulario for valido significa que o Django conseguiu encontrar o usuario no banco de dados
            #agora, basta logar o usuario e ser feliz.
            login(request, form.get_user())
            return HttpResponseRedirect("/home/") # redireciona o usuario logado para a pagina inicial
        else:
            return render(request, "login.html", {"form": form})

    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "login.html", {"form": AuthenticationForm()})

def register_occur(request):
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = AgroglifoForm(request.POST)
        print(form)
        if form.is_valid(): # se o formulario for valido
            cidade = form.cleaned_data['cidade']
            estado = form.cleaned_data['estado']
            data = form.cleaned_data['data']
            descricao = form.cleaned_data['descricao']
            cod = uuid.uuid4().hex
            try:
                Agroglifos.objects.create(
                    city=cidade,
                    state=estado,
                    date=data,
                    description=descricao,
                    uuid=cod
                    )
            except Exception as e:
                print(e)
                # Incluímos no contexto
                context = {
                  'erro': 'Informaçẽs incorretas!'
                }
                return render(request, "register_occur.html", context)
            #form.save() # cria um novo usuario a partir dos dados enviados
            return HttpResponseRedirect("/list_occurrences/") # redireciona para a tela de login
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "register_occur.html", {"form": form})

    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "register_occur.html", {"form": UserCreationForm() })
#return render_to_response("register_occur.html")

def list_occurrences(request):
    # Primeiro, buscamos os funcionarios
    occurrences = Agroglifos.objects.all().order_by('-date')

    # Incluímos no contexto
    context = {
      'occurrences': occurrences
    }

    # Retornamos o template no qual os funcionários serão dispostos
    return render(request, "list_occurrences.html", context)


def summary(request):
    states_options = [
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO",
            "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI",
            "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
            ]
    occurrences = []
    for i in states_options:
        count = Agroglifos.objects.filter(state=i).count()
        if count > 0:
            occurrences.append({"state":i, "count":count})
    # Incluímos no contexto
    context = {
      'occurrences': occurrences
    }

    # Retornamos o template no qual os funcionários serão dispostos
    return render(request, "summary.html", context)

def details(request, uuid):
    # Primeiro, buscamos os funcionarios
    occurrence = Agroglifos.objects.get(uuid=uuid)

    # Incluímos no contexto
    context = {
      'occurrence': occurrence
    }

    # Retornamos o template no qual os funcionários serão dispostos
    return render(request, "details.html", context)
