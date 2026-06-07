"""
refine_youtube_commands.py
============================

Parser Mejorado - Extrae comandos con precisión desde YouTube

Mejoras:
- Detección de comandos compuestos (Knife -> Bisect)
- Parámetros específicos y valores
- Diferenciación entre UI y shortcuts
- Mapeo a comandos LYZU reales
- Validación de sintaxis

Fecha: 22 Febrero 2026
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass


@dataclass
class ParsedCommand:
    """Comando extraído y parseado."""
    raw_text: str
    command_type: str
    action: str
    parameters: Dict[str, Any]
    lyzu_equivalent: str
    confidence: float
    notes: str = ""


class AdvancedYouTubeCommandParser:
    """Parser avanzado con mejor clasificación de comandos."""
    
    # Mapeo de acciones YouTube -> LYZU
    ACTION_MAP = {
        # Operaciones básicas
        "G": ("move", "move_object", 0.95),
        "Grab": ("move", "move_object", 0.95),
        "Mover": ("move", "move_object", 0.95),
        
        "R": ("rotate", "rotate_object", 0.95),
        "Rotate": ("rotate", "rotate_object", 0.95),
        "Rotar": ("rotate", "rotate_object", 0.95),
        
        "S": ("scale", "scale_object", 0.95),
        "Scale": ("scale", "scale_object", 0.95),
        "Escalar": ("scale", "scale_object", 0.95),
        
        "E": ("extrude", "extrude_mesh", 0.90),
        "Extrude": ("extrude", "extrude_mesh", 0.90),
        "Extruir": ("extrude", "extrude_mesh", 0.90),
        
        # Herramientas específicas
        "Bisect": ("cut", "bisect_object", 0.85),
        "Corte": ("cut", "bisect_object", 0.85),
        "Knife": ("cut", "bisect_object", 0.80),
        
        "Loop Cut": ("cut", "loop_cut", 0.85),
        "Ctrl+R": ("cut", "loop_cut", 0.90),
        
        "Tab": ("mode_change", "edit_mode", 0.95),
        "Modo edición": ("mode_change", "edit_mode", 0.95),
        
        "A": ("select_all", "select_all", 0.90),
        "Select All": ("select_all", "select_all", 0.90),
        
        "Shift+A": ("create", "add_object", 0.95),
        "Add": ("create", "add_object", 0.95),
        
        # UI Navigation
        "Edit->Preferences": ("settings", "edit_preferences", 0.80),
        "Add-ons": ("settings", "addon_manager", 0.85),
        
        # Herramientas avanzadas
        "Merge": ("merge", "merge_vertex", 0.85),
        "Merge by Distance": ("merge", "merge_vertex", 0.85),
        
        "Bevel": ("bevel", "bevel_edges", 0.85),
        "Array": ("array", "array_modifier", 0.80),
        "Shift+R": ("repeat", "repeat_last", 0.85),
        
        "Duplicate": ("duplicate", "duplicate_object", 0.90),
        "Shift+D": ("duplicate", "duplicate_object", 0.95),
        
        "Fill": ("fill", "fill_faces", 0.85),
        "F": ("fill", "fill_faces", 0.85),
        
        "Bridge": ("bridge", "bridge_edges", 0.80),
        "Join": ("join", "join_objects", 0.90),
        "Ctrl+J": ("join", "join_objects", 0.95),
    }
    
    def __init__(self):
        self.parsed_commands: List[ParsedCommand] = []
    
    def parse_transcript(self, text: str) -> List[ParsedCommand]:
        """Parsea una transcripción completa."""
        self.parsed_commands = []
        
        lines = text.split('\n')
        
        for line in lines:
            if not line.strip() or line.startswith('Transcripción:'):
                continue
            
            if line.strip().startswith('['):
                # Línea con timestamp
                cmd = self._parse_timestamped_line(line)
                if cmd:
                    self.parsed_commands.append(cmd)
            elif '->' in line or any(k in line for k in self.ACTION_MAP.keys()):
                # Línea con instrucción
                cmd = self._parse_instruction_line(line)
                if cmd:
                    self.parsed_commands.append(cmd)
        
        return self.parsed_commands
    
    def _parse_timestamped_line(self, line: str) -> ParsedCommand:
        """Parsea línea con timestamp."""
        # Extraer timestamp
        timestamp_match = re.match(r'\[(\d+:\d+)\]\s*(.*)', line)
        if not timestamp_match:
            return None
        
        timestamp = timestamp_match.group(1)
        text = timestamp_match.group(2)
        
        return self._parse_text(text, f"[{timestamp}]")
    
    def _parse_instruction_line(self, line: str) -> ParsedCommand:
        """Parsea línea con instrucciones."""
        return self._parse_text(line.strip(), "instruction")
    
    def _parse_text(self, text: str, source: str) -> ParsedCommand:
        """Parsea texto y extrae comandos."""
        
        # Buscar acciones conocidas
        for action_key, (cmd_type, lyzu_cmd, confidence) in self.ACTION_MAP.items():
            if action_key.lower() in text.lower():
                # Extraer parámetros
                params = self._extract_parameters(text, action_key)
                
                # Mejorar confianza basado en parámetros
                if params:
                    confidence += 0.05
                
                return ParsedCommand(
                    raw_text=text[:100],
                    command_type=cmd_type,
                    action=action_key,
                    parameters=params,
                    lyzu_equivalent=lyzu_cmd,
                    confidence=min(confidence, 1.0),
                    notes=source
                )
        
        return None
    
    def _extract_parameters(self, text: str, action: str) -> Dict[str, Any]:
        """Extrae parámetros del texto."""
        params = {}
        
        # Buscar valores numéricos
        numbers = re.findall(r'(\d+(?:\.\d+)?)', text)
        if numbers:
            params['values'] = numbers
        
        # Buscar ejes (X, Y, Z)
        axes = re.findall(r'\b([XYZ])(?:\s|,|$)', text, re.IGNORECASE)
        if axes:
            params['axes'] = axes
        
        # Buscar grados
        if 'grado' in text.lower() or '°' in text:
            params['is_rotation'] = True
        
        # Buscar opciones específicas
        if 'Clear Inner' in text or 'Clear Outer' in text:
            params['bisect_mode'] = 'clear'
        
        if 'Fill' in text:
            params['fill'] = True
        
        # Detectar si es array/repetición
        if 'array' in text.lower() or 'repetir' in text.lower():
            params['is_array'] = True
        
        # Detectar si requiere copia
        if 'copias' in text.lower() or 'copy' in text.lower():
            params['create_copy'] = True
        
        return params
    
    def validate_commands(self) -> Dict[str, Any]:
        """Valida los comandos parseados."""
        validation = {
            "total": len(self.parsed_commands),
            "by_type": {},
            "by_confidence": {},
            "total_confidence": 0,
            "average_confidence": 0
        }
        
        for cmd in self.parsed_commands:
            # Contar por tipo
            validation["by_type"][cmd.command_type] = \
                validation["by_type"].get(cmd.command_type, 0) + 1
            
            # Agrupar por confianza
            conf_level = f"{int(cmd.confidence * 100)}%"
            validation["by_confidence"][conf_level] = \
                validation["by_confidence"].get(conf_level, 0) + 1
            
            # Sumar confianza
            validation["total_confidence"] += cmd.confidence
        
        if validation["total"] > 0:
            validation["average_confidence"] = \
                validation["total_confidence"] / validation["total"]
        
        return validation
    
    def generate_lyzu_script(self) -> str:
        """Genera script de LYZU ejecutable."""
        script = """# Script LYZU generado desde YouTube
# Autogenerado - 22 Febrero 2026

from lyzu_core import LYZUCore

# Inicializar LYZU
lyzu = LYZUCore(mode='hybrid', enable_learning_freedom=True)

# Historial de comandos
commands_executed = []

"""
        
        for i, cmd in enumerate(self.parsed_commands, 1):
            if cmd.confidence >= 0.80:  # Solo comandos con confianza alta
                script += f"\n# Paso {i}: {cmd.action} ({int(cmd.confidence*100)}% confianza)\n"
                script += f"# Original: {cmd.raw_text}\n"
                
                # Generar comando LYZU
                if cmd.lyzu_equivalent == "move_object":
                    script += f'result = lyzu.process_user_input("Move object with parameters {cmd.parameters}")\n'
                elif cmd.lyzu_equivalent == "rotate_object":
                    script += f'result = lyzu.process_user_input("Rotate object")\n'
                elif cmd.lyzu_equivalent == "scale_object":
                    script += f'result = lyzu.process_user_input("Scale object")\n'
                elif cmd.lyzu_equivalent == "bisect_object":
                    script += f'result = lyzu.process_user_input("Bisect/Cut object with parameters {cmd.parameters}")\n'
                else:
                    script += f'result = lyzu.process_user_input("{cmd.action}")\n'
                
                script += f'commands_executed.append(result)\n'
        
        script += """
# Mostrar resultados
print(f"Comandos ejecutados: {len(commands_executed)}")
for i, result in enumerate(commands_executed, 1):
    print(f"  {i}. Status: {result.get('status', 'UNKNOWN')}")
"""
        
        return script


def main():
    """Función principal."""
    print("=" * 70)
    print(" PARSER MEJORADO - EXTRACCIÓN PRECISA DE COMANDOS YOUTUBE")
    print("=" * 70)
    
    parser = AdvancedYouTubeCommandParser()
    
    transcription_files = [
        "tutorial_fundamentos_42.txt",
        "tutorial_villa_savoye.txt",
        "tutorial_cortes_bisect.txt",
        "tutorial_arquitectura_2d_a_3d.txt",
        "tutorial_arquitectura_36.txt"
    ]
    
    all_results = {
        "parsing_date": "2026-02-22",
        "transcriptions": []
    }
    
    for transcript_file in transcription_files:
        path = Path("ZULY_LAB/entrenamiento_youtube") / transcript_file
        
        if not path.exists():
            print(f"\n❌ {transcript_file} - NO ENCONTRADO")
            continue
        
        print(f"\n{'='*70}")
        print(f"📄 Procesando: {transcript_file}")
        print(f"{'='*70}")
        
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        parser.parse_transcript(text)
        validation = parser.validate_commands()
        
        print(f"\n✅ Comandos extraídos: {validation['total']}")
        print(f"   Por tipo: {validation['by_type']}")
        print(f"   Confianza promedio: {validation['average_confidence']*100:.0f}%")
        print(f"   Distribución: {validation['by_confidence']}")
        
        # Mostrar primeros 5 comandos con alta confianza
        print(f"\n   Top comandos (80%+):")
        high_conf_cmds = [cmd for cmd in parser.parsed_commands 
                         if cmd.confidence >= 0.80][:5]
        for cmd in high_conf_cmds:
            print(f"     ✓ {cmd.action:<15} → {cmd.lyzu_equivalent:<20} ({int(cmd.confidence*100)}%)")
        
        # Generar script LYZU
        lyzu_script = parser.generate_lyzu_script()
        script_path = Path("ZULY_LAB") / f"lyzu_script_{transcript_file.replace('.txt', '.py')}"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(lyzu_script)
        print(f"\n   📝 Script LYZU generado: {script_path.name}")
        
        # Guardar resultados
        result = {
            "filename": transcript_file,
            "total_commands": validation['total'],
            "by_type": validation['by_type'],
            "average_confidence": validation['average_confidence'],
            "high_confidence_count": len(high_conf_cmds)
        }
        all_results["transcriptions"].append(result)
    
    # Guardar resumen
    summary_path = Path("ZULY_LAB") / "refined_parsing_results.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*70}")
    print("✅ REFINEMENT COMPLETADO")
    print(f"{'='*70}")
    print(f"📊 Resumen guardado en: {summary_path}")


if __name__ == "__main__":
    main()
