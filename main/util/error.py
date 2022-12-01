class Error:
    def error(self,error):
        erro = {}
        for key, value in error.items():
            erro["errors"] = value
        return erro

