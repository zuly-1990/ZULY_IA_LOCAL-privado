"""
archiver.py

FASE 19: Archivado y Compresión de Sesiones

Gestiona archivado automático de logs y trazas con compresión gzip.
"""

import os
import json
import gzip
import shutil
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
from core.utils.logging import log_info, log_debug, log_warning


class SessionArchiver:
    """
    Archiva sesiones antiguas con compresión gzip.
    
    Responsabilidades:
    - Mover archivos antiguos a archives/
    - Comprimir con gzip
    - Indexar para búsqueda
    - Restaurar si es necesario
    """
    
    def __init__(self, base_dir: str):
        """
        Inicializa el archivador.
        
        Args:
            base_dir: Directorio base (ej: 'logs/actions')
        """
        self.base_dir = Path(base_dir)
        self.archive_dir = self.base_dir / 'archives'
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear subdirectorios por mes
        self.current_month_dir = self._get_month_dir(datetime.now())
        self.current_month_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_month_dir(self, date: datetime) -> Path:
        """Obtiene directorio de archivo para un mes."""
        month_str = date.strftime("%Y-%m")
        return self.archive_dir / month_str
    
    def archive_file(self, filepath: str, compress: bool = True) -> Optional[str]:
        """
        Archiva un archivo individual.
        
        Args:
            filepath: Ruta completa del archivo a archivar
            compress: Si se comprime con gzip
        
        Returns:
            Ruta del archivo archivado, o None si falló
        """
        source_path = Path(filepath)
        
        if not source_path.exists():
            log_warning(f"Archivo no existe: {filepath}")
            return None
        
        # Determinar directorio de destino basado en fecha del archivo
        file_mtime = datetime.fromtimestamp(source_path.stat().st_mtime)
        target_dir = self._get_month_dir(file_mtime)
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Nombre del archivo archivado
        if compress:
            target_filename = source_path.name + '.gz'
            target_path = target_dir / target_filename
            
            # Comprimir
            with open(source_path, 'rb') as f_in:
                with gzip.open(target_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            log_debug(f"📦 Archivado y comprimido: {source_path.name} → {target_path}")
        else:
            target_path = target_dir / source_path.name
            shutil.move(str(source_path), str(target_path))
            log_debug(f"📦 Archivado: {source_path.name} → {target_path}")
        
        # Eliminar original
        if source_path.exists():
            source_path.unlink()
        
        # Actualizar índice
        self._update_index(target_path, file_mtime)
        
        return str(target_path)
    
    def archive_old_files(self, age_days: int, pattern: str = "*.json") -> List[str]:
        """
        Archiva todos los archivos más antiguos que N días.
        
        Args:
            age_days: Edad mínima en días para archivar
            pattern: Patrón de archivos (glob)
        
        Returns:
            Lista de archivos archivados
        """
        cutoff_date = datetime.now() - timedelta(days=age_days)
        archived = []
        
        for filepath in self.base_dir.glob(pattern):
            # Ignorar directorio de archives
            if 'archives' in str(filepath):
                continue
            
            file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            
            if file_mtime < cutoff_date:
                result = self.archive_file(str(filepath))
                if result:
                    archived.append(result)
        
        if archived:
            log_info(f"📦 Archivados {len(archived)} archivos antiguos (>{age_days} días)")
        
        return archived
    
    def _update_index(self, filepath: Path, file_date: datetime):
        """
        Actualiza el índice de archives.
        
        Args:
            filepath: Ruta del archivo archivado
            file_date: Fecha del archivo
        """
        month_dir = filepath.parent
        index_path = month_dir / 'index.json'
        
        # Cargar índice existente
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
        else:
            index = {'month': month_dir.name, 'files': []}
        
        # Agregar entrada
        index['files'].append({
            'filename': filepath.name,
            'archived_at': datetime.now().isoformat(),
            'original_date': file_date.isoformat(),
            'compressed': filepath.suffix == '.gz',
            'size_bytes': filepath.stat().st_size
        })
        
        # Guardar índice
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
    
    def restore_file(self, archived_filepath: str, target_dir: Optional[str] = None) -> Optional[str]:
        """
        Restaura un archivo archivado.
        
        Args:
            archived_filepath: Ruta del archivo archivado
            target_dir: Directorio de destino (None = base_dir)
        
        Returns:
            Ruta del archivo restaurado
        """
        source_path = Path(archived_filepath)
        
        if not source_path.exists():
            log_warning(f"Archivo archivado no existe: {archived_filepath}")
            return None
        
        target_directory = Path(target_dir) if target_dir else self.base_dir
        target_directory.mkdir(parents=True, exist_ok=True)
        
        # Si está comprimido, descomprimir
        if source_path.suffix == '.gz':
            target_filename = source_path.stem  # Quitar .gz
            target_path = target_directory / target_filename
            
            with gzip.open(source_path, 'rb') as f_in:
                with open(target_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            log_info(f"📂 Restaurado y descomprimido: {source_path.name}")
        else:
            target_path = target_directory / source_path.name
            shutil.copy(str(source_path), str(target_path))
            log_info(f"📂 Restaurado: {source_path.name}")
        
        return str(target_path)
    
    def get_archive_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de archives.
        
        Returns:
            Dict con estadísticas
        """
        total_files = 0
        total_size = 0
        months = []
        
        for month_dir in self.archive_dir.iterdir():
            if month_dir.is_dir():
                month_files = list(month_dir.glob('*'))
                # Excluir index.json del conteo
                month_files = [f for f in month_files if f.name != 'index.json']
                
                month_size = sum(f.stat().st_size for f in month_files)
                
                total_files += len(month_files)
                total_size += month_size
                
                months.append({
                    'month': month_dir.name,
                    'file_count': len(month_files),
                    'size_bytes': month_size
                })
        
        return {
            'total_archived_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'months': months
        }
    
    def search_archives(self, date_from: Optional[datetime] = None, 
                       date_to: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """
        Busca archives en un rango de fechas.
        
        Args:
            date_from: Fecha inicial (None = sin límite)
            date_to: Fecha final (None = sin límite)
        
        Returns:
            Lista de archivos que coinciden
        """
        results = []
        
        for month_dir in self.archive_dir.iterdir():
            if not month_dir.is_dir():
                continue
            
            index_path = month_dir / 'index.json'
            if not index_path.exists():
                continue
            
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            
            for file_info in index.get('files', []):
                file_date = datetime.fromisoformat(file_info['original_date'])
                
                # Filtrar por rango
                if date_from and file_date < date_from:
                    continue
                if date_to and file_date > date_to:
                    continue
                
                results.append({
                    'filename': file_info['filename'],
                    'path': str(month_dir / file_info['filename']),
                    'date': file_info['original_date'],
                    'compressed': file_info['compressed'],
                    'size_bytes': file_info['size_bytes']
                })
        
        return results
