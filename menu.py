# imports
import os

# user menu options
menu_options = {
	1: '| Analyze code from a local file |',
	2: '| Analyze code from the console  |',
	3: '| EXIT                           |'
}

# console cleaner
def cls():
	os.system('cls' if os.name=='nt' else 'clear')

# menu options display
def Print_menu(menu_options):
	for key in menu_options.keys():
		print(key, '--', menu_options[key])

def Menu_logic(
	program_name: str,
	menu_options: 'dict[int, str]',
	option_one: 'function',
	option_two: 'function'
):
	cls()
	print(f'{program_name} Dockbook Article | BREGANT, Joaquin | 2023')
	while True:
		Print_menu(menu_options)
		option = ''
		try:
			option = int(input('Enter an option: '))
		except:
			cls()
			print('Invalid option! Please enter one of the available options')
		cls()
		if option==1:
			option_one()
		elif option==2:
			option_two()
		elif option==3:
			print('Execution finished!')
			exit()
		else:
			print()
	







