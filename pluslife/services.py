from .models import Refeicao, Hidratacao, Exercicio

class RefeicaoService:
    def criar_refeicao(self, usuario, dados_form):
        nova_refeicao = Refeicao()
        nova_refeicao.usuario = usuario
        nova_refeicao.nome = dados_form.get('nome')
        nova_refeicao.data_hora = dados_form.get('data_hora')
        nova_refeicao.peso = dados_form.get('peso')
        nova_refeicao.calorias = dados_form.get('calorias')
        nova_refeicao.tipo_refeicao = dados_form.get('tipo_refeicao')
        nova_refeicao.save()
        return nova_refeicao

class HidratacaoService:
    def criar_hidratacao(self, usuario, dados_form):
        hidratacao = Hidratacao()
        hidratacao.usuario = usuario
        hidratacao.data_hora = dados_form.get('data_hora')
        hidratacao.mililitros = dados_form.get('mililitros')
        hidratacao.save()
        return hidratacao

class ExercicioService:
    def criar_exercicio(self, usuario, dados_form):
        novo_exercicio = Exercicio()
        novo_exercicio.usuario = usuario
        novo_exercicio.nome = dados_form.get('nome')
        novo_exercicio.data_hora = dados_form.get('data_hora')
        novo_exercicio.minutos = dados_form.get('minutos')
        novo_exercicio.tipo_exercicio = dados_form.get('tipo_exercicio')
        novo_exercicio.save()
        return novo_exercicio
