#deveria estar na pasta models


class Token_params:
    client_id: str
    client_secret: str


class Cpf_params(Token_params):
    user_cpf: str
    cpf_for_query: str
