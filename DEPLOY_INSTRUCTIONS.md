# 🚀 Инструкция по деплою SEO исправлений

## Быстрый старт

### 1. Пересборка Nuxt сайта
```bash
cd /Users/kamil/PycharmProjects/calories_notebook/landing/
npm run generate
```

Это создаст статические файлы в директории `dist/`.

### 2. Копирование файлов на сервер
```bash
cd /Users/kamil/PycharmProjects/calories_notebook/
./deploy/deploy_landing.sh
```

Или вручную:
```bash
ssh german_server
cd /path/to/calories_notebook
git pull origin main
cd landing
npm run generate
# Перезапустить nginx/веб-сервер
```

### 3. Проверка после деплоя

#### Проверить canonical URL:
```bash
# Главная страница блога
curl -I https://calories.toxiguard.site/blog/ | grep -i canonical

# Статья 1
curl -I https://calories.toxiguard.site/blog/podschet-kaloriy-po-foto-telegram-bot/ | grep -i canonical

# Статья 2
curl -I https://calories.toxiguard.site/blog/avtomaticheskiy-dnevnik-pitaniya/ | grep -i canonical
```

Должны увидеть:
```
link: <https://calories.toxiguard.site/blog/>; rel="canonical"
link: <https://calories.toxiguard.site/blog/podschet-kaloriy-po-foto-telegram-bot>; rel="canonical"
```

#### Проверить sitemap.xml:
```bash
curl https://calories.toxiguard.site/sitemap.xml
```

Не должно быть якорных ссылок (#faq, #features, etc).

#### Проверить llms.txt:
```bash
curl https://calories.toxiguard.site/llms.txt
```

Должно быть описание проекта, а не `Disallow: /`.

### 4. Отправить в Google Search Console

1. Откройте [Google Search Console](https://search.google.com/search-console)
2. Выберите свойство `calories.toxiguard.site`
3. Перейдите в **Индексирование > Sitemap**
4. Повторно отправьте sitemap: `https://calories.toxiguard.site/sitemap.xml`
5. Перейдите в **Проверка URL**
6. Проверьте и запросите индексацию для:
   - `/blog/`
   - `/blog/podschet-kaloriy-po-foto-telegram-bot`
   - `/blog/avtomaticheskiy-dnevnik-pitaniya`
   - `/blog/ii-v-pitanii-kak-iskusstvennyy-intellekt-menyaet-zdorove`
   - `/blog/pochemu-vazhno-sledit-za-kaloriyami-nauka-zdorove-prakticheskie-vyvody`

### 5. Отправить в Яндекс.Вебмастер

1. Откройте [Яндекс.Вебмастер](https://webmaster.yandex.ru/)
2. Выберите сайт `calories.toxiguard.site`
3. Перейдите в **Индексирование > Файлы Sitemap**
4. Обновите sitemap
5. Проверьте индексацию URL

---

## Ожидаемые результаты

### Неделя 1-2:
- [ ] Canonical URL корректны на всех страницах
- [ ] Sitemap обновлен в Search Console
- [ ] Первые страницы начинают индексироваться

### Неделя 3-4:
- [ ] Все статьи блога проиндексированы
- [ ] Появляются первые показы в Search Console
- [ ] Рост запросов с 0 до 10-20

### Месяц 2-3:
- [ ] Позиции улучшились на 20-30 мест
- [ ] Трафик вырос на 100-200%
- [ ] Показы увеличились до 100-200 в день

---

## Troubleshooting

### Проблема: Canonical URL не обновляется
**Решение:**
1. Очистить кэш CDN (если используется)
2. Очистить кэш браузера
3. Проверить, что файлы обновились на сервере
4. Перезапустить nginx/веб-сервер

### Проблема: Статьи не индексируются
**Решение:**
1. Проверить robots.txt (должен разрешать /blog/)
2. Проверить canonical URL (должен быть самоссылочным)
3. Запросить переобход в Search Console
4. Подождать 1-2 недели

### Проблема: Keywords всё ещё слишком много
**Решение:**
1. Проверить, что изменения применились
2. Проверить все файлы Vue в `landing/pages/blog/`
3. Убедиться, что не осталось тега `keywords` с длинным списком

---

## Контакты для помощи

- **GitHub Issues:** [Создать issue](https://github.com/your-repo/issues)
- **Email:** support@calories.toxiguard.site
- **Telegram:** @caloriesnote_bot

---

**Последнее обновление:** 2 октября 2025



