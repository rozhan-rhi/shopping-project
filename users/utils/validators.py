class Validations:
    def emptyCheck(self,kwargs):
        dict_keys=kwargs.keys()
        for item in dict_keys:
            value = str(kwargs[item]).strip()
            if len(value) <1:
                return True


    def check_password(self,password):
        if len(password) < 8:
            return True


    def checkConfirm_and_pass(self,password,confirmPassword):
        if password != confirmPassword :
            return True


