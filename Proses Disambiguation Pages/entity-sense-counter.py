f = open('title-meaning-description.txt','r')
cnt_e = 0
cnt_s = 0

for line in f:
	if "||ENTITY" in line:
		cnt_e += 1
	elif "||SENSE" in line:
		cnt_s += 1

print "Entity:",cnt_e
print "Sense:",cnt_s
print "Ration E/D:",float(float(cnt_e)/cnt_s)

f.close()
