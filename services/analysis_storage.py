import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AnalysisStorage:
    """Хранилище последних анализов пользователей для возможности редактирования"""
    
    def __init__(self):
        # В памяти храним последние анализы пользователей
        # В продакшене лучше использовать Redis или базу данных
        self._storage: Dict[int, Dict[str, Any]] = {}
        self._cleanup_interval = timedelta(hours=2)  # Очищаем старые записи через 2 часа
    
    def store_analysis(self, user_id: int, analysis_text: str, image_path: str, weight: Optional[int] = None):
        """
        Сохраняет последний анализ пользователя
        
        Args:
            user_id: ID пользователя Telegram
            analysis_text: Текст анализа от Gemini
            image_path: Путь к изображению (для повторного анализа)
            weight: Вес в граммах (если был указан)
        """
        if user_id is None:
            logger.error("user_id не может быть None")
            return
            
        self._storage[user_id] = {
            'analysis_text': analysis_text,
            'image_path': image_path,
            'weight': weight,
            'timestamp': datetime.now(),
            'original_analysis': analysis_text  # Сохраняем оригинальный анализ
        }
        
        logger.info(f"Сохранен анализ для пользователя {user_id}")
        self._cleanup_old_entries()
    
    def get_last_analysis(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает последний анализ пользователя
        
        Args:
            user_id: ID пользователя Telegram
            
        Returns:
            Словарь с данными анализа или None
        """
        analysis = self._storage.get(user_id)
        if analysis:
            # Проверяем, не устарел ли анализ
            if datetime.now() - analysis['timestamp'] > self._cleanup_interval:
                del self._storage[user_id]
                return None
        
        return analysis
    
    def update_analysis(self, user_id: int, updated_analysis: str):
        """
        Обновляет анализ пользователя
        
        Args:
            user_id: ID пользователя Telegram  
            updated_analysis: Обновленный текст анализа
        """
        if user_id in self._storage:
            self._storage[user_id]['analysis_text'] = updated_analysis
            self._storage[user_id]['timestamp'] = datetime.now()
            logger.info(f"Обновлен анализ для пользователя {user_id}")
    
    def clear_analysis(self, user_id: int):
        """Удаляет анализ пользователя"""
        if user_id in self._storage:
            del self._storage[user_id]
            logger.info(f"Удален анализ для пользователя {user_id}")
    
    def has_recent_analysis(self, user_id: int) -> bool:
        """Проверяет, есть ли у пользователя недавний анализ"""
        analysis = self.get_last_analysis(user_id)
        return analysis is not None
    
    def _cleanup_old_entries(self):
        """Очищает устаревшие записи"""
        current_time = datetime.now()
        expired_users = []
        
        for user_id, analysis in self._storage.items():
            if current_time - analysis['timestamp'] > self._cleanup_interval:
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self._storage[user_id]
        
        if expired_users:
            logger.info(f"Удалены устаревшие анализы для {len(expired_users)} пользователей")

# Глобальный экземпляр хранилища
analysis_storage = AnalysisStorage()
