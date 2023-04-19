def tokens(listaTokens):
	for tokenValue in listaTokens: 
		token = tokenValue[0] 
		if token == 'ws':
			return WHITESPACE
		if token == 'id':
			return ID
		if token == 'number':
			return NUMBER
		if token == '+':
			return PLUS
		if token == '-':
			return MINUS
		if token == '*':
			return TIMES
		if token == '/':
			return DIV
		if token == '(':
			return LPAREN
		if token == ')':
			return RPAREN
		else: 
			return "Error sintactico"