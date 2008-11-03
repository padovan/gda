#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import sys, os
import mechanize
#import urllib2
import string
from random import choice
from sha1 import new

from caco.sad.models import *

# TODO: 1. melhorar as espressões regulares

DRE_ALL_DISC = '<a href=".*.htm">(?P<disc_id>[A-Z][A-Z ][0-9]{3,3})(?P<disc_nome>.*)  '

#var token = "319afb0f735e9927e685b7f048e9394d"; (exemplo)
DRE_TOKEN = 'var token = "((?P<token>[0-9a-f]{32,32}))";'
DRE_TURMAS = '<tr height="18">[\\t\\n ]*<td height="18" bgcolor="white" width="100" align="center" class="corpo">(?P<turma>[A-Z1-9#])</td>'
DRE_FILE = '(?P<site>fileDownloadPublico\.do)'
DRE_ALUNO = '(?P<ra>[0-9]{5,7})[ ]*\\t(?P<nome>.*)[ ]*\\t(?P<curso>[0-9][0-9])\\t(?P<nivel>[A-Z])'
DRE_PROF = 'Docente: (?P<docente>.*)\\r\\n'
DRE_HOR_POS = '\<a href="(?P<pos_hor>[MD][0-9]{5,5}\.htm)"\>'
DRE_HOR_POS_DETAIL = '<font size=-1>(?P<disc_id>[A-Z][A-Z ][0-9]{3,3})(?P<disc_nome>.*)   </font>'



def iconv_file(file, name):

    f = open(name + ".ascii", 'w')
    f.write(file) 
    f.close()
    os.system("iconv -f iso8859-1 -t utf-8 " + name + ".ascii >" + \
            name + ".utf8")
    f = open(name + ".utf8", 'r')
    r = f.read()
    f.close()
    os.remove(name + ".utf8")
    os.remove(name + ".ascii")
    return r


def get_site(base, file):

    # FIXME: Fiz uma pequena gambiarra para pode pegar os dados em utf-8
    # Troquei o código abaixo pelo wget da página e um iconv
    #s_disc = urllib2.urlopen(SITE_HOR).read().encode('iso8859-1').decode('utf-8')
    os.system("wget " + base + file + " 2&> /dev/null")
    os.system("iconv -f iso8859-1 -t utf-8 " + file + " > " + file + ".utf8")
    f = open(file + ".utf8")
    site = f.read()
    f.close()
    os.remove(file + ".utf8")
    os.remove(file)
    return site


def add_disciplina(ld):

    # questionário default
    q = Questionario.objects.get(tipo='default')
    # inclui Disciplina no BD e cria lista com elas
    r = []
    for l in ld:
        p = Disciplina(sigla = l[0], nome = l[1], questionario = q)
        p.save()
        r.append(l[0])
    return r


# primeira parte: Descubrir as disciplinas de um dado semestre

# Estamos descobrindo quais são as disciplinas de cada semestre através do site
# da DAC. Lá a página para ver o horário da grad e diferente do da pós. Nao pós
# existem várias modalidades de mestrado e doutorado enquanto na grad não. Por
# isso duas funções aqui: get_disc_grad() and get_disc_pos().

def get_disc_grad():
    
    getbase = BASE_SITE
    getfile = INSTITUTO + ".htm"
    s_disc = get_site(getbase, getfile)
    
    d_all_disc = re.compile(DRE_ALL_DISC)
    # gera lista de disciplinas
    l_disc = re.findall(d_all_disc, s_disc)
    r = add_disciplina(l_disc)
    return r


def get_disc_pos():
    getbase = BASE_SITE
    getfile = INSTITUTO + ".htm"
    s_disc = get_site(getbase, getfile)
    d_file = re.compile(DRE_HOR_POS)
    pages = re.findall(d_file, s_disc)
    r = []
    for p_hor in pages:
        site = get_site(getbase, p_hor)
        d_all_disc = re.compile(DRE_HOR_POS_DETAIL)
        # gera lista de disciplinas 
        l_disc = re.findall(d_all_disc, site)
        d = add_disciplina(l_disc)
        r = r + d
    return r


# dada uma disciplina, get_matriculados descobre quais as turmas existentes e
# a partir desses dados descobre todos os dados sobre cada turma (alunos,
# matriculados e professor)
def get_matriculados(disc):

    mech = mechanize.Browser()
    mech.set_handle_robots(False)

    r = mech.open("http://www.daconline.unicamp.br/altmatr/menupublico.do")
    # encontra o token (hash dinamico para acesso)
    site = r.read()
    dtoken = re.compile(DRE_TOKEN)
    m = re.search(dtoken, site)
    if m is None:
        print "Falhou! O site da DAC mudou a API?"
        # FIXME: gerar algum erro aqui
    token = m.group('token')

# preenche o formulário pra pegar as turmas
    res1 = mech.open("http://www.daconline.unicamp.br/altmatr/conspub_situacaovagaspordisciplina.do?org.apache.struts.taglib.html.TOKEN=" + token + "&txtDisciplina=" + disc + "&txtTurma=V&cboSubG=" + SEMGRAD + "&cboSubP="+ SEMPOS + "&cboAno=" + ANO + "&btnAcao=Continuar")

# parseia o código da página e retira uma lista com as turmas
    site = res1.read()
    dturma = re.compile(DRE_TURMAS)
    turma = re.findall(dturma, site)
   
    for t in turma:
        res2 = mech.open("http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN=" + token + "&txtDisciplina=" + disc  + "&txtTurma=" + t + "&cboSubG=" + SEMGRAD + "&cboSubP=" + SEMPOS + "&cboAno=" + ANO + "&btnAcao=Continuar")

        # verifica se a turma tem alunos, isto é,
        # se está disponivel o link DRE_FILE no site.
        s_file = res2.read()
        d_file = re.compile(DRE_FILE)
        m = re.search(d_file, s_file)
        if m is None:
            continue

        print "Processando %s%s" % (disc, t)

        # salva o arquivo com os dados da turma,
        # faz um iconv e abre de novo
        j = mech.open("https://www.daconline.unicamp.br/altmatr/fileDownloadPublico.do")
        s_turma = iconv_file(j.read(), disc + t)

        dprof = re.compile(DRE_PROF)
        m = re.search(dprof, s_turma)
        
        # inclui o docente no BD
        s = Professor.objects.filter(nome=m.group('docente')) 
        if len(s) == 0:
            Professor(nome=m.group('docente')).save()
        
        p = Professor.objects.filter(nome=m.group('docente'))
        d = Disciplina.objects.filter(sigla=disc)

        dalu = re.compile(DRE_ALUNO)
        alunos = re.findall(dalu, s_turma)
        # cria a atribuicao
        at = Atribuicao(disciplina = d[0], professor = p[0], turma=t, semestre='2008-08-01')
        at.save()
        #inclui os alunos
        for i in alunos:
            ra = i[0]
            if len(ra) == 5:
                ra = '0' + ra
            email = (i[1][0]).lower()
            if email not in []:
                print 'Digite a letra do cara: i', i[1]
                email = raw_input()
            email = email + ra + '@dac.unicamp.br' 
            al = Aluno.objects.filter(username=ra)
            if not al:
                al = Aluno(username=ra, nome= i[1],  curso= i[2])
                al.save()
                at.aluno.add(al)
            else: 
                at.aluno.add(al[0])
            

#main()
# O instituto será fornecido no futuro via inteface administrativa do django.
# Por enquanto temos:

INSTITUTO='IC'
ANO='2008'
SEMESTRE='2'


## GRAD #
SEMGRAD = SEMESTRE
SEMPOS = '0'
NIVEL = 'G'
BASE_SITE = "http://www.dac.unicamp.br/sistemas/horarios/grad/G" \
    + SEMESTRE + "S0/"

ld = get_disc_grad()
for d in ld:
    get_matriculados(d)
## fim GRAD #


## POS #
SEMGRAD = '0'
SEMPOS = SEMESTRE
SEMPOS = '2' + SEMESTRE
NIVEL =  'P'
BASE_SITE = "wget http://www.dac.unicamp.br/sistemas/horarios/pos/P" \
    + SEMESTRE + "S/"

ld = get_disc_pos()
for d in ld:
    get_matriculados(d)
## fim POS #   

print "Done."

