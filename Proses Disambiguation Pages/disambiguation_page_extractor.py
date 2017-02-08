# for extracting disambiguation pages only

arr_of_folder = ['AA','AB','AC','AD','AE','AF','AG']
o = open('disambiguation_pages.txt','w')
for folder in arr_of_folder:
	if folder == 'AG':
		length = 23
	else:
		length = 100
	for x in range(length):
		if(x < 10):
			the_file = '0'+str(x)
		else:
			the_file = str(x)
		f = open(folder+'/wiki_'+the_file,'r')
		documents = []
		record = False
		for line in f:
			line = line.rstrip("\n\r")
			if line:
				if "(disambiguasi)\">" in line:
					record = True
					o.write(line+"\n")
				elif "</doc>" in line:
					if record:
						o.write(line+"\n")
					record = False
				else:
					if record:
						o.write(line+"\n")

o.close()
