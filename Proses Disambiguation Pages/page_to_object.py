import re
from IPython import embed

class Page(object):

	def __init__(self, page_id, title):
		self.title = title
		self.page_id = page_id
		self.meanings = []

	def add_meaning(self, meaning):
		self.meanings.append(meaning)


def ugly_title_taker(the_line):
	title = ''
	start = False
	for i in range(len(the_line)):
		index = len(the_line)-i-1
		if(the_line[index] == '"' and start):
			return title
		elif(the_line[index] == '"'):
			title = the_line[index] + title
			start = True
		else:
			title = the_line[index] + title

def title_cleaner(dirty_title):
	titles = dirty_title.split(' ')
	clean_title = ''
	for x in range(len(titles)):
		if (x == len(titles)-1):
			break
		else:
			clean_title = clean_title + ' ' + titles[x]
	return clean_title[1:]

def id_taker(the_line):
	m = re.match(r'<doc id="(.*)"', the_line)
	the_line = m.group(1)
	result = ''
	for x in range(len(the_line)):
		if(the_line[x] == '"'):
			break
		result = result + the_line[x]
	return result

def bracket_remover(the_line):
	return (the_line.replace('[[','')).replace(']]','').rstrip('\r\n')


def list_cleaner(li):
	m = re.match(r"- (.*)", li)
	return m.group(1)

def get_disambiguation_list(title, line):
	m = re.findall("\[\[(.*)("+ title +")(.*)\]\]", line)
	if(m):
		first_match = m[0]
		str_result = ''
		for i in first_match:
			str_result += i
		str_result = str_result.split(']]')[0]
		# handling |
		return str_result.split('|')[0]
	return line


page = None
f = open('disambiguation_pages.txt','r')
record = False
arr_of_pages = {}
page = None

for line in f:
	if "<doc" in line:
		record = True
		title = ugly_title_taker(line)
		page_id = id_taker(line)
		page = Page(page_id, title_cleaner(title))
		arr_of_pages[page_id] = page
	if "</doc>" in line:
		record = False
		page = None
	if record and "<doc" not in line:
		if "- " in line and (line[0] == "-") and page.title in line:
			meaning = get_disambiguation_list(page.title, list_cleaner(line))
			if (page.title + " (") in meaning or meaning == page.title:
				page.meanings.append(meaning)

deleted_keys = []

for key in arr_of_pages.keys():
	if len(arr_of_pages[key].meanings) == 0:
		deleted_keys.append(key)

for key in deleted_keys:
	del arr_of_pages[key]


f.close()

# f2 = open('all_pages_one_paragraph.txt','r')
f2 = open('/Users/macbook/Documents/Data_Skripsi/Wikipedia/Idwiki/output/all_pages_full_page.txt','r')
all_pages = {}
key = None
for line in f2:
	line = line.rstrip("\n\r")
	if "==========" in line:
		state = 1
	else:
		if state == 1:
			key = line
			state = 2
		elif state == 2:
			state = 0
			all_pages[key] = line 
			key = None



f2.close()


f3 = open('title-meaning-description.txt','w')
for key in arr_of_pages.keys():
	page = arr_of_pages[key]
	f3.write("##TITLE##"+page.title+"\n")
	for meaning in page.meanings:
		f3.write(meaning)
		if "(film" in meaning or "(lagu" in meaning or "(musik" in meaning or "(novel" in meaning or "(album" in meaning:
				f3.write("||ENTITY")
		else:
			if meaning in all_pages:
				# if the description is exist in wikipedia page
				if " "+meaning.lower()+" " in all_pages[meaning] or " "+page.title.lower()+" " in all_pages[meaning]:
					f3.write("||SENSE")
				else:
					#f3.write("||CHECKTAG\n")
					#f3.write(all_pages[meaning].split('.')[0]+"")
					f3.write("||ENTITY")
			else:
				# check with tagger (soon)
				f3.write("||UNKNOWN")
		f3.write("\n")
	f3.write("###############\n")

f3.close()

#embed()