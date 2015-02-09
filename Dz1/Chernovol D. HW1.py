from time import gmtime
begin = gmtime()
s_in = input("Enter name of input file\n")

s_out = input("Enter name of output file\n")

f = open(s_in, 'r')
f1 = open(s_out, 'w')

a = f.read();

f1.write('new ' + a + ' string')
f.close()
f1.close()
end  = gmtime()


print(' Time(ms) : ', (end.tm_sec - begin.tm_sec) *1000)
t = input();
