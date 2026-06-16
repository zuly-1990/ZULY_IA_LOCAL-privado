# core/learning/youtube_learner.py
import os
import json
from core.utils.logging import log_info, log_error, log_warning

class YouTubeVisionLearner:
    """
    Agente encargado de buscar tutoriales en YouTube, extraer sus transcripciones
    y obtener fotogramas visuales para alimentar el cerebro multimodal de Zuly.
    """
    def __init__(self):
        self.download_dir = os.path.join(os.getcwd(), "ZULY_LAB", "youtube_cache")
        os.makedirs(self.download_dir, exist_ok=True)

    def search_and_extract(self, query: str, max_results: int = 1) -> dict:
        """
        Busca un tutorial, extrae subtítulos y fotogramas.
        Retorna un diccionario con 'text' y 'frames_paths'.
        """
        log_info(f"🔍 Buscando conocimiento en YouTube: {query}")
        result = {
            "success": False,
            "video_url": "",
            "transcript": "",
            "frames": []
        }

        try:
            from youtubesearchpython import VideosSearch
            videosSearch = VideosSearch(query + " blender 3.6 geometry nodes", limit=max_results)
            results = videosSearch.result()
            
            if not results['result']:
                log_error("No se encontraron tutoriales en YouTube.")
                return result
                
            video = results['result'][0]
            video_id = video['id']
            video_url = video['link']
            log_info(f"🎬 Video encontrado: {video['title']} ({video_url})")
            
            result["video_url"] = video_url
            result["title"] = video['title']
            
            # 1. Extraer Transcripción
            result["transcript"] = self._get_transcript(video_id)
            
            # 2. Extraer Fotogramas (Opcional, no rompe si falla)
            frames = self._extract_frames(video_url, video_id)
            result["frames"] = frames
            
            result["success"] = True
            
        except ImportError:
            log_error("Faltan dependencias. Instala: pip install youtube-search-python youtube-transcript-api yt-dlp opencv-python")
        except Exception as e:
            log_error(f"Error en búsqueda de YouTube: {e}")
            
        return result

    def _get_transcript(self, video_id: str) -> str:
        """Extrae la transcripción del video (traducida al inglés si es necesario)."""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Intentar obtener transcripción (preferible en inglés, o traducir)
            try:
                transcript = transcript_list.find_transcript(['en', 'es'])
            except:
                # Si no hay en.es, tomar la primera generada automáticamente y traducirla
                transcript = transcript_list.find_generated_transcript(['en', 'es', 'ru', 'hi', 'pt', 'fr'])
                transcript = transcript.translate('en')
                
            text_data = transcript.fetch()
            full_text = " ".join([t['text'] for t in text_data])
            log_info(f"📝 Transcripción extraída con éxito ({len(full_text)} caracteres).")
            return full_text
            
        except Exception as e:
            log_warning(f"No se pudo extraer transcripción: {e}")
            return "No transcript available."

    def _extract_frames(self, video_url: str, video_id: str) -> list:
        """Descarga el video (baja calidad) y extrae 3 fotogramas representativos."""
        frames_paths = []
        try:
            import yt_dlp
            import cv2
            
            video_path = os.path.join(self.download_dir, f"{video_id}.mp4")
            
            # Si no existe, lo descargamos en la peor calidad posible para que sea rápido
            if not os.path.exists(video_path):
                log_info("⬇️ Descargando video para análisis visual...")
                ydl_opts = {
                    'format': 'worstvideo[ext=mp4]', 
                    'outtmpl': video_path,
                    'quiet': True
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
            
            # Extraer fotogramas con OpenCV
            log_info("🖼️ Extrayendo fotogramas del video...")
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Queremos 3 fotogramas: al 25%, 50% y 75% del video
            targets = [int(total_frames * 0.25), int(total_frames * 0.50), int(total_frames * 0.75)]
            
            for i, target_frame in enumerate(targets):
                cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
                ret, frame = cap.read()
                if ret:
                    frame_path = os.path.join(self.download_dir, f"{video_id}_frame_{i}.jpg")
                    cv2.imwrite(frame_path, frame)
                    frames_paths.append(frame_path)
                    
            cap.release()
            log_info(f"📸 {len(frames_paths)} fotogramas extraídos exitosamente.")
            
        except ImportError:
            log_warning("No se instaló yt-dlp o opencv-python. Se omite análisis visual.")
        except Exception as e:
            log_warning(f"Error extrayendo fotogramas: {e}")
            
        return frames_paths
