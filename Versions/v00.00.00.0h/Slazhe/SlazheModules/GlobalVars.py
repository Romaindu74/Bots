class GlobalVars:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GlobalVars, cls).__new__(cls)
            cls._instance._init_vars()
        return cls._instance

    def _init_vars(self):
        self.variables = {}

    def set_variable(self, name, value):
        self.variables[name] = value

    def get_variable(self, name, default=None):
        return self.variables.get(name, default)

    def save_variables(self):
        return self.variables.copy()
    
    def restore_variables(self, saved_variables):
        self.variables = saved_variables
# Version Globale: v00.00.00.0h
# Version du fichier: v00.00.00.01
