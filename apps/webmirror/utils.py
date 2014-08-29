

from access_tokens import scope, tokens
def make_global_token( ):
	return tokens.generate( scope.access_all() )