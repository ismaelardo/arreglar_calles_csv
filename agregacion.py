import csv, sys
tables_names = sys.argv[1:]
agrs = [] #cada elemento es una lista con las cantidades de datos que hay por cada uv.
for table in tables_names:
	with open(table) as csv_obj:
		f=csv.reader(csv_obj,delimiter = ',')
		agr=[0]*26
		next(f)
		for row in f:
			try:
				agr[int(row[5])-1]+=1
			except:
				pass
	agrs.append(agr)
with open('agregacion.csv','w',newline='') as csv_obj:
	csv_writer=csv.writer(csv_obj)
	csv_writer.writerow(['UV','PENDIENTES','RESUELTOS'])
	
	for i, ag in enumerate(agrs[0]):
		row =[0]
		row[0] = str(i+1)
		for list_uv in agrs:
			row.append(list_uv[i])
		csv_writer.writerow(row)