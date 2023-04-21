def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[1].replace("#","") 
		if token == 'ws':
			return WHITESPACE
		if token == 'number':
			return NUMBER
		if token == '+':
			return PLUS
		if token == '*':
			return TIMES
		if token == '(':
			return LPAREN
		if token == ')':
			return RPAREN
		else: 
			return "Error sintactico"