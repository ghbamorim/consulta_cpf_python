class Token_params:
  client_id : str
  client_secret : str  
  
class Cpf_params(Token_params):
  user_cpf : str
  cpfs_for_query : str

