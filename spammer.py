#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

spamMsg = u"""
Olá %(nome)s,

Gostaríamos de informar que o seu usuário no sistema do GDA é: "%(user)s" com senha "%(pass)s" (sem as aspas) e para acessar o GDA acesse:

	www.caco.ic.unicamp.br/gda

Você poderá responder os questionários das seguintes disciplinas:
%(discs)s

Infelizmente nosso sistema não permite ainda que as respostas sejam salvas parcialmente. Portanto uma vez que você começou a responder o questionário faça o até o fim. Pedimos desculpa por isso e estamos trabalhando para que no semestre que vem isso não aconteça.

Obrigado por contribuir

CACo - Centro Acadêmico da Computação
gestao@caco.ic.unicamp.br | www.caco.ic.unicamp,br
"""

tmpFile = u'/tmp/gdaLogin'
subjText = u'Login do GDA'

def main():
	import os, re, time
	from caco.sad.models import Aluno, Atribuicao

	alunos = [i.strip().split(' ') for i in open('alunos.passwd').readlines()]
	total = len(alunos)

	spamFill = {}
	for n, ra in enumerate(alunos):
		# pegando o aluno
		aluno = Aluno.objects.filter(username=ra[0])[0]
		# pegando o primeiro nome
		nome = aluno.nome.split(' ')[0]
		# pegando as disciplinas
		discs = ['%s - %s' % (d.disciplina.sigla, d.disciplina.nome.strip()) 
			for d in Atribuicao.objects.filter(aluno=aluno)]

		spamFill['nome'] = nome
		spamFill['user'] = ra[0]
		spamFill['pass'] = ra[1]
		spamFill['discs'] = '\n'.join(discs)

		# trabalhando com a mensagem em um arquivo
		handle = open(tmpFile, 'w')
		spamText = spamMsg % spamFill
		handle.write(spamText.encode('utf8'))
		handle.close

		# envia o e-mail
		email = ' '.join(ra[2:]) # pega todos os emails
		sendInfo = {
			'to' : email,
			'subj' : subjText,
			'fn' : tmpFile
		}
		print u'Enviando spam %d/%d do usuário %s (%s)' % (n, total, ra[0], nome)
		# Modo 4real
		#os.system('mutt %(to)s -s "%(subj)s" < %(fn)s' % sendInfo)
		# Modo dry-run
		print 'mutt "%(to)s" -s "%(subj)s" < %(fn)s' % sendInfo
		# end Modo
		time.sleep(0.1)  # sem flood né

		# remove o arquivo
		os.remove(tmpFile)	

if __name__ == "__main__":
	main()

