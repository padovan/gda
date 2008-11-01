# GDA Functinos

def dbSemester(semestre, ano):
    # transforma o semestre 1 ou 2 em datas, coerente com o banco
    if semestre == '1': # semestre impar
        return '%s-01-01' % ano
    else: # semestre par
        return '%s-08-01' % ano
    
