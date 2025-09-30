#!/bin/bash

cd /Users/kamil/PycharmProjects/calories_notebook/landing

# Заменяем основные тексты в компонентах
find components/ -name "*.vue" -exec sed -i '' 's/ТЕКСТ/Правильный текст/g' {} \;

# Заменяем конкретные ключи
find components/ -name "*.vue" -exec sed -i '' 's/pricing\.title/Выберите свой тарифный план/g' {} \;
find components/ -name "*.vue" -exec sed -i '' 's/pricing\.subtitle/Начните с бесплатного Lite или получите все функции Pro/g' {} \;
find components/ -name "*.vue" -exec sed -i '' 's/cta\.title/Готов начать контролировать питание?/g' {} \;
find components/ -name "*.vue" -exec sed -i '' 's/cta\.subtitle/Запусти бота прямо сейчас и получи первый анализ за 5 секунд/g' {} \;
find components/ -name "*.vue" -exec sed -i '' 's/faq\.title/Часто задаваемые вопросы/g' {} \;

echo "Замена завершена"
