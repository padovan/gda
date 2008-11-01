from django.db import models
import time


'''
    1. Botar pra funcionar depois a objetos Curso e Instituto!
'''


class Curso(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nome

    class Admin:
        list_display = ['codigo','nome']
        ordering = ['nome']

    class Meta:
        ordering = ['nome']

class Aluno(models.Model):
    RA = models.CharField(max_length=6, primary_key=True)
    nome = models.CharField(max_length=256)
    email = models.EmailField()
    # FIXME: habilitar o curso aqui:
    #curso = models.ForeignKey(Curso)
    curso = models.CharField(max_length=2)
    senha = models.CharField(max_length=256)

    def __unicode__(self):
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
    # professor podera ter login?
    # informacoes como instituto?
    nome = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nome

    class Admin:
        search_fields = ('nome')


class Questionario(models.Model):
    tipo = models.CharField(max_length=128)
    texto = models.CharField(max_length=1024, blank = True)
    semestre = models.DateField()

    def __unicode__(self):
        return self.tipo

    class Admin:
        list_display = ('tipo', 'texto')
        list_filter = ['tipo']
        search_fields = ('texto')


class Disciplina(models.Model):
    sigla = models.CharField(max_length=6, primary_key=True)
    nome = models.CharField(max_length=256)
    questionario = models.ForeignKey(Questionario)
    # FIXME: colocar instituto 

    def __unicode__(self):
        return self.sigla

    class Admin:
        list_display = ('sigla','nome')
        # FIXME: fazer buscar por sigla ou por nome
        search_fields = ('sigla')

class Atribuicao(models.Model):
    disciplina = models.ForeignKey(Disciplina)
    professor = models.ForeignKey(Professor)
    turma = models.CharField(max_length=1)
    aluno = models.ManyToManyField(Aluno)
    # FIXME: configurar atribuicao default para o semestre corrente.
    semestre = models.DateField()


    def __unicode__(self):
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
    texto = models.CharField(max_length=1024)
    tipo = models.CharField(max_length=1, choices=TIPO_CH)
    questionario = models.ManyToManyField(Questionario, verbose_name = "Questionario(s)")

    def __unicode__(self):
        return self.texto

    class Admin:
        fields = (
                ('',{'fields': ('texto', 'tipo', 'questionario',)}),
        )
        search_fields = ['texto']
        list_filter = ['tipo']


class Alternativa(models.Model):
    texto = models.CharField(max_length=512)
    pergunta = models.ForeignKey(Pergunta)

    def __unicode__(self):
        return self.texto

    class Admin:
        pass


class Resposta(models.Model):
    texto = models.CharField(max_length=1024)
    pergunta = models.ForeignKey(Pergunta)
    alternativa = models.ForeignKey(Alternativa)
    semestre = models.DateField()

    def __unicode__(self):
        return self.texto

    class Admin:
        pass
