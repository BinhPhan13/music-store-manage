class Admin:
    def __init__(self, id, name, pw):
        self.__id = id
        self.__name = name
        self.__pw = pw

    def __str__(self) -> str:
        return f"{self.name:10}{self.pw:10}"

    @property
    def id(self):
        return self.__id
    
    @property
    def name(self):
        return self.__name
    
    @property
    def pw(self):
        return self.__pw
    
class AdminManager:
    def __init__(self, admin):
        self.__admin = admin

    def login(self):
        admin_id = input('- Enter ID: ')
        admin_pw = input('- Enter password: ')
        if admin_id == self.__admin.id and admin_pw == self.__admin.pw:
            print('Login successfully')
        else:
            print('Password or ID is wrong')

    def logout(self):
        pass
    
if __name__ == '__main__':
    admin = Admin('0', 'Binh', 'python')
    amng = AdminManager(admin)
    amng.login()