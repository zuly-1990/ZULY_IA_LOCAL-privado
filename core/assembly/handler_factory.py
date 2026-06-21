import ast
from typing import Optional
from core.utils.logging import log_info, log_error, log_warning

class HandlerFactory:
    """
    Genera dinámicamente handlers en Python cuando no existe una implementación para una intención nueva.
    Utiliza validación estricta de AST para asegurar que el código es seguro.
    """
    def __init__(self):
        self.allowed_nodes = (
            ast.Module, ast.ClassDef, ast.FunctionDef, ast.arguments, ast.arg,
            ast.Assign, ast.Name, ast.Store, ast.Load, ast.Call, ast.Attribute,
            ast.Return, ast.Expr, ast.Constant, ast.Dict, ast.List, ast.Tuple,
            ast.If, ast.Compare, ast.Eq, ast.NotEq, ast.Pass, ast.alias, ast.ImportFrom
        )

    def generate_handler(self, intent_name: str, spec: str, generated_code: str) -> bool:
        log_info(f"Intentando generar handler dinámico: {intent_name}")
        
        # Validar la seguridad del código generado
        if not self._is_safe_code(generated_code):
            log_error("Código generado rechazado por validación de seguridad (AST).")
            return False
            
        # En producción, esto se guardaría en core/assembly/handlers_generados/
        log_info(f"Código validado exitosamente. Se podría guardar como handler_{intent_name}.py")
        return True

    def _is_safe_code(self, code: str) -> bool:
        """Valida que el código no contenga nodos AST maliciosos o prohibidos"""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if not isinstance(node, self.allowed_nodes):
                    log_warning(f"Nodo no permitido detectado: {type(node).__name__}")
                    return False
            return True
        except SyntaxError as e:
            log_error(f"Error de sintaxis en el código generado: {e}")
            return False
