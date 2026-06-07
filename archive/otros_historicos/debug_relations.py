from core.structural_interpreter import StructuralInterpreter
import json

interpreter = StructuralInterpreter()
text = "Crea un cubo en 0,0,0 y una esfera encima del cubo"
result = interpreter.interpret(text)
print(f"ELEMENTS: {[el['id'] for el in result['elements']]}")
print(f"COUNT: {len(result['relations'])}")
for r in result['relations']:
    print(r)
