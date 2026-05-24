
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

class ProductoException(FoodUException):
    pass


class ProductoNoEncontradoError(ProductoException):
    pass


class ProductoNoDisponibleError(ProductoException):
    pass


class PedidoException(FoodUException):
    pass


class PedidoVacioError( PedidoException):
    pass


class PedidoNoEncontradoError(PedidoException):
    pass


class CalificacionException(FoodUException):
    pass


class CalificacionInvalidaError(CalificacionException):
    pass