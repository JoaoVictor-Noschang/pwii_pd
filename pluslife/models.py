from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class TipoRefeicao(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class TipoExercicio(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class BemEstar(models.Model):
    usuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='bem_estares')

    SENTIMENTOS_OPCOES = [
        ('muito_triste', 'Muito Triste'),
        ('triste', 'Triste'),
        ('neutro', 'Neutro'),
        ('feliz', 'Feliz'),
        ('muito_feliz', 'Muito Feliz'),
        ('ansioso', 'Ansioso'),
        ('irritado', 'Irritado'),
        ('grato', 'Grato'),
        ('empolgado', 'Empolgado'),
    ]
    data = models.DateField() 
    sentimento = models.CharField(
        max_length=50,
        choices=SENTIMENTOS_OPCOES,
        default='neutro',
        verbose_name='Como você se sente?'
    )
    desabafo = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Desabafo (Opcional)'
    )

    def __str__(self):
        return f"{self.data.strftime('%d/%m/%Y')} - {self.get_sentimento_display()}"

    class Meta:
        verbose_name = "Bem-Estar Mental"
        verbose_name_plural = "Registros de Bem-Estar Mental"
        ordering = ['-data']


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}'


class LegendaImc(models.Model):
    titulo = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, data_nascimento, password=None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório")
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, data_nascimento=data_nascimento, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, data_nascimento, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser precisa ter is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(email, nome, data_nascimento, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    data_criacao = models.DateTimeField(default=timezone.now)

    enderecos = models.ManyToManyField('Endereco', blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'data_nascimento']

    def __str__(self):
        return self.email


class Refeicao(models.Model):
    nome = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    peso = models.FloatField()
    calorias = models.FloatField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='refeicoes')
    tipo_refeicao = models.ForeignKey(TipoRefeicao, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nome} - {self.data_hora}"


class Hidratacao(models.Model):
    data_hora = models.DateTimeField()
    mililitros = models.FloatField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='hidratacoes')

    def __str__(self):
        return f"{self.mililitros} ml em {self.data_hora}"


class Exercicio(models.Model):
    nome = models.CharField(max_length=100)
    data_hora = models.DateTimeField()
    minutos = models.PositiveIntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='exercicios')
    tipo_exercicio = models.ForeignKey(TipoExercicio, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.tipo_exercicio} - {self.minutos} min"


class IMC(models.Model):
    peso = models.FloatField()
    altura = models.FloatField()
    imc = models.FloatField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='imcs')
    legenda = models.ForeignKey(LegendaImc, on_delete=models.CASCADE)

    def __str__(self):
        return f"IMC: {self.imc} ({self.usuario})"
