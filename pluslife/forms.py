from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario, Endereco, Refeicao, TipoRefeicao, Hidratacao, Exercicio, TipoExercicio, BemEstar


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Seu email'}),
    )

    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Sua senha'}),
    )

class CadastroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Informe uma senha segura.'
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'data_nascimento', 'password']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cidade']
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


#forms para refeicoes
class RefeicaoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M'], 
        label="Data e Hora"
    )

    class Meta:
        model = Refeicao
        fields = ['nome', 'data_hora', 'peso', 'calorias', 'tipo_refeicao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'calorias': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_refeicao': forms.Select(attrs={'class': 'form-control'}),
        }


class TipoRefeicaoForm(forms.ModelForm):
    class Meta:
        model = TipoRefeicao
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
        }


#forms para hidratacoes
class HidratacaoForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Data e Hora'
    )

    class Meta:
        model = Hidratacao
        fields = ['data_hora', 'mililitros']
        widgets = {
            'mililitros': forms.NumberInput(attrs={'class': 'form-control'}),
        }


#formss para exeercicios
class ExercicioForm(forms.ModelForm):
    data_hora = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Exercicio
        fields = ['nome', 'data_hora', 'minutos', 'tipo_exercicio']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'minutos': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_exercicio': forms.Select(attrs={'class': 'form-control'}),
        }

class TipoExercicioForm(forms.ModelForm):
    class Meta:
        model = TipoExercicio
        fields = ['titulo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
        }


#forms para manipulacao dos dados do usuario
class EditarPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class EditarEnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['rua', 'numero', 'bairro', 'cidade']
        widgets = {
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
        }


#forms para lidar com o bem estar
class BemEstarForm(forms.ModelForm):
    class Meta:
        model = BemEstar
        fields = ['data', 'sentimento', 'desabafo']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'sentimento': forms.Select(attrs={'class': 'form-control'}),
            'desabafo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }