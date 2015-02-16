import time
import sys
import xml.dom.minidom

MAX_SIZE = 1000000000.000

#begin = date.today()
#s_in = input("Enter name of input file\n")
s_in = sys.argv[1]
#s_out = input("Enter name of output file\n")
s_out = sys.argv[2]

f = open(s_in, 'r')
f1 = open(s_out, 'w')

##### READING
doc = xml.dom.minidom.parse(f)
#print(doc)

elements_nets = doc.getElementsByTagName('net')
#print(elements_nets)
#print(elements_nets.length)
#f1.print(elements_nets.length)



###### MASS INIT
long = elements_nets.length
i = 0
A = []
while i < long:
    A.append([])
    j = 0
    while j < long:
        A[i].append(MAX_SIZE)
        j = j+1
    i = i+1

###### END MASSS
###### INITITALIZING
i = 0
while i < long:
    A[i][i] = 0
    i = i+1

###### RESISTORS (READ &  FILL)
resistors = doc.getElementsByTagName('resistor')

for t in resistors:
    #print(t)
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = A[en][be] = 1/(1/A[be][en]+1/size)
    #print(be,en,size)


###### CAPACTORS (READ &  FILL)

capactors = doc.getElementsByTagName('capactor')

for t in capactors:
    #print(t)
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = A[en][be] = 1/(1/A[be][en]+1/size)
    #print(be,en,size)


###### DOIDES (READ &  FILL)

diodes = doc.getElementsByTagName('diode')

for t in diodes:
    #print(t)
    be = int(t.getAttribute('net_from'))-1
    en = int(t.getAttribute("net_to"))-1
    size = float(t.getAttribute('resistance'))
    A[be][en] = 1/(1/A[be][en]+1/size)
    size = float(t.getAttribute('reverse_resistance'))
    A[en][be] = 1/(1/A[en][be]+1/size)
    #print(be,en,size)

# test - working
# a = f.read();
#f1.write('new ' + a + ' string')

k = 0
while k < long:
    i = 0
    while i < long:
        j = 0
        while j < long:
            if i != j:
                A[i][j] = 1/(1/A[i][j]+1/(A[i][k]+A[k][j]))
            j = j+1
        i = i+1
    k = k+1

#####################   OUTPUT
for row in A:
    for col in row:
        #s = "{0:f}".format(col)
        #f1.write(s)
        #f1.write(str(col)+',')
        f1.write("{0:f},".format(col))
    f1.write("\n")



f.close()
f1.close()
#end  = datetime.time()

print(' Time(ms) : ', (time.process_time()*1000))
t = input()
