import os
import json
import time
def main():
	
	main_menu()

def select_lang(menu_selec,lang_selec,text_selec):

	with open(f"{os.getcwd()}/language/{lang_selec}/{text_selec}.json") as main_menu_lang:
		languagetxt = json.load(main_menu_lang)
		i = 0
		output_text = {} 
		for k,v in languagetxt.items():
			if i == menu_selec:
				output_text = v[0]
			i += 1

	return output_text
			

def main_menu():
	text_dict = select_lang(0,"PTBR","main_menu")
	selection = 0
	for k,v in text_dict.items():
		print(k,v)
	try:
		selection = int(input(""))
		if selection == 1:
			print(f"Numero selecionado: {selection}")
		elif selection == 2:
			print(f"Numero selecionado: {selection}")
		elif selection == 3:
			print(f"Numero selecionado: {selection}")
		else:
			print(f"Erro, input invalido tem que ser 1 ou 2 ou 3!! INPUT={selection}")
	except:
		print("INPUT TEM Q SER UM NUMERO")

if __name__ == "__main__":
	main()