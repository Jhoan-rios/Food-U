class FoodUException(Exception):
    pass

class UsuarioException(FoodUException):
    pass


class UsuarioDuplicadoError(UsuarioException):
    pass


class CorreoRegistradoError(UsuarioException):
    pass


class UsuarioNoEncontradoError(UsuarioException):
    pass

class VendedorException(FoodUException):
    pass


class VendedorDuplicadoError(VendedorException):
    pass


class VendedorNoEncontradoError(VendedorException):
    pass

