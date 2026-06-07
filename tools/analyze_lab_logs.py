import json
import glob
import os
from pathlib import Path
from statistics import mean

def analyze_logs():
    base_path = Path(r"C:\Users\Admin\Desktop\ZULY_IA_LOCAL")
    logs_dir = base_path / "ZULY_LAB" / "logs_sesiones"
    report_file = base_path / "ZULY_LAB" / "REPORT_FASE_A.md"
    
    # Asegurar que existe el directorio
    if not logs_dir.exists():
        print(f"Error: No se encuentra el directorio de logs: {logs_dir}")
        return

    json_files = glob.glob(str(logs_dir / "*.json"))
    
    total_executions = 0
    successes = 0
    failures = 0
    times = []
    errors = {}
    exercise_stats = {}

    print(f"Analizando {len(json_files)} logs en {logs_dir}...")

    for fpath in json_files:
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Filter for Phase A (starts with A)
            ex_code = data.get('ejercicio', 'UNKNOWN')
            if not ex_code.startswith('A'):
                continue
                
            total_executions += 1
            is_success = data.get('exito', False)
            
            # Ignorar simulaciones si queremos solo real? 
            # El usuario pidió "científico", mezclaremos ambos por ahora pero podríamos distinguir
            # si el log tuviera esa meta-data. Los logs actuales no distinguen explícitamente mock vs real en top level
            # pero asumiremos todos son válidos para estadística de "capacidad del agente".
            
            if is_success:
                successes += 1
            else:
                failures += 1
            
            t_total = data.get('tiempo_total_segundos', 0)
            times.append(t_total)
            
            # Per exercise stats
            if ex_code not in exercise_stats:
                exercise_stats[ex_code] = {'total': 0, 'success': 0, 'time': []}
            exercise_stats[ex_code]['total'] += 1
            if is_success:
                exercise_stats[ex_code]['success'] += 1
            exercise_stats[ex_code]['time'].append(t_total)

            # Errors
            if not is_success:
                for err in data.get('errores', []):
                    errors[err] = errors.get(err, 0) + 1

        except Exception as e:
            print(f"Error leyendo {fpath}: {e}")

    if total_executions == 0:
        print("No se encontraron ejecuciones de Fase A.")
        return

    # Generate Report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 📊 Reporte Científico Fase A (Estructura)\n\n")
        f.write(f"**Fecha Análisis:** {os.path.getmtime(report_file) if os.path.exists(report_file) else 'Recién generado'}\n\n")
        f.write(f"**Total Ejecuciones:** {total_executions}\n")
        f.write(f"**Tasa de Éxito Global:** {(successes/total_executions*100):.1f}% ({successes}/{total_executions})\n")
        if times:
            f.write(f"**Tiempo Promedio Global:** {mean(times):.2f}s\n\n")
        
        f.write("## 📈 Desglose por Ejercicio\n\n")
        f.write("| Ejercicio | Ejecuciones | Éxito | Tiempo Promedio |\n")
        f.write("|-----------|-------------|-------|-----------------|\n")
        
        for ex in sorted(exercise_stats.keys()):
            stats = exercise_stats[ex]
            success_rate = (stats['success'] / stats['total']) * 100
            avg_time = mean(stats['time']) if stats['time'] else 0
            f.write(f"| **{ex}** | {stats['total']} | {success_rate:.1f}% | {avg_time:.2f}s |\n")
            
        f.write("\n## ⚠️ Top Errores Detectados\n\n")
        if errors:
            sorted_errors = sorted(errors.items(), key=lambda x: x[1], reverse=True)
            for err, count in sorted_errors[:5]:
                 f.write(f"- **({count})**: {err}\n")
        else:
            f.write("No se detectaron errores significativos.\n")

    print(f"✅ Reporte generado exitosamente en: {report_file}")
    
    # Imprimir resumen en consola
    print(f"\nRESUMEN RÁPIDO:")
    print(f"Tasa de Éxito: {(successes/total_executions*100):.1f}%")
    print(f"Errores más comunes: {list(errors.keys())[:3] if errors else 'Ninguno'}")

if __name__ == "__main__":
    analyze_logs()
