# tests/test_exceptions.py
"""
Tests unitarios para el módulo de excepciones personalizadas.
"""

import pytest
from core.utils.exceptions import (
    ZulyException,
    CommandExecutionError,
    CommandNotFoundError,
    CommandLoadError,
    NLUError,
    ValidationError,
    SceneMonitorError,
    FileOperationError,
    ConfigurationError,
    LearningEngineError,
    IntentClassificationError,
    EntityExtractionError
)


class TestZulyException:
    """Tests para la excepción base ZulyException."""
    
    def test_basic_exception(self):
        """Test de excepción básica sin detalles."""
        exc = ZulyException("Error de prueba")
        assert str(exc) == "Error de prueba"
        assert exc.message == "Error de prueba"
        assert exc.details == {}
    
    def test_exception_with_details(self):
        """Test de excepción con detalles."""
        details = {"key": "value", "number": 42}
        exc = ZulyException("Error con detalles", details=details)
        
        assert exc.message == "Error con detalles"
        assert exc.details == details
        assert "key=value" in str(exc)
        assert "number=42" in str(exc)
    
    def test_exception_can_be_raised(self):
        """Test que la excepción puede ser lanzada y capturada."""
        with pytest.raises(ZulyException) as exc_info:
            raise ZulyException("Test error")
        
        assert "Test error" in str(exc_info.value)


class TestCommandExceptions:
    """Tests para excepciones relacionadas con comandos."""
    
    def test_command_execution_error(self):
        """Test de CommandExecutionError."""
        exc = CommandExecutionError(
            "Fallo al ejecutar comando",
            details={"command": "crearcubo", "reason": "Blender no disponible"}
        )
        
        assert isinstance(exc, ZulyException)
        assert exc.details["command"] == "crearcubo"
        assert exc.details["reason"] == "Blender no disponible"
    
    def test_command_not_found_error(self):
        """Test de CommandNotFoundError."""
        exc = CommandNotFoundError(
            "Comando no encontrado",
            details={"requested_command": "comandoinexistente"}
        )
        
        assert isinstance(exc, ZulyException)
        assert exc.details["requested_command"] == "comandoinexistente"
    
    def test_command_load_error(self):
        """Test de CommandLoadError."""
        exc = CommandLoadError(
            "Error cargando módulo",
            details={"module": "test_module", "error": "ImportError"}
        )
        
        assert isinstance(exc, ZulyException)
        assert exc.details["module"] == "test_module"


class TestNLUExceptions:
    """Tests para excepciones de NLU."""
    
    def test_nlu_error(self):
        """Test de NLUError."""
        exc = NLUError(
            "Error procesando entrada",
            details={"user_input": "", "reason": "Entrada vacía"}
        )
        
        assert isinstance(exc, ZulyException)
        assert exc.details["reason"] == "Entrada vacía"
    
    def test_intent_classification_error(self):
        """Test de IntentClassificationError."""
        exc = IntentClassificationError(
            "No se pudo clasificar intención",
            details={"confidence": 0.2}
        )
        
        assert isinstance(exc, NLUError)
        assert isinstance(exc, ZulyException)
        assert exc.details["confidence"] == 0.2
    
    def test_entity_extraction_error(self):
        """Test de EntityExtractionError."""
        exc = EntityExtractionError(
            "No se pudieron extraer entidades",
            details={"text": "mueve a xyz"}
        )
        
        assert isinstance(exc, NLUError)
        assert isinstance(exc, ZulyException)


class TestValidationError:
    """Tests para ValidationError."""
    
    def test_validation_error_with_expected_value(self):
        """Test de ValidationError con valor esperado."""
        exc = ValidationError(
            "Parámetro inválido",
            details={
                "parameter": "location",
                "value": "abc",
                "expected": "tuple[float, float, float]"
            }
        )
        
        assert isinstance(exc, ZulyException)
        assert exc.details["parameter"] == "location"
        assert exc.details["expected"] == "tuple[float, float, float]"


class TestOtherExceptions:
    """Tests para otras excepciones."""
    
    def test_scene_monitor_error(self):
        """Test de SceneMonitorError."""
        exc = SceneMonitorError("Error capturando escena")
        assert isinstance(exc, ZulyException)
    
    def test_file_operation_error(self):
        """Test de FileOperationError."""
        exc = FileOperationError(
            "Error escribiendo archivo",
            details={"filepath": "/path/to/file.json"}
        )
        assert isinstance(exc, ZulyException)
        assert exc.details["filepath"] == "/path/to/file.json"
    
    def test_configuration_error(self):
        """Test de ConfigurationError."""
        exc = ConfigurationError("Configuración inválida")
        assert isinstance(exc, ZulyException)
    
    def test_learning_engine_error(self):
        """Test de LearningEngineError."""
        exc = LearningEngineError("Error en motor de aprendizaje")
        assert isinstance(exc, ZulyException)


class TestExceptionHierarchy:
    """Tests para verificar la jerarquía de excepciones."""
    
    def test_all_inherit_from_zuly_exception(self):
        """Verifica que todas las excepciones heredan de ZulyException."""
        exceptions = [
            CommandExecutionError,
            CommandNotFoundError,
            CommandLoadError,
            NLUError,
            ValidationError,
            SceneMonitorError,
            FileOperationError,
            ConfigurationError,
            LearningEngineError,
            IntentClassificationError,
            EntityExtractionError
        ]
        
        for exc_class in exceptions:
            assert issubclass(exc_class, ZulyException)
    
    def test_nlu_subclasses(self):
        """Verifica que las subclases de NLU heredan correctamente."""
        assert issubclass(IntentClassificationError, NLUError)
        assert issubclass(EntityExtractionError, NLUError)
    
    def test_can_catch_by_base_class(self):
        """Verifica que se pueden capturar por clase base."""
        with pytest.raises(ZulyException):
            raise CommandExecutionError("Test")
        
        with pytest.raises(NLUError):
            raise IntentClassificationError("Test")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
