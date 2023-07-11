# imports
import ply.yacc as yacc
import lexer
from lexer import tokens

from importlib import reload
import re

from helpers import Request_route
from menu import Menu_logic, menu_options

# var errors control
error_counter = 0

# var traduced
export_txt = list()

#---- GRAMATICAL PRODUCTIONS ----#

def p_SIGMA(p): # distinguished symbol
    '''SIGMA : doctype ARTICLE
    '''
    export_txt.append(['Prod. SIGMA -->', p.slice])
    p[0] = f'{p[2]}'

def p_ARTICLE(p):
    '''ARTICLE : article INFO TITLEH1 CONT_A_S cArticle
				| article INFO TITLEH1 CONT_A_S SECTIONS cArticle           
				| article TITLEH1 CONT_A_S cArticle
                | article TITLEH1 CONT_A_S SECTIONS cArticle
                | article INFO CONT_A_S cArticle
                | article INFO CONT_A_S SECTIONS cArticle
                | article CONT_A_S cArticle
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p) == 5):
        p[0] = f'{p[2]}\n{p[3]}'
    elif(len(p) == 6):
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}'
    elif(len(p) == 7):
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}\n{p[5]}'   
    export_txt.append(['Prod. ARTICLE -->', p.slice])
    
def p_INFO(p):
    '''INFO : info CONT_INFO cInfo
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. INFO -->', p.slice])

def p_CONT_INFO(p):
    '''CONT_INFO : ELEM_INFO CONT_INFO
				| ELEM_INFO
    '''
    if(len(p) == 3):
        p[0] = f'<p style="background-color:green; color: white; font-size:8px">{p[1]}</p>\n{p[2]}'
    elif(len(p) == 2):
        p[0] = f'<p style="background-color:green; color: white; font-size:8px">{p[1]}</p>'
        
    export_txt.append(['Prod. CONT_INFO -->', p.slice])
    
def p_ELEM_INFO(p):
    '''ELEM_INFO : MEDIA_OBJECT
				| ABSTRACT
                | ADDRESS
                | AUTHOR
                | DATE
                | COPYRIGHT
                | TITLEH1
    '''
    export_txt.append(['Prod. ELEM_INFO -->', p.slice])
    p[0] = f'{p[1]}'
    
def p_SECTION(p):
    '''SECTION : section CONT_A_S cSection
				| section CONT_A_S SECTIONS cSection
				| section INFO CONT_A_S cSection
                | section INFO CONT_A_S SECTIONS cSection
                | section TITLEH2 CONT_A_S cSection
                | section TITLEH2 CONT_A_S SECTIONS cSection
                | section INFO TITLEH2 CONT_A_S cSection
                | section INFO TITLEH2 CONT_A_S SECTIONS cSection
                | section TITLEH2 cSection
    '''
    if(len(p) == 4):
        p[0] = f'<div>{p[2]}</div'
    elif(len(p) == 5):
        p[0] = f'<div>{p[2]}\n{p[3]}</div>'
    elif(len(p) == 6):
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}</div>'
    elif(len(p) == 7):
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}\n{p[5]}</div>'
    export_txt.append(['Prod. SECTION -->', p.slice])

def p_SECTIONS(p):
    '''SECTIONS : SECTION 
				| SECTION SECTIONS
                | SIMPLE_SEC
                | SIMPLE_SEC SECTIONS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. SECTIONS -->', p.slice])

def p_CONT_A_S(p):
    '''CONT_A_S : CONT_1
				| CONT_1 CONT_A_S
                | SECTION
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. CONT_A_S -->', p.slice])

def p_CONT_1(p):
    '''CONT_1 :   ITEMIZED_LIST
				| IMPORTANT
                | PARA
                | SIMPARA
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
                | COMMENT
                | ABSTRACT
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. CONT_1 -->', p.slice])

def p_SIMPLE_SEC(p):
    '''SIMPLE_SEC : simpleSection CONT_SS cSimpleSection
				| simpleSection INFO CONT_SS cSimpleSection
                | simpleSection TITLE CONT_SS cSimpleSection
                | simpleSection INFO TITLE CONT_SS cSimpleSection
    '''
    if len(p)==4:
        p[0] = f'<div>{p[2]}</div'
    elif len(p)==5:
        p[0] = f'<div>{p[2]}\n{p[3]}</div'
    else:
        p[0] = f'<div>{p[2]}\n{p[3]}\n{p[4]}</div'
    export_txt.append(['Prod. SIMPLE_SEC -->', p.slice])

def p_CONT_SS(p):
    '''CONT_SS : CONT_1
				| CONT_1 CONT_SS
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. CONT_SS -->', p.slice])

def p_ABSTRACT(p):
    '''ABSTRACT : abstract TITLE cAbstract
				| abstract TITLE PARAS cAbstract
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p)==5):
        p[0] = f'{p[2]}{p[3]}'
    export_txt.append(['Prod. ABSTRACT -->', p.slice])

def p_TITLE(p):
    '''TITLE : title CONT_TITLE cTitle
    '''
    p[0] = f'<h3>{p[2]}</h3>'
    export_txt.append(['Prod. TITLE -->', p.slice])
    
def p_TITLEH1(p):
    '''TITLEH1 : title CONT_TITLE cTitle
    '''
    p[0] = f'<h1>{p[2]}</h1>'
    export_txt.append(['Prod. TITLEH1 -->', p.slice])
    
def p_TITLEH2(p):
    '''TITLEH2 : title CONT_TITLE cTitle
    '''
    p[0] = f'<h2>{p[2]}</h2>'
    export_txt.append(['Prod. TITLEH1 -->', p.slice])
    
def p_CONT_TITLE(p):
    '''CONT_TITLE : ELEM_TITLE
				| ELEM_TITLE CONT_TITLE
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_TITLE -->', p.slice])

def p_ELEM_TITLE(p):
    '''ELEM_TITLE : text
				| EMPHASIS
                | LINK
                | EMAIL
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. ELEM_TITLE -->', p.slice])
    
def p_PARAS(p):
    '''PARAS : PARA
				| SIMPARA
                | PARA PARAS
                | SIMPARA PARAS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. PARAS -->', p.slice])

def p_PARA(p):
    '''PARA : para CONT_PARA cPara
    '''
    p[0] = f'<p>{p[2]}</p>'
    export_txt.append(['Prod. PARA -->', p.slice])

def p_CONT_PARA(p):
    '''CONT_PARA : ELEM_PARA
				| ELEM_PARA CONT_PARA
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. CONT_PARA -->', p.slice])

def p_ELEM_PARA(p):
    '''ELEM_PARA : text
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
                | ITEMIZED_LIST
                | IMPORTANT
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. ELEM_PARA -->', p.slice])

def p_ITEMIZED_LIST(p):
    '''ITEMIZED_LIST : itemizedlist LIST_ITEM cItemizedlist
    '''
    p[0] = f'<ul>\n\t{p[2]}\n</ul>'
    export_txt.append(['Prod. ITEMIZED_LIST -->', p.slice])

def p_LIST_ITEM(p):
    '''LIST_ITEM : listItem CONT_ITEM cListItem
                |  LIST_ITEM listItem CONT_ITEM cListItem
    '''
    if len(p)==4:
        p[0] = f'<li>\n\t{p[2]}\n</li>'
    else:
        p[0] = f'{p[1]}\n<li>\v{p[3]}\n</li>'
    export_txt.append(['Prod. LIST_ITEM -->', p.slice])

def p_CONT_ITEM(p):
    '''CONT_ITEM : CONT_1
				| CONT_1 CONT_ITEM
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_ITEM -->', p.slice])

def p_MEDIA_OBJECT(p):
    '''MEDIA_OBJECT : mediaObject INFO CONT_MEDIA_OBJECT cMediaObject
				| mediaObject CONT_MEDIA_OBJECT cMediaObject
    '''
    if len(p)==4:
        p[0] = f'<p>{p[2]}</p>'
    else:
        p[0] = f'<p>{p[2]}{p[3]}</p>'
    export_txt.append(['Prod. MEDIA_OBJECT -->', p.slice])

def p_CONT_MEDIA_OBJECT(p):
    '''CONT_MEDIA_OBJECT : IMAGE_OBJECT
				| VIDEO_OBJECT
                | IMAGE_OBJECT MEDIA_OBJECT
                | VIDEO_OBJECT MEDIA_OBJECT
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. CONT_MEDIA_OBJECT -->', p.slice])

def p_IMAGE_OBJECT(p):
    '''IMAGE_OBJECT : imageObject INFO imageData cImageObject
				| imageObject imageData cImageObject
    '''
    pattern = r'<imagedata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    if len(p)==4:
        atrr_value = re.match(pattern, p[2])
        p[0] = f'<img src="{atrr_value}">'
    else:
        atrr_value = re.match(pattern, p[3])
        p[0] = f'<img src="{atrr_value}">{p[2]}</img>'
    export_txt.append(['Prod. IMAGE_OBJECT -->', p.slice])

def p_VIDEO_OBJECT(p):
    '''VIDEO_OBJECT : videoObject INFO imageData cVideoObject
				| videoObject videoData cVideoObject
    '''
    pattern = r'<videodata\s+fileref=["\']((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*/>'
    if len(p)==4:
        atrr_value = re.match(pattern, p[2]).group(2)
        p[0] = f'<video src="{atrr_value}"></video>'
    else:
        atrr_value = re.match(pattern, p[3]).group(2)
        p[0] = f'<video src="{atrr_value}">{p[2]}</video>'
    export_txt.append(['Prod. VIDEO_OBJECT -->', p.slice])

def p_AUTHOR(p):
    '''AUTHOR : author CONT_AUTHOR cAuthor
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. AUTHOR -->', p.slice])

def p_CONT_AUTHOR(p):
    '''CONT_AUTHOR : FIRSTNAME
				| SURNAME
                | EMAIL
                | FIRSTNAME SURNAME
                | FIRSTNAME EMAIL
                | SURNAME EMAIL
                | FIRSTNAME SURNAME EMAIL
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
    elif(len(p)==4):
        p[0] = f'{p[1]}\n{p[2]}\n{p[3]}'
        
    export_txt.append(['Prod. CONT_AUTHOR -->', p.slice])

def p_ADDRESS(p):
    '''ADDRESS : address cAddress
                | address CONT_ADDRESS cAddress
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    export_txt.append(['Prod. ADDRESS -->', p.slice])

def p_CONT_ADDRESS(p):
    '''CONT_ADDRESS : ELEM_ADDRESS
				| ELEM_ADDRESS CONT_ADDRESS
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}\n{p[2]}'
        
    export_txt.append(['Prod. CONT_ADDRESS -->', p.slice])

def p_ELEM_ADDRESS(p):
    '''ELEM_ADDRESS : STREET
				| CITY
                | STATE
                | PHONE
                | EMAIL
                | text
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. ELEM_ADDRESS -->', p.slice])

def p_COPYRIGHT(p):
    '''COPYRIGHT : copyright YEAR cCopyright
				| copyright YEAR HOLDER cCopyright 
    '''
    if(len(p) == 4):
        p[0] = f'{p[2]}'
    elif(len(p)==5):
        p[0] = f'{p[2]}\n{p[3]}'
    export_txt.append(['Prod. COPYRIGHT -->', p.slice])

def p_SIMPARA(p):
    '''SIMPARA : simpara CONT_SECL cSimpara
    '''
    p[0] = f'<p>{p[2]}</p>'
    export_txt.append(['Prod. SIMPARA -->', p.slice])

def p_EMPHASIS(p):
    '''EMPHASIS : emphasis CONT_SECL cEmphasis
    '''
    p[0] = f'<strong>{p[2]}</strong>'
    export_txt.append(['Prod. EMPHASIS -->', p.slice])

def p_COMMENT(p):
    '''COMMENT : comment CONT_SECL cComment
    '''
    p[0] = f'<i>{p[2]}</i>'
    export_txt.append(['Prod. COMMENT -->', p.slice])

def p_LINK(p):
    '''LINK : link CONT_SECL cLink
    '''
    pattern = r'(<link\s+xlink:href=["\'])((?:(http[s]?|ftp[s]?)://)?(?:[\w.-]+/)*[\w.-]+\.[\w.-]+(?:\S+)?)["\']\s*>'
    attr_value = re.match(pattern, p[1]).group(2)
    p[0] = f'<a href="{attr_value}">{p[2]}</a>'
    export_txt.append(['Prod. LINK -->', p.slice])

def p_CONT_SECL(p):
    '''CONT_SECL : CONT_2
				| CONT_2 CONT_SECL
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_SECL -->', p.slice])
    
def p_CONT_2(p):
    '''CONT_2 : text
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
    '''
    p[0]= f'{p[1]}'
    export_txt.append(['Prod. CONT_2 -->', p.slice])
    
def p_IMPORTANT(p):
    '''IMPORTANT : important TITLE CONT_IMPORTANT cImportant
				| important CONT_IMPORTANT cImportant
    '''
    if(len(p) == 4):
        p[0] = f'<div style="background-color: red; color:white;">{p[2]}</div>'
    elif(len(p)==5):
        p[0] = f'<div style="background-color: red; color:white;">{p[2]}{p[3]}</div>'
    export_txt.append(['Prod. IMPORTANT -->', p.slice])

def p_CONT_IMPORTANT(p):
    '''CONT_IMPORTANT : CONT_1
				| CONT_1 CONT_IMPORTANT
    '''
    if(len(p) == 2):
        p[0] = f'{p[1]}'
    elif(len(p)==3):
        p[0] = f'{p[1]}{p[2]}'
    
    export_txt.append(['Prod. CONT_IMPORTANT -->', p.slice])

def p_CONT_VAR(p):
    '''CONT_VAR : CONT_3
				| CONT_3 CONT_VAR
    '''
    if(len(p)==2):
        p[0] = f'{p[1]}'
    elif(len(p) == 3):
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_VAR -->', p.slice])

def p_CONT_3(p):
    '''CONT_3 : text
				| LINK
                | EMPHASIS
                | COMMENT
    '''
    p[0] = f'{p[1]}'
    export_txt.append(['Prod. CONT_3 -->', p.slice])

def p_FIRSTNAME(p):
    '''FIRSTNAME : firstname CONT_VAR cFirstname
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. FIRSTNAME -->', p.slice])

def p_SURNAME(p):
    '''SURNAME : surname CONT_VAR cSurname
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. SURNAME -->', p.slice])

def p_STREET(p):
    '''STREET : street CONT_VAR cStreet
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. STREET -->', p.slice])

def p_CITY(p):
    '''CITY : city CONT_VAR cCity
    '''
    p[0] = f'{p[2]}'

    export_txt.append(['Prod. CITY -->', p.slice])

def p_STATE(p):
    '''STATE : state CONT_VAR cState
    '''
    p[0] = f'{p[2]}'

    export_txt.append(['Prod. STATE -->', p.slice])

def p_PHONE(p):
    '''PHONE : phone CONT_VAR cPhone
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. PHONE -->', p.slice])

def p_EMAIL(p):
    '''EMAIL : email CONT_VAR cEmail
    '''
    p[0]=f'<a href="{p[2]}'
    export_txt.append(['Prod. EMAIL -->', p.slice])

def p_DATE(p):
    '''DATE : date CONT_VAR cDate
    '''
    p[0] = f'{p[2]}'

    export_txt.append(['Prod. DATE -->', p.slice])
    
def p_YEAR(p):
    '''YEAR : year CONT_VAR cYear
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. YEAR -->', p.slice])

def p_HOLDER(p):
    '''HOLDER : holder CONT_VAR cHolder
    '''
    p[0] = f'{p[2]}'

    export_txt.append(['Prod. HOLDER -->', p.slice])

def p_INFORMAL_TABLE(p):
    '''INFORMAL_TABLE : informalTable TABLE_MEDIA cInformalTable
				| informalTable TABLE_GROUP cInformalTable
    '''
    p[0] = f'<table>{p[2]}</table>'
    export_txt.append(['Prof. INFORMAL_TABLE -->', p.slice])

def p_TABLE_MEDIA(p):
    '''TABLE_MEDIA : MEDIA_OBJECT
				| MEDIA_OBJECT TABLE_MEDIA
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. TABLE_MEDIA -->', p.slice])

def p_TABLE_GROUP(p):
    '''TABLE_GROUP : TGROUP
				| TGROUP TABLE_GROUP
    '''
    if len(p)==2:
        p[0] = f'<div>{p[1]}</div>'
    else:
        p[0] = f'<div>{p[1]}</div>\n{p[2]}'
    export_txt.append(['Prod. TABLE_GROUP -->', p.slice])

def p_TGROUP(p):
    '''TGROUP : tgroup THEAD TBODY TFOOT cTgroup
				| tgroup THEAD TBODY cTgroup
                | tgroup TBODY TFOOT cTgroup
                | tgroup TBODY cTgroup
    '''
    if len(p)==4:   #Si la tabla solo tiene cuerpo
        p[0] = f'{p[2]}'
    elif len(p)==5:
        p[0] = f'{p[2]}\n{p[3]}'
    else:
        p[0] = f'{p[2]}\n{p[3]}\n{p[4]}'
    export_txt.append(['Prod. TGROUP -->', p.slice])

#-------------- Header table
def p_THEAD(p):
    '''THEAD : thead CONT_TH cThead
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. THEAD -->', p.slice])

def p_CONT_TH(p):
    '''CONT_TH : ROWH
				| ROWH CONT_TH
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. CONT_TH -->', p.slice])

def p_ROWH(p):
    '''ROWH : row CONT_ROWH cRow
    '''
    p[0] = f'<tr>{p[2]}</tr>'
    export_txt.append(['Prod. ROWH -->', p.slice])

def p_CONT_ROWH(p):
    '''CONT_ROWH : ENTRYH
				| ENTRYH CONT_ROWH
                | ENTRYTBLH
				| ENTRYTBLH CONT_ROWH
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_ROWH -->', p.slice])

def p_ENTRYH(p):
    '''ENTRYH : entry CONT_ENTRY cEntry
    '''
    p[0] = f'<th>{p[2]}</th>'
    export_txt.append(['Prod. ENTRYH -->', p.slice])

def p_ENTRYTBLH(p):
    '''ENTRYTBLH : entrytbl THEAD TBODY cEntrytbl
				| entrytbl TBODY cEntrytbl
    '''
    if len(p)==4:
        p[0] = f'<th><div>{p[2]}</div></th>'
    else:
        p[0] = f'<th>{p[2]}\n{p[3]}</th>'
    export_txt.append(['Prod. ENTRYTBL -->', p.slice])
#----------- fin header table

def p_CONT_T(p):
    '''CONT_T : ROW
				| ROW CONT_T
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    export_txt.append(['Prod. CONT_T -->', p.slice])

def p_TFOOT(p):
    '''TFOOT : tfoot CONT_T cTfoot
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. TFOOT -->', p.slice])
    
def p_TBODY(p):
    '''TBODY : tbody CONT_T cTbody
    '''
    p[0] = f'{p[2]}'
    export_txt.append(['Prod. TBODY -->', p.slice])

def p_ROW(p):
    '''ROW : row CONT_ROW cRow
    '''
    p[0] = f'<tr>{p[2]}</tr>'
    export_txt.append(['Prod. ROW -->', p.slice])

def p_CONT_ROW(p):
    '''CONT_ROW : ENTRY
				| ENTRY CONT_ROW
                | ENTRYTBL
				| ENTRYTBL CONT_ROW
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_ROW -->', p.slice])

def p_ENTRY(p):
    '''ENTRY : entry CONT_ENTRY cEntry
    '''
    p[0] = f'<td>{p[2]}</td>'
    export_txt.append(['Prod. ENTRY -->', p.slice])

def p_ENTRYTBL(p):
    '''ENTRYTBL : entrytbl THEAD TBODY cEntrytbl
				| entrytbl TBODY cEntrytbl
    '''
    if len(p)==4:
        p[0] = f'<td><div>{p[2]}</div></td>'
    else:
        p[0] = f'<td><div>{p[2]}\n{p[3]}</div></td>'
    export_txt.append(['Prod. ENTRYTBL -->', p.slice])

def p_CONT_ENTRY(p):
    '''CONT_ENTRY : text
				| text CONT_ENTRY
                | ITEMIZED_LIST
                | ITEMIZED_LIST CONT_ENTRY
                | IMPORTANT
                | IMPORTANT CONT_ENTRY
                | PARA
                | PARA CONT_ENTRY
                | SIMPARA
                | SIMPARA CONT_ENTRY
                | COMMENT
                | COMMENT CONT_ENTRY
                | ABSTRACT
                | ABSTRACT CONT_ENTRY
                | MEDIA_OBJECT
                | MEDIA_OBJECT CONT_ENTRY
    '''
    if len(p)==2:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}{p[2]}'
    export_txt.append(['Prod. CONT_ENTRY -->', p.slice])

#----------------------------------------
def p_error(p):
    # p return lexer object
    global error_counter
    if (p):
        print(f'SYNTAX ERROR --> Type: {p.type} | Value: {p.value} | Line: {p.lineno}')
        export_txt.append(['!!! Parser error -->', p])
    error_counter += 1

parser = yacc.yacc()  # ignore warnings
# error log=yacc.NullLogger()

def Analyze_from_file():
	cleanpath = Request_route()
	global error_counter
	# Execute code analyzer
	try:
		file = open(cleanpath, 'r', encoding='utf8')
		strings = file.read()
		file.close()
		lexer.lineno = 1
		result = parser.parse(strings)

		try:
			with open(f'analyzed-productions.txt', 'w', encoding='utf8') as f:
				f.write('ANALYZED PRODUCTIONS BY THE PARSER:\n========================================\n')
				counter = 0
				for line in export_txt:
					counter += 1
					f.write(f'{counter}] {line[0]} | {line[1]}\n')
					f.write(f'----------------------------------------\n')
				f.write(f'========================================\n')
				f.write(f'Total analyzed productions: {counter}\n')
			f.close()
		except:
			print('(!) ERROR creating logs')
		if error_counter > 0:
			print('(XXXXX) A syntax error occurred (XXXXX)')
			# counter reset
			error_counter = 0
			reload(lexer)
		else:
			print('(V) The file is syntactically correct (V)')
			# export to html
			search_str = '\\' if ('\\' in cleanpath) else '/' 	# Check if the file is in a path with backslashes (\) or forward slashes (/)
			raw_file_name = cleanpath.split(search_str)[-1] 	# Get the file name without the path
			file_name = raw_file_name.split('.xml')[0]			# Get the file name without the extension
			arr = [] 											# List to store the content of the HTML file
			arr.append(
				f'''<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset="utf-8">\n\t<title>{file_name}</title>\n</head>\n<body>\n'''
			)
			arr.append(result)
			arr.append('\n</body>\n</html>') # end of html file

			with open(f'exports/{file_name}.html', 'w', encoding='utf8') as f:
				for line in arr:
					f.write(line)
			f.close()
			print('(!) A .txt file was exported with the analyzed productions.')
			
	except IOError:
		print('An error occurred trying to read file: ', cleanpath)

def Analyze_from_console():
	# normal excecution
	print('| End the execution: [Ctrl] + [c] |\n| Back to principal menu: _exit   |')
	while True:
		s = input('>> ')
		if s=='_exit':
			break
		result = parser.parse(s)
		print(result)

#---------------------------------------
if __name__=='__main__':
	Menu_logic(
		'Parser',
		menu_options,
		Analyze_from_file,
		Analyze_from_console
	)
