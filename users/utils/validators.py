class Validations:
    def emptyCheck(self,**kwargs):
        dict_keys=kwargs.keys()
        for item in dict_keys:
            value = str(kwargs[item])
            if len(value) <1:
                raise ValueError("empty string")


    def check_password(self,password):
        if len(password) < 8:
            raise ValueError("password is shorter than 8")

    def checkConfirm_and_pass(self,password,confirmPassword):
        if password != confirmPassword :
            raise ValueError("password and confirm password are not equal")


