# -*- coding: utf-8 -*-

# Create your views here.

from django.shortcuts import render_to_response
from caco.sad import models

def selecionaDisciplina(request):
    discs = models.Disciplina.objects.all()
    return render_to_response('selecionaDisciplina.html', {'disciplinas' : discs,} )

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
