from django.db import models
import time

'''#FIXME:
   1. Vamos passar todos os nomes de campos e classes para o inglês?
'''


class Curso(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(maxlength=256)

    def __str__(self):
        return self.nome

    class Admin:
        list_display = ['codigo','nome']
        ordering = ['nome']

    class Meta:
        ordering = ['nome']

class Aluno(models.Model):
    RA = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)
    email = models.EmailField()
    # FIXME: habilitar o curso aqui:
    #curso = models.ForeignKey(Curso)
    curso = models.CharField(maxlength=2)
    senha = models.CharField(maxlength=256)

    def __str__(self):
        return self.RA

    class Admin:
        fields = (
                ('', {'fields': ('RA', 'nome', 'email', 'curso',)}),
        )
        list_display = ('RA', 'nome', 'email', 'curso')
        list_filter = ['curso']
        search_fields = ('nome', 'RA')


class Professor(models.Model):
    #FIXME: adicionar mais campos aqui
    # professor poderá ter login?
    # informações como instituto?
    nome = models.CharField(maxlength=256)

    def __str__(self):
        return self.nome

    class Admin:
        search_fields = ('nome')


class Questionario(models.Model):
    tipo = models.CharField(maxlength=128)
    texto = models.CharField(maxlength=1024, blank = True)

    def __str__(self):
        return self.tipo

    class Admin:
        list_display = ('tipo', 'texto')
        list_filter = ['tipo']
        search_fields = ('texto')


class Disciplina(models.Model):
    sigla = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)
    questionario = models.ForeignKey(Questionario)

    def __str__(self):
        return self.sigla

    class Admin:
        list_display = ('sigla','nome')
        # FIXME: fazer buscar por sigla ou por nome
        search_fields = ('sigla')

class Atribuicao(models.Model):
    SEMESTRE_CH = (
        (1, 'Primeiro'),
        (2, 'Segundo'),
    )
    disciplina = models.ForeignKey(Disciplina)
    professor = models.ForeignKey(Professor)
    turma = models.CharField(maxlength=1)
    aluno = models.ManyToManyField(Aluno)
    semestre = models.PositiveSmallIntegerField(maxlength=1, choices=SEMESTRE_CH)
    ano = models.PositiveSmallIntegerField(default=time.strftime("%Y", time.localtime()))


    def __str__(self):
        return self.disciplina.sigla + self.turma

    class Admin:
        list_display = ('disciplina','professor', 'turma')
        list_filter = ['disciplina']
        search_fields = ('disciplina')


class Pergunta(models.Model):
    TIPO_CH = (
        ('A', 'Alternativa'),
        ('D', 'Dissertativa'),
    )
    texto = models.CharField(maxlength=1024)
    tipo = models.CharField(maxlength=1, choices=TIPO_CH)
    questionario = models.ManyToManyField(Questionario, verbose_name = "Questionário(s)")

    def __str__(self):
        return self.texto

    class Admin:
        fields = (
                ('',{'fields': ('texto', 'tipo', 'questionario',)}),
        )
        search_fields = ['texto']
        list_filter = ['tipo']


class Alternativa(models.Model):
    texto = models.CharField(maxlength=512)
    pergunta = models.ForeignKey(Pergunta)

    def __str__(self):
        return self.texto

    class Admin:
        pass


class Resposta(models.Model):
    texto = models.CharField(maxlength=1024)
    pergunta = models.ForeignKey(Pergunta)
    alternativa = models.ForeignKey(Alternativa)

    def __str__(self):
        return self.texto

    class Admin:
        pass

