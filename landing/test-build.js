#!/usr/bin/env node

// Скрипт для тестирования сборки лендинга
const { execSync } = require('child_process')
const fs = require('fs')
const path = require('path')

console.log('🧪 Тестируем сборку лендинга...')

try {
  // Проверяем наличие package.json
  if (!fs.existsSync('package.json')) {
    throw new Error('package.json не найден')
  }

  // Устанавливаем зависимости
  console.log('📦 Устанавливаем зависимости...')
  execSync('npm install', { stdio: 'inherit' })

  // Проверяем TypeScript
  console.log('🔍 Проверяем TypeScript...')
  execSync('npx tsc --noEmit', { stdio: 'inherit' })

  // Собираем проект
  console.log('🔨 Собираем проект...')
  execSync('npm run build', { stdio: 'inherit' })

  // Проверяем наличие .output
  if (!fs.existsSync('.output')) {
    throw new Error('Сборка не создала .output директорию')
  }

  // Проверяем основные файлы
  const requiredFiles = [
    '.output/server/index.mjs',
    '.output/public/index.html'
  ]

  for (const file of requiredFiles) {
    if (!fs.existsSync(file)) {
      throw new Error(`Отсутствует файл: ${file}`)
    }
  }

  console.log('✅ Сборка успешна!')
  console.log('📊 Размер сборки:')
  
  // Показываем размер сборки
  execSync('du -sh .output', { stdio: 'inherit' })

  console.log('🎉 Все тесты пройдены!')

} catch (error) {
  console.error('❌ Ошибка при тестировании:', error.message)
  process.exit(1)
}
