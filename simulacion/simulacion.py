def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[1].replace("#","") 
		if token == 'ws':
			print("white")
		elif token == 'number':
			print("number")
		elif token == '+':
			print("PLUS")
		elif token == '*':
			print("TIMES")
		elif token == '(':
			print("LPAREN")
		elif token == ')':
			print("RPAREN")
		else: 
			print("Error sintactico")