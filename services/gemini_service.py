import base64
import logging
import aiohttp
import json
from config import GEMINI_API_KEY

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    def encode_image(self, image_path: str) -> str:
        """Кодирует изображение в base64"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            logger.error(f"Ошибка при кодировании изображения: {e}")
            raise
    
    async def analyze_food(self, image_path: str, weight_grams: int) -> str:
        """
        Анализирует фото еды с помощью Google Gemini API
        
        Args:
            image_path: путь к файлу изображения
            weight_grams: вес еды в граммах
            
        Returns:
            Строка с анализом КБЖУ и витаминов
        """
        try:
            # Кодируем изображение
            base64_image = self.encode_image(image_path)
            
            # Определяем MIME тип
            mime_type = "image/jpeg"
            if image_path.lower().endswith('.png'):
                mime_type = "image/png"
            
            prompt = f"""
            Проанализируй это изображение еды и определи:
            
            1. Какие продукты/блюда видны на фото (будь внимательным к деталям)
            2. Рассчитай для {weight_grams} грамм:
               - Калории (ккал)
               - Белки (г)
               - Жиры (г) 
               - Углеводы (г)
            3. Укажи только ВИТАМИНЫ и МИНЕРАЛЫ с процентом от дневной нормы (НЕ включай холестерин, клетчатку и другие не-витаминные вещества)
            
            Отвечай на русском языке в следующем формате:
            
            ПРОДУКТЫ: [детальное описание всех видимых продуктов и ингредиентов]
            
            ПИЩЕВАЯ ЦЕННОСТЬ ({weight_grams} г):
            - Калории: XXX ккал
            - Белки: XX г
            - Жиры: XX г
            - Углеводы: XX г
            
            ВИТАМИНЫ И МИНЕРАЛЫ (% от дневной нормы):
            - Витамин A: XX% от дневной нормы
            - Витамин C: XX% от дневной нормы
            - Витамин K: XX% от дневной нормы
            - Витамин E: XX% от дневной нормы
            - Витамин B12: XX% от дневной нормы
            - Фолиевая кислота: XX% от дневной нормы
            - Калий: XX% от дневной нормы
            - Магний: XX% от дневной нормы
            - Железо: XX% от дневной нормы
            - Кальций: XX% от дневной нормы
            [только витамины и минералы, НЕ холестерин или клетчатку]
            
            ВАЖНО: 
            - Анализируй ЛЮБОЕ изображение с едой, даже если это сложные блюда, десерты, напитки или готовые продукты
            - Всегда давай максимально точную оценку на основе визуального анализа
            - Используй стандартные дневные нормы витаминов и минералов для взрослого человека
            - В разделе витаминов указывай ТОЛЬКО витамины (A, B, C, D, E, K и т.д.) и минералы (железо, кальций, магний, калий и т.д.)
            - НЕ включай холестерин, клетчатку, антиоксиданты и другие соединения - только витамины и минералы!
            """
            
            # Подготавливаем данные для запроса
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            },
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ошибка Gemini API {response.status}: {error_text}")
                        return f"Ошибка анализа изображения: {response.status}"
                    
                    result = await response.json()
                    
                    # Извлекаем текст ответа
                    if 'candidates' in result and len(result['candidates']) > 0:
                        if 'content' in result['candidates'][0]:
                            if 'parts' in result['candidates'][0]['content']:
                                if len(result['candidates'][0]['content']['parts']) > 0:
                                    return result['candidates'][0]['content']['parts'][0]['text']
                    
                    logger.error(f"Неожиданный формат ответа Gemini: {result}")
                    return "Не удалось получить анализ изображения"
            
        except Exception as e:
            logger.error(f"Ошибка при анализе еды через Gemini: {e}")
            return f"Произошла ошибка при анализе изображения: {str(e)}"
    
    async def analyze_food_auto_weight(self, image_path: str) -> str:
        """
        Анализирует фото еды с автоматическим определением веса Gemini
        
        Args:
            image_path: путь к файлу изображения
            
        Returns:
            Строка с анализом КБЖУ и витаминов с автоопределенным весом
        """
        try:
            # Кодируем изображение
            base64_image = self.encode_image(image_path)
            
            # Определяем MIME тип
            mime_type = "image/jpeg"
            if image_path.lower().endswith('.png'):
                mime_type = "image/png"
            
            prompt = f"""
            Проанализируй это изображение еды и определи:
            
            1. Какие продукты/блюда видны на фото (будь внимательным к деталям)
            2. Оцени примерный вес порции в граммах на основе визуального анализа
            3. Рассчитай для этого веса:
               - Калории (ккал)
               - Белки (г)
               - Жиры (г) 
               - Углеводы (г)
            4. Укажи только ВИТАМИНЫ и МИНЕРАЛЫ с процентом от дневной нормы
            
            Отвечай на русском языке в следующем формате:
            
            ПРОДУКТЫ: [детальное описание всех видимых продуктов и ингредиентов]
            
            ПРИМЕРНЫЙ ВЕС: [XXX г] (визуальная оценка)
            
            ПИЩЕВАЯ ЦЕННОСТЬ (на примерный вес):
            - Калории: XXX ккал
            - Белки: XX г
            - Жиры: XX г
            - Углеводы: XX г
            
            ВИТАМИНЫ И МИНЕРАЛЫ (% от дневной нормы):
            - Витамин A: XX% от дневной нормы
            - Витамин C: XX% от дневной нормы
            - Витамин K: XX% от дневной нормы
            - Витамин E: XX% от дневной нормы
            - Витамин B12: XX% от дневной нормы
            - Фолиевая кислота: XX% от дневной нормы
            - Калий: XX% от дневной нормы
            - Магний: XX% от дневной нормы
            - Железо: XX% от дневной нормы
            - Кальций: XX% от дневной нормы
            [только витамины и минералы, НЕ холестерин или клетчатку]
            
            ВАЖНО: 
            - Внимательно оцени размер порции по визуальным признакам (размер тарелки, сравнение с привычными объектами)
            - Анализируй ЛЮБОЕ изображение с едой, даже если это сложные блюда, десерты, напитки или готовые продукты
            - Всегда давай максимально точную оценку на основе визуального анализа
            - Используй стандартные дневные нормы витаминов и минералов для взрослого человека
            - В разделе витаминов указывай ТОЛЬКО витамины (A, B, C, D, E, K и т.д.) и минералы (железо, кальций, магний, калий и т.д.)
            - НЕ включай холестерин, клетчатку, антиоксиданты и другие соединения - только витамины и минералы!
            """
            
            # Подготавливаем данные для запроса
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            },
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            # Выполняем запрос
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status != 200:
                        error_text = await response.text()
                        logger.error(f"Ошибка Gemini API {response.status}: {error_text}")
                        return f"Ошибка анализа изображения: {response.status}"
                    
                    result = await response.json()
                    
                    # Извлекаем текст ответа
                    if 'candidates' in result and len(result['candidates']) > 0:
                        if 'content' in result['candidates'][0]:
                            if 'parts' in result['candidates'][0]['content']:
                                if len(result['candidates'][0]['content']['parts']) > 0:
                                    return result['candidates'][0]['content']['parts'][0]['text']
                    
                    logger.error(f"Неожиданный формат ответа Gemini: {result}")
                    return "Не удалось получить анализ изображения"
            
        except Exception as e:
            logger.error(f"Ошибка при анализе еды через Gemini (автовес): {e}")
            return f"Произошла ошибка при анализе изображения: {str(e)}"
