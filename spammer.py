#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

spamMsg = """
Olá%(nome)s,

Gostaríamos de informar que o seu usuário é: "%(user)s" com senha "%(pass)s" (sem as aspas)
"""

tmpFile = '/tmp/gdaLogin'
subjText = 'Login do GDA'

def main():
	import os, re, time
	alunos = [i.strip().split(' ') for i in open('alunos.passwd').readlines()]
	total = len(alunos)

	spamFill = {}
	for n, aluno in enumerate(alunos):
		try:
			nome = os.popen('finger ' + aluno[3].split('@')[0])  # 'finger raxxxxxx'
			nome = nome.readlines()[0]  # primeira linha que contém o 'Name: '
			nome = ' %s' % re.sub(r'.*Name: ([^ ]*).*\n.*', r'\1', nome)  # precisa de um espaço
		except:
			nome = ''
		spamFill['nome'] = nome
		spamFill['user'] = aluno[0]
		spamFill['pass'] = aluno[1]

		# trabalhando com a mensagem em um arquivo
		handle = open(tmpFile, 'w')
		handle.write(spamMsg % spamFill)
		handle.close

		# envia o e-mail
		try:
			email = '%s %s' % aluno[2:4] # pega o terceiro e quarto campo
		except TypeError:
			email = aluno[2]
		sendInfo = {
			'to' : email,
			'subj' : subjText,
			'fn' : tmpFile
		}
		print 'Enviando spam %d/%d' % (n, total)
		#os.system('mutt %(to)s -s "%(subj)s" < %(fn)s' % sendInfo)
		print 'mutt "%(to)s" -s "%(subj)s" < %(fn)s' % sendInfo
		time.sleep(0.1)  # sem flood né

		# remove o arquivo
		os.remove(tmpFile)
	

if __name__ == "__main__":
	main()

