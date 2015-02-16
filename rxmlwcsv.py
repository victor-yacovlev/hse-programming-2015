import time
import sys
import xml

start = int(round(time.time()*1000))

def im_xml_csv(argv):
	inname = argv[0]
	outname = argv[1]
	
	from xml.etree import ElementTree
	tree = ElementTree.parse(inname)
	elem = tree.findall('.//net')
	n = len(elem)
	diods = tree.findall('.//diode')
	nd = len(diods)
	dic = {}
	for i in range(nd):
		first = int(diods[i].get('net_from'))
		last = int(diods[i].get('net_to'))
		num = float(diods[i].get('resistance'))
		numrev = float(diods[i].get('reverse_resistance'))
		dic[(first, last)] = num
		dic[(last, first)] = numrev
	resist = tree.findall('.//resistor')
	nr = len(resist)
	for i in range(nr):
		first = int(resist[i].get('net_from'))
		last = int(resist[i].get('net_to'))
		num = float(resist[i].get('resistance'))
		dic[(first, last)] = num
		dic[(last, first)] = num
	capact = tree.findall('.//capactor')
	nc = len(capact)
	for i in range(nc):
		first = int(capact[i].get('net_from'))
		last = int(capact[i].get('net_to'))
		num = float(capact[i].get('resistance'))
		dic[(first, last)] = num
		dic[(last, first)] = num
	inf = float('Inf')
	table = [[inf for i in range(n)] for j in range(n)]
	for i in range(n):
		table[i][i] = 0
	for key in dic:
		if table[key[0]-1][key[1]-1] == 0 or dic[key] == 0:
			table[key[0]-1][key[1]-1] = 0
		elif (1/table[key[0]-1][key[1]-1] + 1/dic[key]) == 0:
		    table[key[0]-1][key[1]-1] = inf
		else:
			table[key[0]-1][key[1]-1] = 1/(1/table[key[0]-1][key[1]-1] + 1/dic[key])
	for k in range(n):
		for i in range(n):
			for j in range(n):
				if table[i][j] == 0 and (table[i][k]+table[k][j]) == 0 :
					table[i][j] = 0
				elif table[i][j] == 0:
					table[i][j] = round(1/(inf + 1/(table[i][k]+table[k][j]) ), 6)
				elif (table[i][k]+table[k][j]) == 0:
					table[i][j] = round(1/(1/table[i][j] + inf),6)
				elif (1/table[i][j] + 1/(table[i][k]+table[k][j]) ) == 0:
				    table[i][j] = inf
				else:
					table[i][j] = round(1/(1/table[i][j] + 1/(table[i][k]+table[k][j])), 6)
	with open(outname, "w") as fl:
		for i in range(n):
			for j in range(n):
				if j == n-1:
					fl.write(str(table[i][j]))
				else:
					fl.write(str(table[i][j])+",")
			fl.write("\n")


im_xml_csv(sys.argv[1:])

finish = int(round(time.time()*1000))
print(finish-start)
