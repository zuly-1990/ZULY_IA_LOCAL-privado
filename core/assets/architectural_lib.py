
"""
ZULY Architectural Component Library
Provides procedural generator functions for complex architectural elements.
"""
from typing import Dict, Any, List

class ArchitecturalLibrary:
    def __init__(self, adapter):
        self.adapter = adapter

    def create_framed_window(self, name: str, location: List[float], size: List[float], 
                             frame_thickness: float = 0.1, frame_depth: float = 0.1):
        """
        Crea una ventana completa con marco esculpido y cristal.
        """
        # 1. Crear el marco (Cubo esculpido con Inset)
        self.adapter.create_primitive('cube', name=f"{name}_Frame", location=location)
        self.adapter.set_dimensions(f"{name}_Frame", size)
        
        # Esculpimos el hueco del cristal
        self.adapter.inset_faces(f"{name}_Frame", thickness=frame_thickness, 
                                 depth=frame_depth, face_select='FRONT')
        
        # Aplicamos material de marco
        self.adapter.create_material(f"Mat_Frame_{name}", color=(0.1, 0.1, 0.1), roughness=0.4)
        self.adapter.apply_material(f"{name}_Frame", f"Mat_Frame_{name}")

        # 2. Crear el cristal (Cubo fino)
        self.adapter.create_primitive('cube', name=f"{name}_Glass", location=location)
        glass_size = [size[0] - frame_thickness*2, 0.02, size[2] - frame_thickness*2]
        self.adapter.set_dimensions(f"{name}_Glass", glass_size)
        
        self.adapter.create_material("Mat_Glass", color=(0.5, 0.7, 1.0), alpha=0.3, transmission=1.0)
        self.adapter.apply_material(f"{name}_Glass", "Mat_Glass")

        return f"{name}_Frame"

    def create_spiral_staircase(self, name: str, location: List[float], steps: int = 15, 
                                step_height: float = 0.2, step_rotation: float = 0.4):
        """
        Crea una escalera de caracol de forma procedural.
        """
        import math
        center_x, center_y, center_z = location
        
        for i in range(steps):
            step_name = f"{name}_Step_{i}"
            angle = i * step_rotation
            z_pos = center_z + (i * step_height)
            
            # Posicionamos el escalón en radio
            x_pos = center_x + math.cos(angle) * 1.0
            y_pos = center_y + math.sin(angle) * 1.0
            
            self.adapter.create_primitive('cube', name=step_name, location=[x_pos, y_pos, z_pos])
            self.adapter.set_dimensions(step_name, [1.2, 0.4, 0.1])
            self.adapter.set_rotation(step_name, [0, 0, angle])
                
        return name
                
        return name
