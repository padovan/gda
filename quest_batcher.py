#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recent
"""

# Código feito para >=python2.5

def main(argv = [__name__,]):
	from sad.models import Questionario, Pergunta, Alternativa
	from os import path

	for tipo in ['estagio','praticas','teoricas','teoricas_praticas']:
		print "Cadastrando perguntas do questionário %s" % tipo
		# pega o questionario
		try:
			q = Questionario.objects.filter(tipo=tipo)[0]
		except:
			# no existe esto questionario!!!
			q = Questionario(tipo=tipo, texto=tipo, semestre='2008-08-01')
			print q
			q.save()
		# prepara as questoes
		filename = path.join('questionarios', tipo)
		content = open(filename).read().splitlines()
		for question in content:
			# detecta qual o tipo de questão
			if question.find('$') > 0:
				# dissertativa
				text = question.split(' $')[0]
				question_type = 'D'
			elif question.find('#') > 0:
				# alternativa
				text, alterns = question.split(' # ')
				alterns = alterns[1:-1].split(',')  # tirei o '(' e ')'
				question_type = 'A'
			else:
				print "Deu pau aqui!!! Não casou dissertativo ou alternativa: %s" % question
				return
			# removendo as aspas duplas da pergunta
			text = text.split('"')[1]
			# cria a pergunta, se ainda não existir
			try:
				p = Pergunta.objects.filter(texto=text,tipo=question_type,questionario=q)[0]
				print "\tQuestão %d/%d já era cadastrada!" % (content.index(question), len(content))
			except:
				# no existe esta pregunta!!!
				p = Pergunta(texto=text,tipo=question_type)
				p.save()  # pra adicionar um n:n precisa ter a key antes
				p.questionario.add(q)
				p.save()  # agora salva com o questionário
				print "\tCadastrado questão %d/%d" % (content.index(question), len(content))
			# opa, sendo alternativa tem mais coisa...
			if question_type == 'A':
				print "\t\tCadastrando %d alternativas..." % (len(alterns)),
				# cadastra cada alternativa, se não existir ainda
				for altern in alterns:
					try:
						a = Alternativa.objects.filter(texto=altern,pergunta=p)[0]
					except:
						# no existe esta pregunta!!!
						a = Alternativa(texto=altern,pergunta=p)
						a.save()
				print "Feito!"
	# done!

if __name__ == "__main__":
    from sys import argv
    main(argv)
