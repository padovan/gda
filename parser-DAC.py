#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import sys, os
import mechanize
import urllib2
from time import sleep

from caco.sad.models import *

# TODO: 1. melhorar as espressões regulares

DRE_ALL_DISC = '<a href=".*.htm">(?P<disc_id>[A-Z][A-Z ][0-9]{3,3})(?P<disc_nome>.*)  '

#var token = "319afb0f735e9927e685b7f048e9394d"; (exemplo)
DRE_TOKEN = 'var token = "((?P<token>[0-9a-f]{32,32}))";'
DRE_TURMAS = '<tr height="18">[\\t\\n ]*<td height="18" bgcolor="white" width="100" align="center" class="corpo">(?P<turma>[A-Z1-9#])</td>'
DRE_FILE = '(?P<site>fileDownloadPublico\.do)'
DRE_ALUNO = '(?P<ra>[0-9]{5,7})[ ]*\\t(?P<nome>.*)[ ]*\\t(?P<curso>[0-9][0-9])\\t(?P<nivel>[A-Z])'
DRE_PROF = 'Docente: (?P<docente>.*)\\r\\n'



# O instituto será fornecido no futuro via inteface administrativa do django
# por ora temos
INSTITUTO='IC'
SEMGRAD=['1']
SEMPOS=['-1']
NIVEL='G'
ANO=['2008']

if NIVEL == 'G':
    SITE_HOR = "http://www.dac.unicamp.br/sistemas/horarios/grad/G" \
    + SEMGRAD[0] + "S0/"+  INSTITUTO + ".htm"
else:
    SITE_HOR = "wget http://www.dac.unicamp.br/sistemas/horarios/pos/P" \
    + SEMPOS[0] + "S/"+  INSTITUTO + ".htm"


# primeira parte: Discubrir as disciplinas de um dado semestre
def all_disc():
    
    # FIXME: Fiz uma pequena gambiarra para pode pegar os dados em utf-8
    # Troquei o código abaixo pelo wget da página e um iconv
    #s_disc = urllib2.urlopen(SITE_HOR).read().encode('iso8859-1').decode('utf-8')

    # Aqui começa a gambiarra
    os.system("wget " + SITE_HOR + " > /dev/null")
    os.system("iconv -f iso8859-1 -t utf-8 " + INSTITUTO + ".htm >" +  INSTITUTO + ".utf8")
    f = open(INSTITUTO + ".utf8")
    s_disc = f.read()
    f.close()
    os.remove(INSTITUTO + ".utf8")
    os.remove(INSTITUTO + ".htm")
    # aqui termina 
    
    d_all_disc = re.compile(DRE_ALL_DISC)
    l_disc = re.findall(d_all_disc, s_disc)
    r = []
    # questionário default
    q = Questionario.objects.get(tipo='default')
    # inclui Disciplina no BD e cria lista com elas
    for l in l_disc:
        p = Disciplina(sigla = l[0], nome = l[1], questionario = q)
        p.save()
        r.append(l[0])
    return r


def get_matriculados(txtDisciplina):

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
    res1 = mech.open("http://www.daconline.unicamp.br/altmatr/conspub_situacaovagaspordisciplina.do?org.apache.struts.taglib.html.TOKEN=" + token + "&txtDisciplina=9&txtTurma=a&cboSubG=" + SEMGRAD[0] + "&cboSubP=-1")

    mech.select_form("FormSelecionarNivelPeriodoDisciplina")
    mech["cboSubG"] = SEMGRAD
    #mech["cboSubP"] = SEMPOS
    mech["cboAno"] = ANO
    mech["txtDisciplina"]  = txtDisciplina
    res1 = mech.submit()

# parseia o código da página e retira uma lista com as turmas
    site = res1.read()
    dturma = re.compile(DRE_TURMAS)
    turma = re.findall(dturma, site)
   
    for t in turma:
        res2 = mech.open("http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do?org.apache.struts.taglib.html.TOKEN=" + token + "&txtDisciplina=9&txtTurma=a&cboSubG=" + SEMGRAD[0] + "&cboSubP=-1")

        mech.select_form("FormSelecionarNivelPeriodoDisciplina")
        mech["cboSubG"] = SEMGRAD
        #mech["cboSubP"] = SEMPOS
        mech["cboAno"] = ANO
        mech["txtDisciplina"] = txtDisciplina
        mech["txtTurma"] = t
        res3 = mech.submit()

        # verifica se a turma tem alunos, isto é,
        # se está disponivel o link DRE_FILE no site.
        s_file = res3.read()
        d_file = re.compile(DRE_FILE)
        m = re.search(d_file, s_file)
        if m is None:
            continue

        print "Processando %s%s" % (txtDisciplina, t)

        # salva o arquivo com os dados da turma,
        # faz um iconv e abre de novo
        j = mech.open("https://www.daconline.unicamp.br/altmatr/fileDownloadPublico.do")
        f = open(txtDisciplina + t + ".ascii", 'w')
        f.write(j.read()) 
        f.close()
        os.system("iconv -f iso8859-1 -t utf-8 " + txtDisciplina + t + ".ascii >" + \
                txtDisciplina + t + ".utf8")
        f = open(txtDisciplina + t + ".utf8", 'r')
        s_turma = f.read()
        f.close()
        os.remove(txtDisciplina + t + ".utf8")
        os.remove(txtDisciplina + t + ".ascii")

        dprof = re.compile(DRE_PROF)
        m = re.search(dprof, s_turma)
        

        # inclui o docente no BD
        s = Professor.objects.filter(nome=m.group('docente')) 
        if len(s) == 0:
            Professor(nome=m.group('docente')).save()
        
        p = Professor.objects.filter(nome=m.group('docente'))
        d = Disciplina.objects.filter(sigla=txtDisciplina)

        dalu = re.compile(DRE_ALUNO)
        alunos = re.findall(dalu, s_turma)
        at = Atribuicao(disciplina = d[0], professor = p[0], turma=t, semestre='2008-08-01')
        at.save()
        for i in alunos:
            al = Aluno(RA=i[0], nome= i[1], curso= i[2])
            al.save()
            at.aluno.add(al)
            



#main()
ld = all_disc()
for d in ld:
    get_matriculados(d)
print "Done."

