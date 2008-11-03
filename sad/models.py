from django.db import models
from django.contrib.auth.models import User

'''
    1. Botar pra funcionar depois a objetos Curso e Instituto!
'''

#class Curso(models.Model):
#    codigo = models.IntegerField(primary_key=True)
#    nome = models.CharField(max_length=256)
#
#    def __unicode__(self):
#        return self.nome


class Aluno(User):
    nome = models.CharField(max_length=256)
    # FIXME: habilitar o curso aqui:
    #curso = models.ForeignKey(Curso)
    curso = models.CharField(max_length=2)

    def __unicode__(self):
        return self.username


class Professor(models.Model):
    #FIXME: adicionar mais campos aqui
    # professor podera ter login?
    # informacoes como instituto?
    nome = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nome


class Questionario(models.Model):
    tipo = models.CharField(max_length=128)
    texto = models.CharField(max_length=1024, blank = True)
    semestre = models.DateField()

    def __unicode__(self):
        return self.tipo


class Disciplina(models.Model):
    sigla = models.CharField(max_length=6, primary_key=True)
    nome = models.CharField(max_length=256)
    questionario = models.ForeignKey(Questionario)
    # FIXME: colocar instituto 

    def __unicode__(self):
        return self.sigla


class Atribuicao(models.Model):
    disciplina = models.ForeignKey(Disciplina)
    professor = models.ForeignKey(Professor)
    turma = models.CharField(max_length=1)
    aluno = models.ManyToManyField(Aluno)
    # FIXME: configurar atribuicao default para o semestre corrente.
    semestre = models.DateField()

    def __unicode__(self):
        return self.disciplina.sigla + self.turma


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


class Alternativa(models.Model):
    texto = models.CharField(max_length=512)
    pergunta = models.ForeignKey(Pergunta)

    def __unicode__(self):
        return self.texto


class Resposta(models.Model):
    pergunta = models.ForeignKey(Pergunta)
    # Tem que ser o texto ou alternativa
    texto = models.CharField(max_length=1024, null=True)
    alternativa = models.ForeignKey(Alternativa, null=True)
    hash_aluno = models.CharField(max_length=32)
    atribuicao = models.ForeignKey(Atribuicao)

    def __unicode__(self):
        return self.texto

