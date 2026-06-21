import time
import logging
from core.agent import Agent

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')
logger = logging.getLogger("MassiveTrainer")

def run_massive_training():
    logger.info("===============================================")
    logger.info(" INICIANDO ENTRENAMIENTO MASIVO C3 (DEEPSEEK)")
    logger.info("===============================================")
    
    agent = Agent()
    
    # Lista de desafíos arquitectónicos de alta complejidad
    desafios = [
        "descomponer: crea un rascacielos de cristal de 50 pisos con pilares de acero",
        "descomponer: crea un estadio moderno con techo retráctil y gradas perimetrales",
        "descomponer: crea una ciudad futurista estilo cyberpunk con puentes colgantes",
        "descomponer: crea una catedral gótica con arcos ojivales y vitrales",
        "descomponer: crea un puente atirantado de alta resistencia con cables tensores",
        "descomponer: crea un museo de arte abstracto con paredes curvas y luz cenital"
    ]
    
    exitos = 0
    fallos = 0
    
    for i, desafio in enumerate(desafios, 1):
        logger.info(f"\n[{i}/{len(desafios)}] Procesando: '{desafio}'")
        try:
            start_time = time.time()
            result = agent.process_natural_request(desafio)
            elapsed = time.time() - start_time
            
            if result.get('success'):
                logger.info(f"✅ EXITO ({elapsed:.2f}s). Patrón almacenado en memoria C2.")
                exitos += 1
            else:
                logger.error(f"❌ FALLO ({elapsed:.2f}s). Razón: {result.get('error', 'Desconocido')}")
                fallos += 1
                
        except Exception as e:
            logger.error(f"❌ ERROR CRITICO en el desafío {i}: {e}")
            fallos += 1
            
        time.sleep(2) # Pausa por rate-limits
        
    logger.info("\n===============================================")
    logger.info(f" ENTRENAMIENTO FINALIZADO: {exitos} exitosos, {fallos} fallidos")
    logger.info("===============================================")

if __name__ == "__main__":
    run_massive_training()
