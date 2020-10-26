import Levenshtein
import csv,sys
archivo_calles=sys.argv[1]
col_calles = int(sys.argv[2])

def numero_en_nombre(nombre):
	prefix = []
	aux = False
	dict_nums = {'1 ': 'UNO','2 ': 'DOS','3 ': 'TRES','4 ': 'CUATRO','5 ': 'CINCO','6 ': 'SEIS',
	'7 ': 'SIETE','8 ': 'OCHO','9 ': 'NUEVE','10 ': 'DIEZ','11 ': 'ONCE','12 ': 'DOCE',
	'13 ': 'TRECE','14 ': 'CATORCE','15 ': 'QUINCE','16 ': 'DIECISEIS','17 ': 'DIECISIETE'}
	for num in dict_nums:
		if num in nombre:
			aux = True
			prefix.append(num)
	if aux:		
		#print(nombre)
		nombre = dict_nums[max(prefix,key=len)] + nombre[len(max(prefix, key=len))-1:]
		#print(nombre)
	return nombre		

		
def subpertenencia(nombre1,nombre2):
	if nombre1 in nombre2 or nombre2 in nombre1:
		#print(f'nombre_denuncia: {nombre1}, nombre en street-uv: {nombre2}')
		return nombre2	

def mejor_levenshtein(calle_d,lista_calles):
	distancia_menor_calle = [100,''] # distancia, calle escogida

	for calle in lista_calles:
		#print(calle,calle_d)
		distancia = Levenshtein.distance(calle_d,calle)
		if  distancia < distancia_menor_calle[0]:
			distancia_menor_calle = [distancia,calle]
	return distancia_menor_calle

calles_bien = []
with open('streets-uv.csv') as csvfile:
	f = csv.reader(csvfile,delimiter=',')
	#print(f.next())
	for row in f:
		calles_bien.append(row[0])
	calles_bien = calles_bien[1:]	
with open(archivo_calles) as csvfile:
	f=list(csv.reader(csvfile, delimiter=','))
	#posibles_coincidencias=[]
	calles_denuncia = []
	distancia = [0]*(len(f)-1)
	#print(distancia)
	for row in f[1:]:
		calles_denuncia.append(row[col_calles])
	for i, calle_d in enumerate(calles_denuncia):	
		if calle_d != '0':
			if not calle_d.isupper():
				calles_denuncia[i]=calle_d.upper()
			coincidencias = []
			calles_denuncia[i]=numero_en_nombre(calles_denuncia[i])
			for calle in calles_bien:
				coincidencia = subpertenencia(calles_denuncia[i], calle)
				if coincidencia:
					coincidencias.append(coincidencia)
			#print('coin',coincidencias)		
			#print('cd',calles_denuncia[i])		
			#coincidencias.insert(0,calles_denuncia[i])		
			#posibles_coincidencias.append(coincidencias)
			if len(coincidencias) == 1:
				#print('pos',posibles_coincidencias)
				calles_denuncia[i] = coincidencias[0]
			[distancia[i], calles_denuncia[i]]=mejor_levenshtein(calles_denuncia[i],calles_bien)
	#i = 0		
	#for row in f[1:]:
	#	if distancia[i]>1:
	#		print('antigua: ',row[3],'nueva: ',calles_denuncia[i], 'distancia:',distancia[i])		
	#	i+=1
			#print(calle_d)	
with open(archivo_calles) as read_obj, open(archivo_calles[:-4]+'_MEJORADA.csv','w', newline='') as write_obj:
	# Create a csv.reader object from the input file object
	csv_reader = csv.reader(read_obj)
	# Create a csv.writer object from the output file object
	csv_writer = csv.writer(write_obj)

	i=-1
	for row in csv_reader:
		#print(len(row))
		if i==-1:
			row.insert(col_calles+1,'CALLE_ARREGLADA')
			csv_writer.writerow(row)
		else:
			row.insert(col_calles+1,calles_denuncia[i])
			csv_writer.writerow(row)
		#print(len(row))	
		i += 1
			

