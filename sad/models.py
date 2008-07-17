from django.db import models

#FIXME:
#   1. Será que essa modelagem está correta? Peguntar pra alguém que manje
# Hanson ou Alan por exemplo. Mas acho que pelo menos essa parte está bem modelada
#   2. Vejo a possibilidade de criar uma classe Curso. Isso deixa nosso 
# sistema mais genérico.
#   4. Vamos passar todos os nomes de campos e classes para o inglês?

#  Último: Alguém pode pedir pra invetarem comentário em bloco :-(


class Curso(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(maxlength=256)

    def __str__(self):
        return self.nome

    class Admin:
        list_display = ['codigo','nome']

class Aluno(models.Model):
    RA = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)
    email = models.EmailField()
    #curso = models.ForeignKey(Curso)
    curso = models.CharField(maxlength=2)
    password = models.CharField(maxlength=256)

    def __str__(self):
        return self.RA

    class Admin:
        fields = (
                ('', {'fields': ('RA', 'nome', 'email', 'curso',)}),
        )
        #FIXME: fazer campo de select no curso (talvez uma tabela curso)
        # ou ainda deixar o campo com maior flexibilidade para
        # facilitar o uso do GDA por outras pessoas 
        list_display = ('RA', 'nome', 'email', 'curso')
        list_filter = ['curso']
        #FIXME: fazer busca por RA também
        search_fields = ('nome')


class Professor(models.Model):
    #FIXME: adicionar mais campos aqui
    # professor poderá ter login?
    # informações como instituto?
    # Ahh.. como eu queria comentário em bloco no python
    nome = models.CharField(maxlength=256)

    def __str__(self):
        return self.nome

    class Admin:
        search_fields = ('nome')


class Disciplina(models.Model):
    sigla = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)
    # FIXME: campo quest_id vai onde?

    def __str__(self):
        return self.sigla

    class Admin:
        list_display = ('sigla','nome')
        # FIXME: fazer buscar por sigla ou por nome
        search_fields = ('sigla')

class Atribuicao(models.Model):
    disciplina = models.ForeignKey(Disciplina)
    professor = models.ForeignKey(Professor)
    turma = models.CharField(maxlength=1)
    #FIXME: criar campo periodo?
    #periodo = models.
    def __str__(self):
        return self.disciplina.sigla + self.turma

    class Admin:
        list_display = ('disciplina','professor', 'turma')
        # FIXME: Fazer filtragem por disciplina e professor
        # não funciona por que é chave estrangeira
        #list_filter = ['disciplina']
        search_fields = ('disciplina')

class DiscTurma(models.Model):
    aluno = models.ForeignKey(Aluno)
    disc_turma = models.ForeignKey(Atribuicao)
    
    #def __str__(self):
    # FIXME: o que retornar aqui

    class Admin:
        #FIXME: não cheguei a pensar essa parte
        pass


class Questionario(models.Model):
    tipo = models.CharField(maxlength=128)
    texto = models.CharField(maxlength=1024, blank = True)

    def __str__(self):
        return self.tipo

    class Admin:
        pass

class Pergunta(models.Model):
    tipo = models.PositiveSmallIntegerField()
    texto = models.CharField(maxlength=1024)
    quest = models.ForeignKey(Questionario)

    def __str__(self):
        return self.texto

    class Admin:
        pass


class Alternativa(models.Model):
    texto = models.CharField(maxlength=512)
    pergunta_id = models.ForeignKey(Pergunta)

    def __str__(self):
        return self.texto

    class Admin:
        pass

class Resposta(models.Model):
    texto = models.CharField(maxlength=1024)
    perg = models.ForeignKey(Pergunta)
    altern = models.ForeignKey(Alternativa)

    #FIXME: devemor guardar aqui e/ou na pergunta se é alternativa ou não?

    class Admin:
        pass

