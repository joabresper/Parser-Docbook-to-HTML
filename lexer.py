#IMPORTS
import ply.lex as lex
import re
from menu import cls, menu_options, Menu_logic
from helpers import Request_route

# var errors control
error_counter = 0

#GRAMATICAL TERMINAL SYMBOLS
tokens = [
    # Tags
    'doctype',
    
    'article',
    'cArticle',
    
    'section',
    'cSection',
    
    'info',
    'cInfo',
    
    'simpleSection',
    'cSimpleSection',
    
    'title',
    'cTitle',
    
    'itemizedlist',
    'cItemizedlist',

    'important',
    'cImportant',
    
    'para',
    'cPara',
    
    'simpara',
    'cSimpara',

    'address',
    'cAddress',

    'mediaObject',
    'cMediaObject',
    
	'videoObject',
    'cVideoObject',
    
	'imageObject',
    'cImageObject',
    
	'videoData',
    
    'imageData',

    'informalTable',
    'cInformalTable',
    
    'comment',
    'cComment',

    'abstract',
    'cAbstract',
    
    'author',
    'cAuthor',
    
    'date',
    'cDate',
    
    'copyright',
    'cCopyright',
    
    'street',
    'cStreet',
    
    'city',
    'cCity',
    
    'state',
    'cState',
    
    'phone',
    'cPhone',
    
    'email',
    'cEmail',
    
    'firstname',
    'cFirstname',
    
    'surname',
    'cSurname',
    
    'year',
    'cYear',
    
    'holder',
    'cHolder',
    
    'emphasis',
    'cEmphasis',
    
    'listItem',
    'cListItem',
    
    'tgroup',
    'cTgroup',
    
    'thead',
    'cThead',
    
    'tfoot',
    'cTfoot',
    
    'tbody',
    'cTbody',
    
    'row',
    'cRow',
    
    'entry',
    'cEntry',
    
    'entrytbl',
    'cEntrytbl',
     
    'link',
    'cLink',

    # Tags content
    'text',
]

#TOKEN FUNCTIONS
def t_doctype(t): r'<!DOCTYPE article>'; return(t);

def t_article(t): r'<article>'; return(t);
def t_cArticle(t): r'</article>'; return(t);

def t_section(t): r'<section>'; return(t);
def t_cSection(t): r'</section>';  return(t);

def t_info(t): r'<info>'; return(t);
def t_cInfo(t): r'</info>'; return(t);

def t_simpleSection(t): r'<simplesect>'; return(t);
def t_cSimpleSection(t): r'</simplesect>'; return(t);

def t_title(t): r'<title>'; return(t);
def t_cTitle(t): r'</title>'; return(t);

def t_itemizedlist(t): r'<itemizedlist>'; return (t);
def t_cItemizedlist(t): r'</itemizedlist>'; return (t);

def t_important(t): r'<important>'; return (t);
def t_cImportant(t): r'</important>'; return (t);

def t_para(t): r'<para>'; return (t);
def t_cPara(t): r'</para>'; return (t);

def t_simpara(t): r'<simpara>'; return (t);
def t_cSimpara(t): r'</simpara>'; return (t);

def t_address(t): r'<address>'; return (t);
def t_cAddress(t): r'</address>'; return (t);

def t_informalTable(t): r'<informaltable>'; return (t);
def t_cInformalTable(t): r'</informaltable>'; return (t);

def t_comment(t): r'<comment>'; return (t);
def t_cComment(t): r'</comment>'; return (t);

def t_abstract(t): r'<abstract>'; return (t);
def t_cAbstract(t): r'</abstract>'; return (t);

def t_author(t): r'<author>'; return (t);
def t_cAuthor(t): r'</author>'; return (t);

def t_date(t): r'<date>'; return (t);
def t_cDate(t): r'</date>'; return (t);

def t_copyright(t): r'<copyright>'; return (t);
def t_cCopyright(t): r'</copyright>'; return (t);

def t_street(t): r'<street>'; return (t);
def t_cStreet(t): r'</street>'; return (t);

def t_city(t): r'<city>'; return (t);
def t_cCity(t): r'</city>'; return (t);

def t_state(t): r'<state>'; return (t);
def t_cState(t): r'</state>'; return (t);

def t_phone(t): r'<phone>'; return (t);
def t_cPhone(t): r'</phone>'; return (t);

def t_email(t): r'<email>'; return (t);
def t_cEmail(t): r'</email>'; return (t);

def t_firstname(t): r'<firstname>'; return (t);
def t_cFirstname(t): r'</firstname>'; return (t);

def t_surname(t): r'<surname>'; return (t);
def t_cSurname(t): r'</surname>'; return (t);

def t_year(t): r'<year>'; return (t);
def t_cYear(t): r'</year>'; return (t);

def t_holder(t): r'<holder>'; return (t);
def t_cHolder(t): r'</holder>'; return (t);

def t_emphasis(t): r'<emphasis>'; return (t);
def t_cEmphasis(t): r'</emphasis>'; return (t);

def t_listItem(t): r'<listitem>'; return (t);
def t_cListItem(t): r'</listitem>'; return (t);

def t_tgroup(t): r'<tgroup>'; return (t);
def t_cTgroup(t): r'</tgroup>'; return (t);

def t_thead(t): r'<thead>'; return (t);
def t_cThead(t): r'</thead>'; return (t);

def t_tfoot(t): r'<tfoot>'; return (t);
def t_cTfoot(t): r'</tfoot>'; return (t);

def t_tbody(t): r'<tbody>'; return (t);
def t_cTbody(t): r'</tbody>'; return (t);

def t_row(t): r'<row>'; return (t);
def t_cRow(t): r'</row>'; return (t);

def t_entry(t): r'<entry>'; return (t);
def t_cEntry(t): r'</entry>'; return (t);

def t_entrytbl(t): r'<entrytbl>'; return (t);
def t_cEntrytbl(t): r'</entrytbl>'; return (t);

def t_mediaObject(t): r'<mediaobject>'; return (t);
def t_cMediaObject(t): r'</mediaobject>'; return (t);

def t_videoObject(t): r'<videoobject>'; return (t);
def t_cVideoObject(t): r'</videoobject>'; return (t);

def t_imageObject(t): r'<imageobject>'; return (t);
def t_cImageObject(t): r'</imageobject>'; return (t);

def t_imageData(t):
    r'<imagedata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    return (t)

def t_videoData(t):
    r'<videodata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    return (t)

def t_link(t):
    r'<link\s+xlink:href=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*>'
    return (t)

def t_cLink(t): r'</link>'; return (t);

def t_text(t): r'[^<>\n\r]+'; return (t)

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\r'

# Error handling rule
def t_error(t):
	global error_counter
	line_start = t.lexer.lexdata.rfind('\n', 0, t.lexpos) + 1
	column = find_column(t.lexer.lexdata, t)
	print(f'Ilegal element --> \'{t.value[0]}\' | Line: {t.lineno} | Pos: {column}')
	error_counter += 1
	t.lexer.skip(1)

def find_column(text, token):
    last_cr = text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr)
    return column

# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


#Input from file
def Analyze_from_file():
	cleanpath = Request_route()
	lexer = lex.lex(reflags=re.IGNORECASE) #ignore capital case and lowercase
	try:
		with open(cleanpath, "r", encoding='utf-8') as file:
			code = file.read()
		lexer.input(code)
		Token_analysis('file', lexer)
	except IOError:
		print('An error occurred trying to read the file: ', cleanpath)
	except FileNotFoundError:
		print(f'File not found: ', cleanpath)
	except Exception as e:
		print(f'Processing error: {str(e)}')

#Input from console
def Analyze_from_console():
	lexer = lex.lex(reflags=re.IGNORECASE) #ignore capital case and lowercase
	# normal excecution
	print('| End the execution: [Ctrl] + [c] |\n| Back to principal menu: _exit   |')
	while True:
		s = input('>> ')
		if s == '_exit':
			cls()
			break;
		lexer.input(s)
		Token_analysis('normal', lexer)

#Token analysis
def Token_analysis(excecution_mode, lexer):
	global error_counter
	export_arr = []
	while True:
		tok = lexer.token()
		if not tok:
			if excecution_mode=='file':
				Export_tokens(export_arr)
			break
		if excecution_mode=='file':
			export_arr.append([tok.type, tok.value, tok.lineno]);
		else:
			print(f'Type: {tok.type} | Value: {tok.value} | Line: {tok.lineno}')

#Exportation of tokens
def Export_tokens(arr):
	global error_counter
	file_name_export = f'analyzed-tokens.txt'
	with open(file_name_export, 'w', encoding='utf8') as f:
		f.write(' TOKEN    |    VALUE \n')
		f.write('---------------------\n')
		counter = 0
		for line in arr:
			counter += 1
			f.write(f'{counter}] {line[0]}: {line[1]} | Line: {line[2]}')
			f.write('\n')
		f.write('---------------------\n')
		f.write(f'Total number of tokens analyzed: {counter}\n')
		if error_counter>0:
			f.write(f'Number of errors found: {error_counter}')
	f.close()
	if error_counter>0:
		print('(XXXXX) Lexer does NOT accept the file (XXXXX)')
	else:
		print('(V) Lexer ACCEPT the file (V)')
	print('(!) A file was exported with the recognized tokens.')


#----------------------------------------


if __name__ == '__main__':
 	Menu_logic(
 		'Lexer',
		menu_options,
		Analyze_from_file,
		Analyze_from_console,
	)
else:
	lexer = lex.lex(reflags=re.IGNORECASE)
