# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from caco.sad import models
from gdadefs import *

def preencheDisciplina(request, req_sigla):
    discs = models.Disciplina.objects.filter(sigla=req_sigla)
    d = discs[0]  # sera lidado uma disciplina por vez no questionario                                                                                                                                           
    pergs = models.Pergunta.objects.filter(questionario=d.questionario)
    pergL = []
    for p in pergs:
        alters = models.Alternativa.objects.filter(pergunta=p)
        alterL = []
        for a in alters:
            alterL.append({'id' : a.id, 'texto' : a.texto,})
        pergL.append({'id' : p.id, 'pergunta' : p.texto, 'alternativas' : alterL,})
    preencheD = {'sigla' : d.sigla, 'nome' : d.nome, 'perguntas' : pergL,}
    return render_to_response('preencheDisciplina.html', preencheD )

def salvaDisciplina(request, req_sigla, **get):
    return render_to_response('salvaDisciplina.html',  )

def show_all_semesters(request):
    semesters = ["Bla", "Creu", "GDA"]
    return render_to_response('sad/all_semesters.html', { 'semesters': semesters} )

def show_all_courses(request, ano, semestre):
    return render_to_response('sad/all_courses.html', { 'ano': ano , 'semestre': semestre } )


def show_all_answers(request, ano, semestre,disciplina):
    answers = ["Foi phoda!", "Dahab coxa!", "Anidao parcero!"]
    return render_to_response('sad/all_answers.html', 
                              { 'ano': ano , 
                                'semestre': semestre , 
                                'answers': answers ,
                                } 
                              )

def all_to_answer(request, ano, semestre):
    #disciplinas = models.Disciplina.objects.filter()  # apenas materia que o cara faz
    
    disciplinas = models.Disciplina.objects.all()
    #disciplinas = ['MC404', 'MC348', 'MC-Serginho']
    return render_to_response('sad/all_to_answer.html', 
                              { 'ano': ano , 
                                'semestre': semestre ,
                                'disciplinas': disciplinas,
                                'answered':False,
                                }
                              )

def answer_course(request, ano, semestre, disciplina):
    discs = models.Disciplina.objects.filter(sigla=disciplina)
    try:
        d = discs[0]  # sera lidado uma disciplina por vez no questionario
        pergs = models.Pergunta.objects.filter(questionario=d.questionario)
        pergL = []
        for p in pergs:
            if p.tipo == 'A':  # alternativa 
                alters = models.Alternativa.objects.filter(pergunta=p)
                alterL = []
                for a in alters:
                    alterL.append({'id' : a.id, 'texto' : a.texto,})
                pergL.append({'id' : p.id, 'pergunta' : p.texto, 'alternativas' : alterL,})
            else:
                pergL.append({'id' : p.id, 'pergunta' : p.texto, })
        return render_to_response('sad/answer_course.html',
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'disciplina': disciplina,
                                    'perguntas': pergL,
                                    'nome': d.nome,
                                    } 
                                  )
    except:
        return render_to_response('sad/consistency_error.html', {} )

def commit_answer_course(request, ano, semestre, disciplina):
    if request.GET:  # se houver respostas
        for resp in request.GET:
            if resp.startswith('pa'):  # alternativas
                p_id = resp.replace('pa','')
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                r = models.Resposta(pergunta=perg, alternativa=request.GET[resp], semestre=dbSemester(semestre,ano))
                r.save()
            else:  # dissertativa
                p_id = resp.replace('pd','')
                perg = models.Pergunta.objects.filter(id=p_id)[0]
                r = models.Resposta(pergunta=perg, texto=request.GET[resp], semestre=dbSemester(semestre,ano))
                r.save()
        return render_to_response('sad/all_to_answer.html', 
                              { 'ano': ano , 
                                'semestre': semestre ,
                                'disciplinas': disciplina,
                                'answered':True,
                                }
                              )
    else:
        return render_to_response('sad/consistency_error.html', {} )
