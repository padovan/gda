from sad.models import *
from django.contrib import admin

class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ['nome']
    ordering = ['nome']

class QuestionarioAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'texto')
    list_filter = ['tipo']
    search_fields = ('texto',)

class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo','nome']
    ordering = ['nome']

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('username','nome','email', 'curso',)
    list_filter = ['curso']
    search_fields = ['username', 'nome', 'email']
    ordering = ['username']

class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'nome')
    search_fields = ['sigla', 'nome']

class AtribuicaoAdmin(admin.ModelAdmin):
    list_display = ('disciplina','professor', 'turma')
    list_filter = ['disciplina', 'semestre', 'professor']
    search_fields = ['disciplina', ] 
    

class PerguntaAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Dados', {'fields': ['tipo', 'questionario',]},),
        ('Pergunta', {'fields': ['texto',]},),
        ]
    search_fields = ['texto']
    list_display = ('texto', 'tipo',)
    list_filter = ['tipo', 'questionario']

class RespostaAdmin(admin.ModelAdmin):
    pass
    
class AlternativaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pergunta',)
    list_filter = ['pergunta',]
    search_fields = ['texto']
    ordering = ['pergunta']

#
#class RespostaAdmin(admin.ModelAdmin):
#    pass


#class GenreAdmin(admin.ModelAdmin):
#    list_display = ('name',)
#
#class MovieAdmin(admin.ModelAdmin):
#    fieldsets = [('General Info',      {'fields': ['title','title_br','pub_date', 'imdb']}),
#                 ('Plot',    {'fields': ['plot'], 'classes': ['collapse']}),
#                 ('Crew',    {'fields': ['cast', 'director']}),
#                 ('Genres',  {'fields': ['genres']}),
#                 ('Quality', {'fields': ['height', 'width']}),
#                 ('Path',    {'fields': ['path', 'owner']}),
#                 ]
#    list_display = ('title', 'title_br', 'year',)
#    list_filter = ['pub_date',]
#    search_fields = ['title', 'title_br']
#    date_hierarchy = 'pub_date'


#admin.site.register(Curso, CursoAdmin)
admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Atribuicao, AtribuicaoAdmin)
admin.site.register(Questionario, QuestionarioAdmin)
admin.site.register(Pergunta, PerguntaAdmin)
admin.site.register(Resposta, RespostaAdmin)
admin.site.register(Alternativa, AlternativaAdmin)

