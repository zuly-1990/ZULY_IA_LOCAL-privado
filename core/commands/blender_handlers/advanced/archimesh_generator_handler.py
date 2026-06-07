# core/commands/blender_handlers/advanced/archimesh_generator_handler.py
"""
Handler Zuly para generar modelos arquitectónicos usando Archimesh.
Integrado con el sistema de handlers de Zuly - usa BlenderAdapter.
"""
import bpy
import math
from typing import Dict, Any, List
from core.utils.blender_adapter import BlenderAdapter
from core.utils.logging import log_info, log_success, log_error


class ArchimeshGeneratorHandler:
    """
    Handler para generar modelos arquitectónicos completos con Archimesh.
    Se integra con el sistema Zuly y usa el adapter existente.
    """
    
    HANDLER_ID = "archimesh_generator"
    CATEGORY = "advanced"
    
    def __init__(self):
        self.adapter = BlenderAdapter()
        self.output_dir = None
    
    def ensure_archimesh(self) -> bool:
        """Asegura que Archimesh esté activado."""
        import addon_utils
        enabled, loaded = addon_utils.check("archimesh")
        if not enabled:
            try:
                addon_utils.enable("archimesh")
                log_info("[ARCHIMESH_GEN] Add-on activado")
            except Exception as e:
                log_error(f"[ARCHIMESH_GEN] Error activando archimesh: {e}")
                return False
        return True
    
    def crear_material(self, nombre: str, color: tuple, tipo: str = "DIFFUSE") -> Any:
        """Crea material PBR simple."""
        mat = bpy.data.materials.new(name=nombre)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        bsdf = nodes.new('ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        bsdf.inputs['Base Color'].default_value = (*color, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.5
        
        mat.node_tree.links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        return mat
    
    def asignar_material(self, obj, material):
        """Asigna material a objeto."""
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
    
    def crear_camara_y_luces(self):
        """Setup básico de cámara e iluminación para JUES V2."""
        # Cámara
        cam_data = bpy.data.cameras.new("Camera_JUES")
        cam_obj = bpy.data.objects.new("Camera", cam_data)
        bpy.context.scene.collection.objects.link(cam_obj)
        bpy.context.scene.camera = cam_obj
        cam_obj.location = (8, -8, 5)
        cam_obj.rotation_euler = (1.1, 0, 0.785)
        
        # Luz principal (Sun) - cumple has_light=True
        sun_data = bpy.data.lights.new("Sun_JUES", type="SUN")
        sun_obj = bpy.data.objects.new("Sun", sun_data)
        bpy.context.scene.collection.objects.link(sun_obj)
        sun_obj.location = (5, 5, 10)
        sun_obj.rotation_euler = (0.785, 0, 0.785)
        sun_data.energy = 5.0
        
        # Luz de relleno (Area)
        area_data = bpy.data.lights.new("Fill_JUES", type="AREA")
        area_obj = bpy.data.objects.new("Fill", area_data)
        bpy.context.scene.collection.objects.link(area_obj)
        area_obj.location = (-5, 3, 4)
        area_obj.rotation_euler = (0, 0, -0.5)
        area_data.energy = 2.0
        area_data.size = 5
        
        log_info("[ARCHIMESH_GEN] Cámara y luces creadas (V2 compliant)")
    
    # ============ GENERADORES DE MODELOS ============
    
    def generar_pabellon_cristal_zen(self) -> Dict[str, Any]:
        """
        MOD-001: Pabellón de Cristal Zen
        Estructura etérea con vidrios y jardín interior.
        """
        self.adapter.clear_scene()
        self.crear_camara_y_luces()
        
        # Materiales
        mat_concreto = self.crear_material("Concreto", (0.7, 0.7, 0.7))
        mat_vidrio = self.crear_material("Vidrio_Cristal", (0.85, 0.92, 0.95))
        mat_madera = self.crear_material("Madera_Zen", (0.55, 0.4, 0.25))
        mat_vegetacion = self.crear_material("Jardin", (0.2, 0.6, 0.3))
        
        # Plataforma base con jardín central
        self.adapter.create_primitive("cube", location=(0, 0, 0.1), scale=(5, 4, 0.1))
        base = bpy.context.active_object
        base.name = "Base_Pabellon"
        self.asignar_material(base, mat_concreto)
        
        # Jardín interior (hueco con vegetación)
        self.adapter.create_primitive("cube", location=(0, 0, 0.2), scale=(1.5, 1.5, 0.05))
        jardin = bpy.context.active_object
        jardin.name = "Jardin_Interior"
        self.asignar_material(jardin, mat_vegetacion)
        
        # 8 Columnas de cristal alrededor
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = math.cos(rad) * 4
            y = math.sin(rad) * 4
            
            try:
                bpy.ops.archimesh.create_column(column_height=3, column_radius=0.1)
                col = bpy.context.active_object
            except:
                self.adapter.create_primitive("cylinder", location=(x, y, 1.5), 
                                            scale=(0.1, 0.1, 1.5))
                col = bpy.context.active_object
            col.location = (x, y, 1.5)
            col.name = f"Columna_Cristal_{angle}"
            self.asignar_material(col, mat_vidrio)
        
        # Techo de cristal
        self.adapter.create_primitive("cube", location=(0, 0, 3.1), scale=(4.8, 3.8, 0.05))
        techo = bpy.context.active_object
        techo.name = "Techo_Cristal"
        self.asignar_material(techo, mat_vidrio)
        
        # Ventanas panorámicas
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            x = math.cos(rad) * 4.8
            y = math.sin(rad) * 3.8
            
            try:
                bpy.ops.archimesh.create_window(width=2.0, height=1.8, depth=0.05)
                vent = bpy.context.active_object
            except:
                self.adapter.create_primitive("cube", location=(x, y, 1.5),
                                          scale=(1.0, 0.02, 0.9))
                vent = bpy.context.active_object
            vent.location = (x, y, 1.5)
            vent.rotation_euler[2] = rad
            vent.name = f"Ventana_{angle}"
            self.asignar_material(vent, mat_vidrio)
        
        # Puerta de entrada zen
        try:
            bpy.ops.archimesh.create_door(width=1.2, height=2.2, depth=0.05)
            puerta = bpy.context.active_object
            puerta.location = (0, 4, 1.1)
        except:
            self.adapter.create_primitive("cube", location=(0, 4, 1.1),
                                      scale=(0.6, 0.02, 1.1))
            puerta = bpy.context.active_object
        puerta.name = "Puerta_Zen"
        self.asignar_material(puerta, mat_madera)
        
        return {
            "status": "success",
            "model_id": "MOD-001_Pabellon_Cristal_Zen",
            "elements": ["base", "jardin_interior", "8_columnas_cristal", 
                        "techo_cristal", "4_ventanas", "puerta"],
            "materials": ["concreto", "vidrio", "madera", "vegetacion"]
        }
    
    def generar_torre_helix(self) -> Dict[str, Any]:
        """
        MOD-002: Torre Helix Corporativa
        Espiral ascendente con atrio central luminoso.
        """
        self.adapter.clear_scene()
        self.crear_camara_y_luces()
        
        mat_acero = self.crear_material("Acero", (0.75, 0.78, 0.82))
        mat_vidrio = self.crear_material("Vidrio_Helix", (0.75, 0.88, 0.95))
        mat_neon = self.crear_material("Neon_Atrio", (0.9, 0.95, 1.0))
        
        # 5 pisos en espiral
        for floor in range(5):
            angle = floor * 30  # Rotación escalonada
            z = floor * 3.0
            rad = math.radians(angle)
            
            # Offset en X/Y para efecto helix
            x = math.cos(rad) * 0.5
            y = math.sin(rad) * 0.5
            
            # Piso del nivel
            self.adapter.create_primitive("cube", location=(x, y, z),
                                      scale=(3.5, 3.5, 0.1))
            piso = bpy.context.active_object
            piso.name = f"Piso_Helix_{floor+1}"
            piso.rotation_euler[2] = rad
            self.asignar_material(piso, mat_acero)
            
            # Ventanas curvas en cada nivel
            for w_angle in [0, 90, 180, 270]:
                w_rad = math.radians(w_angle) + rad
                wx = x + math.cos(w_rad) * 3.4
                wy = y + math.sin(w_rad) * 3.4
                
                try:
                    bpy.ops.archimesh.create_window(width=1.2, height=1.0, depth=0.05)
                    vent = bpy.context.active_object
                except:
                    self.adapter.create_primitive("cube", location=(wx, wy, z + 1.5),
                                              scale=(0.6, 0.02, 0.5))
                    vent = bpy.context.active_object
                vent.location = (wx, wy, z + 1.5)
                vent.rotation_euler[2] = w_rad
                vent.name = f"Ventana_P{floor+1}_{w_angle}"
                self.asignar_material(vent, mat_vidrio)
        
        # Núcleo central iluminado (atrio)
        self.adapter.create_primitive("cylinder", location=(0, 0, 7.5),
                                  scale=(0.8, 0.8, 7.5))
        atrio = bpy.context.active_object
        atrio.name = "Atrio_Luminoso"
        self.asignar_material(atrio, mat_neon)
        
        # Escalera helicoidal alrededor del atrio
        for i in range(24):
            angle = i * 15
            z = i * 0.6
            rad = math.radians(angle)
            x = math.cos(rad) * 1.2
            y = math.sin(rad) * 1.2
            
            self.adapter.create_primitive("cube", location=(x, y, z),
                                      scale=(0.4, 0.15, 0.05))
            step = bpy.context.active_object
            step.name = f"Escalon_Helix_{i+1}"
            step.rotation_euler[2] = rad
            self.asignar_material(step, mat_acero)
        
        return {
            "status": "success",
            "model_id": "MOD-002_Torre_Helix_Corporativa",
            "elements": ["5_pisos_helix", "atrio_luminoso", "escalera_helix", "20_ventanas"],
            "materials": ["acero", "vidrio", "neon"]
        }
    
    def generar_casa_nomada(self) -> Dict[str, Any]:
        """
        MOD-003: Casa Nómada Modular
        Contenedores interconectados con terrazas flotantes.
        """
        self.adapter.clear_scene()
        self.crear_camara_y_luces()
        
        mat_contenedor = self.crear_material("Contenedor", (0.35, 0.4, 0.45))
        mat_terraza = self.crear_material("Madera_Terraza", (0.6, 0.45, 0.3))
        mat_vidrio = self.crear_material("Vidrio_Nomad", (0.8, 0.9, 0.95))
        mat_corten = self.crear_material("Corten", (0.65, 0.35, 0.25))
        
        # 3 contenedores en L
        contenedores = [
            ((0, 0, 1.25), (4, 1.2, 1.25)),      # Principal
            ((-3, 2, 1.25), (1.2, 3, 1.25)),     # Lateral izq
            ((3, 2, 1.25), (1.2, 3, 1.25))       # Lateral der
        ]
        
        for i, (loc, scale) in enumerate(contenedores):
            self.adapter.create_primitive("cube", location=loc, scale=scale)
            cont = bpy.context.active_object
            cont.name = f"Contenedor_{i+1}"
            self.asignar_material(cont, mat_contenedor)
            
            # Ventanas en cada contenedor
            try:
                bpy.ops.archimesh.create_window(width=1.5, height=0.8, depth=0.05)
                vent = bpy.context.active_object
            except:
                self.adapter.create_primitive("cube", location=(loc[0], loc[1]-1.3, loc[2]),
                                          scale=(0.75, 0.02, 0.4))
                vent = bpy.context.active_object
            vent.location = (loc[0], loc[1]-1.3, loc[2])
            vent.name = f"Ventana_Contenedor_{i+1}"
            self.asignar_material(vent, mat_vidrio)
        
        # Terraza flotante superior
        self.adapter.create_primitive("cube", location=(0, 1, 3.0),
                                  scale=(5, 3, 0.08))
        terraza = bpy.context.active_object
        terraza.name = "Terraza_Flotante"
        self.asignar_material(terraza, mat_terraza)
        
        # Escalera exterior a terraza
        for i in range(8):
            self.adapter.create_primitive("cube", 
                                      location=(2.5, 1 + i*0.2, 2.5 + i*0.15),
                                      scale=(0.3, 0.1, 0.05))
            step = bpy.context.active_object
            step.name = f"Escalon_Terraza_{i+1}"
            self.asignar_material(step, mat_corten)
        
        # Puerta principal
        try:
            bpy.ops.archimesh.create_door(width=1.0, height=2.0, depth=0.05)
            puerta = bpy.context.active_object
        except:
            self.adapter.create_primitive("cube", location=(0, -1.25, 1.0),
                                      scale=(0.5, 0.02, 1.0))
            puerta = bpy.context.active_object
        puerta.location = (0, -1.25, 1.0)
        puerta.name = "Puerta_Nomad"
        self.asignar_material(puerta, mat_corten)
        
        return {
            "status": "success",
            "model_id": "MOD-003_Casa_Nomada_Modular",
            "elements": ["3_contenedores", "terraza_flotante", "escalera_exterior", 
                        "3_ventanas", "puerta"],
            "materials": ["contenedor", "madera", "vidrio", "corten"]
        }
    
    def generar_galeria_luminica(self) -> Dict[str, Any]:
        """
        MOD-004: Galería Lumínica
        Espacio museístico con claraboyas y proyecciones.
        """
        self.adapter.clear_scene()
        self.crear_camara_y_luces()
        
        mat_marmol = self.crear_material("Marmol_Galeria", (0.95, 0.95, 0.97))
        mat_piedra = self.crear_material("Piedra_Volcanica", (0.25, 0.25, 0.27))
        mat_claraboia = self.crear_material("Claraboia", (0.9, 0.95, 1.0))
        mat_negro = self.crear_material("Negro_Mate", (0.05, 0.05, 0.05))
        
        # Suelo de mármol
        self.adapter.create_primitive("cube", location=(0, 0, 0.05),
                                  scale=(12, 10, 0.05))
        suelo = bpy.context.active_object
        suelo.name = "Suelo_Marmol"
        self.asignar_material(suelo, mat_marmol)
        
        # 8 Columnas monumentales
        for i, x in enumerate([-9, -5, -2, 2, 5, 9]):
            for j, y in enumerate([-8, 8]):
                try:
                    bpy.ops.archimesh.create_column(column_height=5, column_radius=0.4)
                    col = bpy.context.active_object
                except:
                    self.adapter.create_primitive("cylinder", location=(x, y, 2.5),
                                              scale=(0.4, 0.4, 2.5))
                    col = bpy.context.active_object
                col.location = (x, y, 2.5)
                col.name = f"Columna_Monumental_{i}_{j}"
                self.asignar_material(col, mat_piedra)
        
        # Claraboyas en techo (cilindros de vidrio)
        claraboyas = [(-4, -3), (4, -3), (-4, 3), (4, 3), (0, 0)]
        for i, (x, y) in enumerate(claraboyas):
            self.adapter.create_primitive("cylinder", location=(x, y, 5.1),
                                      scale=(1.5, 1.5, 0.1))
            clar = bpy.context.active_object
            clar.name = f"Claraboia_{i+1}"
            self.asignar_material(clar, mat_claraboia)
        
        # Muros laterales con huecos para luz
        for x in [-11.5, 11.5]:
            self.adapter.create_primitive("cube", location=(x, 0, 2.5),
                                      scale=(0.3, 10, 2.5))
            muro = bpy.context.active_object
            muro.name = f"Muro_Lateral_{x}"
            self.asignar_material(muro, mat_piedra)
            
            # Huecos de luz
            for y in [-6, -2, 2, 6]:
                try:
                    bpy.ops.archimesh.create_window(width=2.0, height=2.5, depth=0.1)
                    vent = bpy.context.active_object
                except:
                    self.adapter.create_primitive("cube", location=(x*1.01, y, 2.5),
                                              scale=(1.0, 0.05, 1.25))
                    vent = bpy.context.active_object
                vent.location = (x*1.01, y, 2.5)
                vent.name = f"Hueco_Luz_{x}_{y}"
                self.asignar_material(vent, mat_claraboia)
        
        # Escultura central abstracta
        self.adapter.create_primitive("ico_sphere", location=(0, 0, 2),
                                  scale=(1.5, 1.5, 1.5))
        escultura = bpy.context.active_object
        escultura.name = "Escultura_Luminica"
        self.asignar_material(escultura, mat_negro)
        
        # Entrada monumental
        try:
            bpy.ops.archimesh.create_door(width=3.0, height=3.5, depth=0.1)
            puerta = bpy.context.active_object
        except:
            self.adapter.create_primitive("cube", location=(0, -10, 1.75),
                                      scale=(1.5, 0.05, 1.75))
            puerta = bpy.context.active_object
        puerta.location = (0, -10, 1.75)
        puerta.name = "Entrada_Monumental"
        self.asignar_material(puerta, mat_piedra)
        
        return {
            "status": "success",
            "model_id": "MOD-004_Galeria_Luminica",
            "elements": ["suelo_marmol", "12_columnas", "5_claraboyas", 
                        "8_huecos_luz", "escultura_central", "entrada"],
            "materials": ["marmol", "piedra_volcanica", "vidrio"]
        }
    
    def generar_orbitals_alpha(self) -> Dict[str, Any]:
        """
        MOD-005: Orbitals Habitat Alpha
        Estación espacial toroidal con gravedad artificial.
        """
        self.adapter.clear_scene()
        self.crear_camara_y_luces()
        
        mat_titanio = self.crear_material("Titanio", (0.6, 0.62, 0.65))
        mat_panel = self.crear_material("Panel_Solar", (0.15, 0.15, 0.35))
        mat_visor = self.crear_material("Visor_Espacial", (0.4, 0.85, 0.95))
        mat_nuclear = self.crear_material("Reactor", (0.9, 0.6, 0.2))
        
        # Anillo toroidal principal (habitat)
        major_radius = 8
        minor_radius = 2
        segments = 16
        
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * major_radius
            y = math.sin(angle) * major_radius
            
            # Módulo del anillo
            self.adapter.create_primitive("cylinder", location=(x, y, 0),
                                      scale=(minor_radius, minor_radius, 3))
            modulo = bpy.context.active_object
            modulo.rotation_euler[0] = 1.5708
            modulo.rotation_euler[2] = angle
            modulo.name = f"Modulo_Habitat_{i+1}"
            self.asignar_material(modulo, mat_titanio)
            
            # Ventanas visor en cada módulo
            wx = math.cos(angle) * (major_radius + 1.5)
            wy = math.sin(angle) * (major_radius + 1.5)
            
            try:
                bpy.ops.archimesh.create_window(width=1.5, height=0.8, depth=0.1)
                vent = bpy.context.active_object
            except:
                self.adapter.create_primitive("cube", location=(wx, wy, 0.5),
                                          scale=(0.75, 0.05, 0.4))
                vent = bpy.context.active_object
            vent.location = (wx, wy, 0.5)
            vent.rotation_euler[2] = angle
            vent.name = f"Visor_{i+1}"
            self.asignar_material(vent, mat_visor)
        
        # Núcleo central (reactor + docks)
        self.adapter.create_primitive("sphere", location=(0, 0, 0), scale=(3, 3, 3))
        nucleo = bpy.context.active_object
        nucleo.name = "Nucleo_Central"
        self.asignar_material(nucleo, mat_titanio)
        
        # Anillos de conexión
        for z in [-2, 0, 2]:
            self.adapter.create_primitive("torus", location=(0, 0, z),
                                      scale=(major_radius, minor_radius*0.3, 0.3))
            anillo = bpy.context.active_object
            anillo.rotation_euler[0] = 1.5708
            anillo.name = f"Anillo_Estructural_{z}"
            self.asignar_material(anillo, mat_titanio)
        
        # Paneles solares externos (8 paneles grandes)
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x = math.cos(rad) * 14
            y = math.sin(rad) * 14
            
            self.adapter.create_primitive("cube", location=(x, y, 4),
                                      scale=(3, 0.05, 1.5))
            panel = bpy.context.active_object
            panel.rotation_euler[2] = rad
            panel.name = f"Panel_Solar_{angle}"
            self.asignar_material(panel, mat_panel)
            
            # Brazo conector
            self.adapter.create_primitive("cylinder", location=(x*0.7, y*0.7, 2),
                                      scale=(0.1, 0.1, 2))
            brazo = bpy.context.active_object
            brazo.rotation_euler[0] = 1.5708
            brazo.name = f"Brazo_{angle}"
        
        # Antenas de comunicación
        for angle in [0, 120, 240]:
            rad = math.radians(angle)
            x = math.cos(rad) * 4
            y = math.sin(rad) * 4
            
            self.adapter.create_primitive("cylinder", location=(x, y, 5),
                                      scale=(0.05, 0.05, 4))
            antena = bpy.context.active_object
            antena.name = f"Antena_{angle}"
            
            # Plato parabólico
            self.adapter.create_primitive("cone", location=(x, y, 7),
                                      scale=(0.8, 0.8, 0.3))
            plato = bpy.context.active_object
            plato.rotation_euler[0] = 3.14159
            plato.name = f"Plato_{angle}"
        
        return {
            "status": "success",
            "model_id": "MOD-005_Orbitals_Habitat_Alpha",
            "elements": ["16_modulos_habitat", "nucleo_central", "3_anillos_estructura",
                        "16_visores", "8_paneles_solares", "3_antenas"],
            "materials": ["titanio", "panel_solar", "visor", "reactor"]
        }
    
    # ============ HANDLER INTERFACE ============
    
    def execute(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ejecuta el comando de generación.
        
        Comandos:
        - "generate_all": Genera los 5 modelos
        - "generate_pabellon": Solo MOD-001
        - "generate_torre": Solo MOD-002
        - "generate_casa": Solo MOD-003
        - "generate_galeria": Solo MOD-004
        - "generate_orbitals": Solo MOD-005
        """
        if not self.ensure_archimesh():
            return {"status": "error", "message": "Archimesh no disponible"}
        
        generators = {
            "pabellon": self.generar_pabellon_cristal_zen,
            "torre": self.generar_torre_helix,
            "casa": self.generar_casa_nomada,
            "galeria": self.generar_galeria_luminica,
            "orbitals": self.generar_orbitals_alpha
        }
        
        command = command.lower()
        
        if command == "generate_all":
            results = []
            for name, gen in generators.items():
                log_info(f"[ARCHIMESH_GEN] Generando {name}...")
                result = gen()
                results.append(result)
                
                # Guardar archivo
                if result["status"] == "success":
                    output_path = params.get("output_dir", "archivo_zuly/temp_arena")
                    blend_path = f"{output_path}/{result['model_id']}_ARCHIMESH.blend"
                    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
                    result["file_path"] = blend_path
            
            return {
                "status": "success",
                "models_generated": len(results),
                "results": results
            }
        
        elif command in generators:
            result = generators[command]()
            
            if result["status"] == "success":
                output_path = params.get("output_dir", "archivo_zuly/temp_arena")
                blend_path = f"{output_path}/{result['model_id']}_ARCHIMESH.blend"
                bpy.ops.wm.save_as_mainfile(filepath=blend_path)
                result["file_path"] = blend_path
            
            return result
        
        else:
            return {
                "status": "error",
                "message": f"Comando '{command}' no reconocido",
                "available": list(generators.keys()) + ["generate_all"]
            }


# Instancia singleton
archimesh_generator = ArchimeshGeneratorHandler()

# Handler interface para Zuly
HANDLERS = {
    "archimesh_generator": archimesh_generator.execute,
    "generate_pabellon": lambda p: archimesh_generator.execute("pabellon", p),
    "generate_torre": lambda p: archimesh_generator.execute("torre", p),
    "generate_casa": lambda p: archimesh_generator.execute("casa", p),
    "generate_galeria": lambda p: archimesh_generator.execute("galeria", p),
    "generate_orbitals": lambda p: archimesh_generator.execute("orbitals", p),
    "generate_all_archimesh": lambda p: archimesh_generator.execute("generate_all", p)
}
