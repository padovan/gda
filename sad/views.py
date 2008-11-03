from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render_to_response
from caco.sad import models
from gdadefs import *

def show_all_semesters(request):
    semesters = ["Bla", "Creu", "GDA"]
    return render_to_response('sad/all_semesters.html', { 'semesters': semesters} )

def show_all_courses(request, ano, semestre):
    return render_to_response('sad/all_courses.html', { 'ano': ano , 'semestre': semestre } )


def show_all_answers(request, ano, semestre,disciplina):
    answers = ["Foi phoda!", "coxa!"]
    return render_to_response('sad/all_answers.html', 
                              { 'ano': ano , 
                                'semestre': semestre , 
                                'answers': answers ,
                                } 
                              )

def all_to_answer(request, ano, semestre, respondido = False):
    if request.user.is_authenticated():
        try:
            # procura o objeto aluno
            aluno = models.Aluno.objects.filter(username=request.user.username)[0]
            # pega as disciplinas desse semestre
            atribuicaoPadrao = models.Atribuicao.objects.filter(aluno=aluno, semestre=dbSemester(semestre, ano))
            # mostra apenas as disciplinas que ele ainda nao respondeu
            from md5 import new
            hash = new(request.user.username).hexdigest()
            atribuicao = []
            for atr in atribuicaoPadrao:
                # FIXME deveria ser mais limpo, um if
                if not models.Resposta.objects.filter(hash_aluno=hash, atribuicao=atr):
                    # remove a atribuicao ja respondida 
                    atribuicao.append(atr)
        except:
            # provavelmente o aluno nao esta fazendo nenhuma discplina
            atribuicao = []
        return render_to_response('sad/all_to_answer.html', 
                                  { 'ano': ano , 
                                    'semestre': semestre ,
                                    'disciplinas': atribuicao,
                                    'respondido': respondido,
                                    }
                                  )
    else:
        return render_to_response('sad/home.html',  {'logado': 0} )

def answer_course(request, ano, semestre, disciplina, turma):
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
                                    'turma': turma,
                                    'perguntas': pergL,
                                    'nome': d.nome,
                                    } 
                                  )
    except:
        return render_to_response('sad/consistency_error.html', {} )

def commit_answer_course(request, ano, semestre, disciplina, turma):
    if request.GET:  # se houver respostas
        atribuicao = models.Atribuicao.objects.filter(disciplina=disciplina,
                turma=turma, semestre=dbSemester(semestre,ano))[0]
        for resp in request.GET:
            from md5 import new
            hash = new(request.user.username).hexdigest()
            if resp.startswith('pa'):  # alternativas
                p_id = resp.replace('pa','')
                # FIXME gambiarra pra interface admin
                text = '' 
                alter = models.Alternativa.objects.filter(id=request.GET[resp])[0]
            else:  # dissertativa
                p_id = resp.replace('pd','')
                text = request.GET[resp]
                alter = None
            perg = models.Pergunta.objects.filter(id=p_id)[0]
            r = models.Resposta(pergunta=perg, texto=text, alternativa=alter,
                    hash_aluno=hash, atribuicao=atribuicao)
            r.save()
        return all_to_answer(request, ano, semestre, True)
    else:
        return render_to_response('sad/consistency_error.html', {} )

def home(request):
    if request.user.is_authenticated():
        # proceed if already authenticated
        return all_to_answer(request, '2008', '2') 
    else:
        return render_to_response('sad/home.html', {'error' : False,})
        

def login_auth(request):
    try:
        #if request.user.is_
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            #FIXME gambiarra
            return all_to_answer(request, '2008', '2') 
        else:
            # Show same error as an exception
            raise
    except:
        return render_to_response('sad/home.html', {'error' : True,})

def logout(request):
    auth.logout(request)
    return home(request)
