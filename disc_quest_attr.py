#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Autor: Gustavo Serra Scalet
Licença: GPLv3 ou mais recente
"""

teoricas = [
	'MC348', 
	'MC448', 
	'MC522', 
	'MC526', 
	'MC668', 
	'MC704', 
	'MC722', 
	'MC822', 
	'MC823', 
	'MC878', 
	'MC898', 
	'MC910', 
	'MC938', 
	'MC998', 
	'MO405', 
	'MO417', 
	'MO422', 
	'MO441', 
	'MO637', 
]

praticas = [ 
	'MC427', 
	'MC715', 
]

teorico_praticas = [
	'MC102', 
	'MC202', 
	'MC326', 
	'MC336', 
	'MC404', 
	'MC436', 
	'MC514', 
	'MC536', 
	'MC542', 
	'MC548', 
	'MC636', 
	'MC750', 
	'MC906', 
	'MC930', 
	'MO640', 
]

estagio = [
	'MC019', 
	'MC030', 
	'MC032', 
	'MC040', 
	'MC041', 
	'MC050', 
	'MO669', 
	'MO800', 
]

topicos = [
	'MO805', 
	'MO806', 
	'MO809', 
	'MO815', 
	'MO818', 
	'MO825', 
	'MO827', 
	'MO829', 
	'MC914', 
	'MC918', 
	'MC919', 
	'MC953', 
	'MC964', 
	'MC976', 
]

teoricas.extend([
#No lo se - Grad
	'MC039', 
	'MC852', 
	'MC923', 
	'MC940', 
	'MC950', 
	'MC962', 
#No lo se - PosGrad
	'MO409', 
	'MO410', 
	'MO416', 
	'MO445', 
	'MO601', 
	'MO603', 
	'MO645', 
	'MO648', 
	'MO649', 
	'MO650', 
	'MO901', 
])

def main():
	from caco.sad.models import Disciplina, Questionario

	# montando um dicionário das matérias com o tipo de questionário delas
	discs = {}
	for tipo in ('teoricas', 'praticas', 'teorico_praticas', 'estagio', 'topicos'):
		for sigla in eval(tipo): # pega a lista com o nome da string
			discs[sigla] = tipo  # e.g discs['MC102'] = 'teorico-praticas'
	
	# adiciona o questionário correto para todas as matérias
	for sigla in discs:
		print 'Incluindo a disciplina %s no questionario %s' % (sigla, discs[sigla])
		d = Disciplina.objects.filter(sigla=sigla)[0]
		try:
			q = Questionario.objects.filter(tipo=discs[sigla])[0]
		except:
			# no existe esto questionario!!!
			q = Questionario(tipo=discs[sigla], texto=discs[sigla], semestre='2008-08-01')
			q.save()
		d.questionario = q
		d.save()

	# done!

if __name__ == "__main__":
	main()

