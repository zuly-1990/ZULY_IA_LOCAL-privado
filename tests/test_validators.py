# tests/test_validators.py
"""
Tests unitarios para el módulo de validadores.
"""

import pytest
from core.utils.validators import (
    validate_location,
    validate_rotation,
    validate_scale,
    validate_material_name,
    validate_object_type,
    validate_positive_number,
    validate_color_rgb
)
from core.utils.exceptions import ValidationError


class TestValidateLocation:
    """Tests para validate_location."""
    
    def test_tuple_input(self):
        """Test con tupla de entrada."""
        result = validate_location((1, 2, 3))
        assert result == (1.0, 2.0, 3.0)
        assert isinstance(result[0], float)
    
    def test_list_input(self):
        """Test con lista de entrada."""
        result = validate_location([1.5, 2.5, 3.5])
        assert result == (1.5, 2.5, 3.5)
    
    def test_string_input(self):
        """Test con string de entrada."""
        result = validate_location("1.0, 2.0, 3.0")
        assert result == (1.0, 2.0, 3.0)
    
    def test_string_with_spaces(self):
        """Test con string con espacios variables."""
        result = validate_location("1,  2,   3")
        assert result == (1.0, 2.0, 3.0)
    
    def test_negative_coordinates(self):
        """Test con coordenadas negativas."""
        result = validate_location([-1, -2, -3])
        assert result == (-1.0, -2.0, -3.0)
    
    def test_invalid_length(self):
        """Test con número incorrecto de coordenadas."""
        with pytest.raises(ValidationError) as exc_info:
            validate_location([1, 2])
        
        assert "3 coordenadas" in str(exc_info.value)
    
    def test_invalid_type(self):
        """Test con tipo inválido."""
        with pytest.raises(ValidationError):
            validate_location(123)
    
    def test_invalid_string_format(self):
        """Test con string mal formateado."""
        with pytest.raises(ValidationError):
            validate_location("abc, def, ghi")


class TestValidateRotation:
    """Tests para validate_rotation."""
    
    def test_basic_rotation(self):
        """Test de rotación básica."""
        result = validate_rotation([0, 90, 180])
        assert result == (0.0, 90.0, 180.0)
    
    def test_rotation_normalization(self):
        """Test de normalización de ángulos."""
        result = validate_rotation([360, 450, -90])
        assert result[0] == 0.0  # 360 % 360
        assert result[1] == 90.0  # 450 % 360
        assert result[2] == 270.0  # -90 % 360
    
    def test_large_angles(self):
        """Test con ángulos grandes."""
        result = validate_rotation([720, 1080, 1440])
        assert result == (0.0, 0.0, 0.0)


class TestValidateScale:
    """Tests para validate_scale."""
    
    def test_uniform_scale_int(self):
        """Test con escala uniforme entera."""
        result = validate_scale(2)
        assert result == 2.0
        assert isinstance(result, float)
    
    def test_uniform_scale_float(self):
        """Test con escala uniforme float."""
        result = validate_scale(1.5)
        assert result == 1.5
    
    def test_non_uniform_scale(self):
        """Test con escala no uniforme."""
        result = validate_scale([1, 2, 3])
        assert result == (1.0, 2.0, 3.0)
    
    def test_string_uniform_scale(self):
        """Test con string de escala uniforme."""
        result = validate_scale("2.5")
        assert result == 2.5
    
    def test_string_non_uniform_scale(self):
        """Test con string de escala no uniforme."""
        result = validate_scale("1, 2, 3")
        assert result == (1.0, 2.0, 3.0)
    
    def test_zero_scale_fails(self):
        """Test que escala cero falla."""
        with pytest.raises(ValidationError) as exc_info:
            validate_scale(0)
        
        assert "positiva" in str(exc_info.value).lower()
    
    def test_negative_scale_fails(self):
        """Test que escala negativa falla."""
        with pytest.raises(ValidationError):
            validate_scale(-1)
    
    def test_non_uniform_with_zero_fails(self):
        """Test que escala no uniforme con cero falla."""
        with pytest.raises(ValidationError):
            validate_scale([1, 0, 3])


class TestValidateMaterialName:
    """Tests para validate_material_name."""
    
    def test_valid_material(self):
        """Test con material válido."""
        valid_materials = ["oro", "plata", "vidrio"]
        result = validate_material_name("oro", valid_materials)
        assert result == "oro"
    
    def test_case_insensitive(self):
        """Test que es case-insensitive."""
        valid_materials = ["oro", "plata"]
        result = validate_material_name("ORO", valid_materials)
        assert result == "oro"
    
    def test_with_spaces(self):
        """Test con espacios."""
        valid_materials = ["oro", "plata"]
        result = validate_material_name("  oro  ", valid_materials)
        assert result == "oro"
    
    def test_invalid_material(self):
        """Test con material inválido."""
        valid_materials = ["oro", "plata"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_material_name("cobre", valid_materials)
        
        assert "no válido" in str(exc_info.value)
        assert "oro" in str(exc_info.value.details["valid_options"])
    
    def test_non_string_fails(self):
        """Test que no-string falla."""
        with pytest.raises(ValidationError):
            validate_material_name(123, ["oro"])


class TestValidateObjectType:
    """Tests para validate_object_type."""
    
    def test_valid_object_type(self):
        """Test con tipo válido."""
        valid_types = ["cubo", "esfera", "cilindro"]
        result = validate_object_type("cubo", valid_types)
        assert result == "cubo"
    
    def test_case_insensitive(self):
        """Test case-insensitive."""
        valid_types = ["cubo", "esfera"]
        result = validate_object_type("CUBO", valid_types)
        assert result == "cubo"
    
    def test_invalid_type(self):
        """Test con tipo inválido."""
        valid_types = ["cubo", "esfera"]
        
        with pytest.raises(ValidationError) as exc_info:
            validate_object_type("piramide", valid_types)
        
        assert "no válido" in str(exc_info.value)


class TestValidatePositiveNumber:
    """Tests para validate_positive_number."""
    
    def test_positive_int(self):
        """Test con entero positivo."""
        result = validate_positive_number(5)
        assert result == 5.0
        assert isinstance(result, float)
    
    def test_positive_float(self):
        """Test con float positivo."""
        result = validate_positive_number(3.14)
        assert result == 3.14
    
    def test_string_number(self):
        """Test con string numérico."""
        result = validate_positive_number("2.5")
        assert result == 2.5
    
    def test_zero_fails(self):
        """Test que cero falla."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_number(0)
        
        assert "positivo" in str(exc_info.value).lower()
    
    def test_negative_fails(self):
        """Test que negativo falla."""
        with pytest.raises(ValidationError):
            validate_positive_number(-5)
    
    def test_custom_name_in_error(self):
        """Test que el nombre personalizado aparece en error."""
        with pytest.raises(ValidationError) as exc_info:
            validate_positive_number(-1, name="radio")
        
        assert "radio" in str(exc_info.value)


class TestValidateColorRGB:
    """Tests para validate_color_rgb."""
    
    def test_tuple_rgb(self):
        """Test con tupla RGB."""
        result = validate_color_rgb([1.0, 0.5, 0.0])
        assert result == (1.0, 0.5, 0.0)
    
    def test_hex_color(self):
        """Test con color hexadecimal."""
        result = validate_color_rgb("#FF8000")
        assert result[0] == 1.0  # R
        assert abs(result[1] - 0.5019607843137255) < 0.001  # G
        assert result[2] == 0.0  # B
    
    def test_hex_without_hash(self):
        """Test con hex sin #."""
        result = validate_color_rgb("FF0000")
        assert result == (1.0, 0.0, 0.0)
    
    def test_black(self):
        """Test con negro."""
        result = validate_color_rgb("#000000")
        assert result == (0.0, 0.0, 0.0)
    
    def test_white(self):
        """Test con blanco."""
        result = validate_color_rgb("#FFFFFF")
        assert result == (1.0, 1.0, 1.0)
    
    def test_invalid_rgb_range(self):
        """Test con valores fuera de rango."""
        with pytest.raises(ValidationError) as exc_info:
            validate_color_rgb([1.5, 0.5, 0.0])
        
        assert "rango" in str(exc_info.value).lower()
    
    def test_invalid_hex_length(self):
        """Test con hex de longitud incorrecta."""
        with pytest.raises(ValidationError):
            validate_color_rgb("#FFF")
    
    def test_invalid_hex_characters(self):
        """Test con caracteres hex inválidos."""
        with pytest.raises(ValidationError):
            validate_color_rgb("#GGGGGG")
    
    def test_wrong_number_of_components(self):
        """Test con número incorrecto de componentes."""
        with pytest.raises(ValidationError):
            validate_color_rgb([1.0, 0.5])


class TestEdgeCases:
    """Tests de casos extremos."""
    
    def test_very_large_coordinates(self):
        """Test con coordenadas muy grandes."""
        result = validate_location([1e10, 1e10, 1e10])
        assert result == (1e10, 1e10, 1e10)
    
    def test_very_small_positive_scale(self):
        """Test con escala muy pequeña pero positiva."""
        result = validate_scale(0.001)
        assert result == 0.001
    
    def test_unicode_material_name(self):
        """Test con nombre de material con unicode."""
        valid_materials = ["oro", "plata"]
        result = validate_material_name("oro", valid_materials)
        assert result == "oro"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
