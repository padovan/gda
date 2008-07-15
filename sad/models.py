from django.db import models


#FIXME:
#   1. Será que essa modelagem está correta? Peguntar pra alguém que manje
# Hanson ou Alan por exemplo. Mas acho que pelo menos essa parte está bem modelada
#   2. Vejo a possibilidade de criar uma classe Curso (não confunda 
# com a classe Cursa!). Isso deixa nosso sistema mais genérico.
#   3. Acho que temos que encontrar outro nome para a classe Cursa.
# Não tá soando bem. É cursa no sentido de tal aluno cursa tal disciplina
#   4. Vamos passar todos os nomes de campos e classes para o inglês?

#  Último: Alguém pode pedir pra invetarem comentário em bloco :-(


class Aluno(models.Model):
    RA = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)
    email = models.EmailField()
    # vai ser  uma 
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
    # Ahh.. como eu queria comentário em bloco no python :-)
    nome = models.CharField(maxlength=256)

    def __str__(self):
        return self.nome

    class Admin:
        search_fields = ('nome')


class Disciplina(models.Model):
    sigla = models.CharField(maxlength=6, primary_key=True)
    nome = models.CharField(maxlength=256)

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
    #FIXME: criar esses dois campos
    #periodo = models.
    #questionario = models.ForeignKey
    def __str__(self):
        return self.disciplina.sigla + self.turma

    class Admin:
        list_display = ('disciplina','professor', 'turma')
        # FIXME: Fazer filtragem por disciplina e professor
        # não funciona por que é chave estrangeira
        #list_filter = ['disciplina']
        search_fields = ('disciplina')

#FIXME: essa tabela ( classe ) tem nome estranho. Não consegui pensar em 
# nada melhor. Ma fica a dica! ;-)
class Cursa(models.Model):
    aluno = models.ForeignKey(Aluno)
    disc_turma = models.ForeignKey(Atribuicao)
    
    #def __str__(self):
    # FIXME: o que retornar aqui

    class Admin:
        #FIXME: não cheguei a pensar essa parte
        pass

    
