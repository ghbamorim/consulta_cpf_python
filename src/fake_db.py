from users import Users

class Db():
  db = []
  
  def init_fake_db(self):  
    new_user = Users()
    new_user.id = 1
    new_user.cpf = '72002557853'
    new_user.name = 'user01'
    new_user.password = '123456'

    self.db.append(new_user)

    new_user = Users()
    new_user.id = 2
    new_user.cpf = '26616776824'
    new_user.name = 'user02'
    new_user.password = '123456'

    self.db.append(new_user)

    new_user = Users()
    new_user.id = 3
    new_user.cpf = '82272182100'
    new_user.name = 'user03'
    new_user.password = '123456'

    self.db.append(new_user)

  def find_user(self, user_id, password):
    return next((user for user in self.db if user.id == user_id and user.password == password), None)