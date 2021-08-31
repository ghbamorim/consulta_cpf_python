# api de consulta de cpf

  Api para consulta de situação cadastral de cpf

## Instalação das dependências

  executar no diretório principal

  ```bash
  pip install -r requirements.txt
  ```

## Inicialização

  executar no diretório principal

  ```bash
  python src/app.py
  ```
### Endpoints

  #### /login
    methodo GET
    parâmetros: 
      autenticação básica (USERNAME e PASSWORD)
      utilizar algum usuário e senha do banco de dados fake. Ex.: USERNAME: user01, PASSWORD: 123456
    retorno: token JWT para ser usado nas consultas com duração de 30 minutos

  #### /cpfstatus
    methodo GET
    parâmetros:
      Header -> x-access-token = token obtido no login

      json body -> Json no formato:
        {"client_id" : "8ddc46f2-f6a3-4077-9e04-74b55de934a5",
         "client_secret" : "06d4aaac-1412-45f6-bd7c-38b2bef0d706",
         "user_cpf": cpf do usuário da api,
         "cpf": cpf a ser consultado}
    retorno:
      json no formato:
        {
          "status": "Regular"
        }