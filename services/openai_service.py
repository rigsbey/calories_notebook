import base64
import logging
from openai import OpenAI
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
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
        Анализирует фото еды с помощью OpenAI GPT-4 Vision
        
        Args:
            image_path: путь к файлу изображения
            weight_grams: вес еды в граммах
            
        Returns:
            Строка с анализом КБЖУ и витаминов
        """
        try:
            # Кодируем изображение
            base64_image = self.encode_image(image_path)
            
            prompt = f"""
            Проанализируй это изображение еды и определи:
            
            1. Какие продукты/блюда видны на фото
            2. Рассчитай для {weight_grams} грамм:
               - Калории (ккал)
               - Белки (г)
               - Жиры (г) 
               - Углеводы (г)
            3. Укажи основные витамины и полезные вещества
            
            Отвечай на русском языке в следующем формате:
            
            **Продукты:** [список продуктов]
            
            **Пищевая ценность ({weight_grams} г):**
            • Калории: XXX ккал
            • Белки: XX г
            • Жиры: XX г
            • Углеводы: XX г
            
            **Витамины и полезные вещества:**
            [список витаминов и веществ]
            
            Будь максимально точным в расчетах, основываясь на визуальной оценке порции.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Ошибка при анализе еды через OpenAI: {e}")
            return f"Произошла ошибка при анализе изображения: {str(e)}"
