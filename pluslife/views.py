from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from datetime import datetime
from django.db import models
from django.db.models import ProtectedError

from .forms import CadastroUsuarioForm, EnderecoForm, LoginForm, RefeicaoForm, TipoRefeicaoForm, HidratacaoForm, ExercicioForm, TipoExercicioForm, EditarPerfilForm, EditarEnderecoForm, TipoExercicioForm, BemEstarForm
from .models import Usuario, Refeicao, Hidratacao, Exercicio, Endereco, TipoRefeicao, TipoExercicio, BemEstar, IMC, LegendaImc

#services das injeções de dependência
from pluslife.services import RefeicaoService, HidratacaoService, ExercicioService

TEMPLATE_CONFIRMACAO_EXCLUSAO = 'pluslife/confirmar_exclusao.html'

@require_GET
def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@require_http_methods(["GET", "POST"])
def cadastro_view(request):
    if request.method == 'POST':
        user_form = CadastroUsuarioForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if user_form.is_valid() and endereco_form.is_valid():
            usuario = user_form.save(commit=False)
            usuario.set_password(user_form.cleaned_data['password'])
            usuario.save()

            endereco = endereco_form.save()
            usuario.enderecos.add(endereco)
            usuario.save()

            login(request, usuario)
            return redirect('dashboard')
    else:
        user_form = CadastroUsuarioForm()
        endereco_form = EnderecoForm()

    return render(request, 'cadastro.html', {
        'user_form': user_form,
        'endereco_form': endereco_form,
    })


@require_http_methods(["GET", "POST"])
def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            senha = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=senha)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'form': form, 'erro': 'Credenciais inválidas'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@require_POST
def logout_usuario(request):
    logout(request)
    return redirect('login')


@require_GET
@login_required
def dashboard_view(request):
    hoje = timezone.now().date()
    usuario = request.user

    # Somar calorias das refeições de hoje
    total_calorias = Refeicao.objects.filter(
        usuario=usuario, data_hora__date=hoje
    ).aggregate(total=models.Sum('calorias'))['total'] or 0

    # Somar mililitros de água de hoje
    total_agua = Hidratacao.objects.filter(
        usuario=usuario, data_hora__date=hoje
    ).aggregate(total=models.Sum('mililitros'))['total'] or 0

    # Somar minutos de exercícios de hoje
    total_minutos = Exercicio.objects.filter(
        usuario=usuario, data_hora__date=hoje
    ).aggregate(total=models.Sum('minutos'))['total'] or 0

    #Conversão de ml para lt
    total_agua_litros = round(total_agua / 1000, 2)

    # Converter minutos em horas e minutos
    horas = total_minutos // 60
    minutos = total_minutos % 60
    tempo_exercicio = f"{horas}h {minutos}m" if total_minutos else "0h 0m"

    return render(request, 'dashboard.html', {
        'usuario': usuario,
        'total_calorias': total_calorias,
        'total_agua': total_agua_litros,
        'tempo_exercicio': tempo_exercicio,
        'hoje': hoje.strftime('%d/%m/%Y'),
    })


#View para refeições
@require_GET
@login_required
def refeicao_view(request):
    refeicoes = Refeicao.objects.filter(usuario=request.user).order_by('-data_hora')
    return render(request, 'pluslife/refeicao.html', {'refeicoes': refeicoes})

@require_http_methods(["GET", "POST"])
@login_required
def cadastrar_refeicao(request):
    form = RefeicaoForm(request.POST or None, usuario=request.user)
    service = RefeicaoService()

    if request.method == 'POST' and form.is_valid():
        #injeção de dependência
        #passando a responsábilidade para o service
        service.criar_refeicao(request.user, form.cleaned_data)
        return redirect('refeicoes')

    return render(request, 'pluslife/form_refeicao.html', {'form': form, 'titulo': 'Nova Refeição'})

@require_http_methods(["GET", "POST"])
@login_required
def editar_refeicao(request, pk):
    refeicao = get_object_or_404(Refeicao, pk=pk, usuario=request.user)
    form = RefeicaoForm(request.POST or None, instance=refeicao, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('refeicoes')

    return render(request, 'pluslife/form_refeicao.html', {'form': form, 'titulo': 'Editar Refeição'})

@require_http_methods(["GET", "POST"])
@login_required
def excluir_refeicao(request, pk):
    refeicao = get_object_or_404(Refeicao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        refeicao.delete()
        return redirect('refeicoes')
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'objeto': refeicao, 
        'tipo': 'refeição', 
        'cancel_url': reverse('refeicoes')
    })

# manipulando cadastros de tipo de refeição
@require_http_methods(["GET", "POST"])
@login_required
def tipos_refeicao_view(request):
    tipos = TipoRefeicao.objects.filter(usuario=request.user)
    form = TipoRefeicaoForm()

    if request.method == 'POST':
        form = TipoRefeicaoForm(request.POST)
        if form.is_valid():
            form.save(usuario=request.user)
            return redirect('tipos_refeicao')

    return render(request, 'pluslife/tipos_refeicao.html', {
        'tipos': tipos,
        'form': form,
    })

@require_http_methods(["GET", "POST"])
@login_required
def editar_tipo_refeicao(request, pk):
    tipo = get_object_or_404(TipoRefeicao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TipoRefeicaoForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('tipos_refeicao')
    else:
        form = TipoRefeicaoForm(instance=tipo)
    return render(request, 'pluslife/form_tipo_refeicao.html', {'form': form, 'tipo': tipo})

@require_http_methods(["GET", "POST"])
@login_required
def excluir_tipo_refeicao(request, pk):
    tipo = get_object_or_404(TipoRefeicao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        try:
            tipo.delete()
            messages.success(request, 'Tipo de refeição excluído com sucesso.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: há refeições associadas a este tipo.')
        return redirect('tipos_refeicao')
    
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'tipo': 'Tipo de Refeição',
        'objeto': tipo,
    })


#View para hidratação
@require_GET
@login_required
def hidratacao_view(request):
    hidratacoes = Hidratacao.objects.filter(usuario=request.user).order_by('-data_hora')
    return render(request, 'pluslife/hidratacao.html', {'hidratacoes': hidratacoes})

@require_http_methods(["GET", "POST"])
@login_required
def cadastrar_hidratacao(request):
    form = HidratacaoForm(request.POST or None)
    service = HidratacaoService()

    if request.method == 'POST' and form.is_valid():
        #injeção de dependência
        #passando a responsábilidade para o service
        service.criar_hidratacao(request.user, form.cleaned_data)
        return redirect('hidratacoes')

    return render(request, 'pluslife/form_hidratacao.html', {
        'form': form,
        'titulo': 'Nova Hidratação'
    })

@require_http_methods(["GET", "POST"])
@login_required
def editar_hidratacao(request, pk):
    hidratacao = get_object_or_404(Hidratacao, pk=pk, usuario=request.user)
    form = HidratacaoForm(request.POST or None, instance=hidratacao)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('hidratacoes')
    return render(request, 'pluslife/form_hidratacao.html', {'form': form, 'titulo': 'Editar Hidratação'})

@require_http_methods(["GET", "POST"])
@login_required
def excluir_hidratacao(request, pk):
    hidratacao = get_object_or_404(Hidratacao, pk=pk, usuario=request.user)
    if request.method == 'POST':
        hidratacao.delete()
        return redirect('hidratacoes')
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'objeto': hidratacao, 
        'tipo': 'hidratação',
        'cancel_url': reverse('hidratacoes')
    })


#views para exercicios
@require_GET
@login_required
def exercicio_view(request):
    exercicios = Exercicio.objects.filter(usuario=request.user).order_by('-data_hora')
    return render(request, 'pluslife/exercicio.html', {'exercicios': exercicios})

@require_http_methods(["GET", "POST"])
@login_required
def cadastrar_exercicio(request):
    form = ExercicioForm(request.POST or None, usuario=request.user)
    service = ExercicioService()

    if request.method == 'POST' and form.is_valid():
        #injeção de dependência
        #passando a responsábilidade para o service
        service.criar_exercicio(request.user, form.cleaned_data)
        return redirect('exercicios')

    return render(request, 'pluslife/form_exercicio.html', {
        'form': form,
        'titulo': 'Novo Exercício'
    })

@require_http_methods(["GET", "POST"])
@login_required
def editar_exercicio(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk, usuario=request.user)
    form = ExercicioForm(request.POST or None, instance=exercicio, usuario=request.user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('exercicios')

    return render(request, 'pluslife/form_exercicio.html', {'form': form, 'titulo': 'Editar Exercício'})

@require_http_methods(["GET", "POST"])
@login_required
def excluir_exercicio(request, pk):
    exercicio = get_object_or_404(Exercicio, pk=pk, usuario=request.user)
    if request.method == 'POST':
        exercicio.delete()
        return redirect('exercicios')
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'objeto': exercicio, 
        'tipo': 'exercício',
        'cancel_url': reverse('exercicios')
    })


#views para manipular tipos de exercícios
@require_http_methods(["GET", "POST"])
@login_required
def tipos_exercicio_view(request):
    tipos = TipoExercicio.objects.filter(usuario=request.user)
    form = TipoExercicioForm()

    if request.method == 'POST':
        form = TipoExercicioForm(request.POST)
        if form.is_valid():
            form.save(usuario=request.user)
            return redirect('tipos_exercicio')

    return render(request, 'pluslife/tipos_exercicio.html', {
        'tipos': tipos,
        'form': form,
    })

@require_http_methods(["GET", "POST"])
@login_required
def editar_tipo_exercicio(request, pk):
    tipo = get_object_or_404(TipoExercicio, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        form = TipoExercicioForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            return redirect('tipos_exercicio')
    else:
        form = TipoExercicioForm(instance=tipo)

    return render(request, 'pluslife/form_tipo_exercicio.html', {
        'form': form,
        'tipo': tipo,
    })

@require_http_methods(["GET", "POST"])
@login_required
def excluir_tipo_exercicio(request, pk):
    tipo = get_object_or_404(TipoExercicio, pk=pk, usuario=request.user)

    if request.method == 'POST':
        try:
            tipo.delete()
            messages.success(request, 'Tipo de exercício excluído com sucesso.')
        except ProtectedError:
            messages.error(request, 'Não é possível excluir: há exercícios associados a este tipo.')
        return redirect('tipos_exercicio')

    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'tipo': 'Tipo de Exercício',
        'objeto': tipo,
    })


#views para o perfil e manipulção do usuário
@require_GET
@login_required
def perfil_view(request):
    usuario = request.user
    enderecos = usuario.enderecos.all() 

    endereco = enderecos.first() if enderecos.exists() else None

    return render(request, 'pluslife/perfil.html', {
        'usuario': usuario,
        'endereco': endereco,
        'url': 'perfil',
    })

@require_http_methods(["GET", "POST"])
@login_required
def editar_perfil_view(request):
    usuario = request.user
    endereco = usuario.enderecos.first()

    if request.method == 'POST':
        user_form = EditarPerfilForm(request.POST, instance=usuario)
        endereco_form = EditarEnderecoForm(request.POST, instance=endereco)

        if user_form.is_valid() and endereco_form.is_valid():
            user_form.save()
            endereco_form.save()
            return redirect('perfil')

    else:
        user_form = EditarPerfilForm(instance=usuario)
        endereco_form = EditarEnderecoForm(instance=endereco)

    return render(request, 'pluslife/editar_perfil.html', {
        'user_form': user_form,
        'endereco_form': endereco_form,
    })


# Views para lidar com Bem estar
@require_GET
@login_required
def bemestar_view(request):
    registros = BemEstar.objects.filter(usuario=request.user).order_by('-data')
    return render(request, 'pluslife/bemestar.html', {'registros': registros})

@require_http_methods(["GET", "POST"])
@login_required
def cadastrar_bemestar(request):
    form = BemEstarForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        registro = form.save(commit=False)
        registro.usuario = request.user
        registro.save()
        return redirect('bemestar')
    return render(request, 'pluslife/form_bemestar.html', {'form': form, 'titulo': 'Novo Registro de Bem-Estar'})

@require_http_methods(["GET", "POST"])
@login_required
def editar_bemestar(request, pk):
    registro = get_object_or_404(BemEstar, pk=pk, usuario=request.user)
    form = BemEstarForm(request.POST or None, instance=registro)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('bemestar')
    return render(request, 'pluslife/form_bemestar.html', {'form': form, 'titulo': 'Editar Registro de Bem-Estar'})

@require_http_methods(["GET", "POST"])
@login_required
def excluir_bemestar(request, pk):
    registro = get_object_or_404(BemEstar, pk=pk, usuario=request.user)
    if request.method == 'POST':
        registro.delete()
        return redirect('bemestar')
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'objeto': registro,
        'tipo': 'registro de bem-estar',
        'cancel_url': reverse('bemestar')
    })


#Views para manipular o IMC
def obter_legenda(imc):
    if imc < 18.5:
        return 'Abaixo do peso'
    elif 18.5 <= imc < 25:
        return 'Peso normal'
    elif 25 <= imc < 30:
        return 'Sobrepeso'
    elif 30 <= imc < 35:
        return 'Obesidade Grau 1'
    elif 35 <= imc < 40:
        return 'Obesidade Grau 2'
    else:
        return 'Obesidade Grau 3'

@require_GET
@login_required
def imc_view(request):
    imcs = IMC.objects.filter(usuario=request.user).order_by('-id')
    return render(request, 'pluslife/imc.html', {'imcs': imcs})

@require_http_methods(["GET", "POST"])
@login_required
def calcular_registrar_imc(request):
    resultado = None
    observacao = None
    peso = None
    altura = None
    imc_formatado = None

    if request.method == 'POST':
        try:
            peso = float(request.POST.get('peso', '0').replace(',', '.'))
            altura = float(request.POST.get('altura', '0').replace(',', '.'))

            if peso > 0 and altura > 0:
                imc = peso / (altura * altura)
                imc_formatado = round(imc, 2)
                observacao = obter_legenda(imc_formatado).strip()

                try:
                    legenda = LegendaImc.objects.get(titulo__iexact=observacao)
                except LegendaImc.DoesNotExist:
                    messages.error(request, f'Legenda não encontrada para: "{observacao}"')
                    legenda = None

                if 'registrar' in request.POST and legenda:
                    IMC.objects.create(
                        peso=peso,
                        altura=altura,
                        imc=imc_formatado,
                        legenda=legenda,
                        usuario=request.user
                    )
                    messages.success(request, "IMC registrado com sucesso.")
                    return redirect('imc')

                resultado = imc_formatado

            else:
                messages.error(request, 'Peso e altura devem ser maiores que zero.')

        except ValueError:
            messages.error(request, 'Erro nos valores informados.')

    return render(request, 'pluslife/calculo_imc.html', {
        'resultado': resultado,
        'observacao': observacao,
        'peso': peso,
        'altura': altura,
    })

@require_http_methods(["GET", "POST"])
@login_required
def excluir_imc(request, pk):
    imc = get_object_or_404(IMC, pk=pk, usuario=request.user)
    if request.method == 'POST':
        imc.delete()
        messages.success(request, 'Registro de IMC excluído com sucesso.')
        return redirect('imc')
    return render(request, TEMPLATE_CONFIRMACAO_EXCLUSAO, {
        'objeto': imc,
        'tipo': 'registro de IMC',
        'cancel_url': reverse('imc')
    })