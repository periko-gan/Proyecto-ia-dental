class BackendError(Exception):
    """Error base del backend."""


class ValidationError(BackendError):
    """Error de validacion de entrada."""


class InferenceError(BackendError):
    """Error durante la inferencia del modelo."""


class ModelLoadError(BackendError):
    """Error al cargar el modelo de IA."""


class AuthenticationError(BackendError):
    """Error de autenticacion."""


class AuthorizationError(BackendError):
    """Error de autorizacion por permisos o pertenencia."""


class UserAlreadyExistsError(BackendError):
    """Error al registrar un usuario ya existente."""
