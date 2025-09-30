export const useCurrency = () => {
  const { locale } = useI18n()
  
  // Расширенная карта валют для разных стран
  const currencyMap = {
    'ru': { symbol: '₽', code: 'RUB', name: 'Рубль' },
    'en': { symbol: '$', code: 'USD', name: 'Dollar' }
  }
  
  // Карта валют по странам
  const countryCurrencyMap = {
    'US': { symbol: '$', code: 'USD', name: 'US Dollar' },
    'CA': { symbol: 'C$', code: 'CAD', name: 'Canadian Dollar' },
    'GB': { symbol: '£', code: 'GBP', name: 'British Pound' },
    'DE': { symbol: '€', code: 'EUR', name: 'Euro' },
    'FR': { symbol: '€', code: 'EUR', name: 'Euro' },
    'IT': { symbol: '€', code: 'EUR', name: 'Euro' },
    'ES': { symbol: '€', code: 'EUR', name: 'Euro' },
    'NL': { symbol: '€', code: 'EUR', name: 'Euro' },
    'AU': { symbol: 'A$', code: 'AUD', name: 'Australian Dollar' },
    'JP': { symbol: '¥', code: 'JPY', name: 'Japanese Yen' },
    'CN': { symbol: '¥', code: 'CNY', name: 'Chinese Yuan' },
    'IN': { symbol: '₹', code: 'INR', name: 'Indian Rupee' },
    'BR': { symbol: 'R$', code: 'BRL', name: 'Brazilian Real' },
    'MX': { symbol: '$', code: 'MXN', name: 'Mexican Peso' },
    'KR': { symbol: '₩', code: 'KRW', name: 'South Korean Won' },
    'SG': { symbol: 'S$', code: 'SGD', name: 'Singapore Dollar' },
    'CH': { symbol: 'CHF', code: 'CHF', name: 'Swiss Franc' },
    'SE': { symbol: 'kr', code: 'SEK', name: 'Swedish Krona' },
    'NO': { symbol: 'kr', code: 'NOK', name: 'Norwegian Krone' },
    'DK': { symbol: 'kr', code: 'DKK', name: 'Danish Krone' },
    'PL': { symbol: 'zł', code: 'PLN', name: 'Polish Zloty' },
    'CZ': { symbol: 'Kč', code: 'CZK', name: 'Czech Koruna' },
    'HU': { symbol: 'Ft', code: 'HUF', name: 'Hungarian Forint' },
    'RO': { symbol: 'lei', code: 'RON', name: 'Romanian Leu' },
    'BG': { symbol: 'лв', code: 'BGN', name: 'Bulgarian Lev' },
    'HR': { symbol: 'kn', code: 'HRK', name: 'Croatian Kuna' },
    'RS': { symbol: 'дин', code: 'RSD', name: 'Serbian Dinar' },
    'UA': { symbol: '₴', code: 'UAH', name: 'Ukrainian Hryvnia' },
    'BY': { symbol: 'Br', code: 'BYN', name: 'Belarusian Ruble' },
    'KZ': { symbol: '₸', code: 'KZT', name: 'Kazakhstani Tenge' },
    'UZ': { symbol: 'сўм', code: 'UZS', name: 'Uzbekistani Som' },
    'KG': { symbol: 'сом', code: 'KGS', name: 'Kyrgyzstani Som' },
    'TJ': { symbol: 'SM', code: 'TJS', name: 'Tajikistani Somoni' },
    'TM': { symbol: 'T', code: 'TMT', name: 'Turkmenistani Manat' },
    'AZ': { symbol: '₼', code: 'AZN', name: 'Azerbaijani Manat' },
    'AM': { symbol: '֏', code: 'AMD', name: 'Armenian Dram' },
    'GE': { symbol: '₾', code: 'GEL', name: 'Georgian Lari' },
    'TR': { symbol: '₺', code: 'TRY', name: 'Turkish Lira' },
    'IL': { symbol: '₪', code: 'ILS', name: 'Israeli Shekel' },
    'AE': { symbol: 'د.إ', code: 'AED', name: 'UAE Dirham' },
    'SA': { symbol: 'ر.س', code: 'SAR', name: 'Saudi Riyal' },
    'EG': { symbol: '£', code: 'EGP', name: 'Egyptian Pound' },
    'ZA': { symbol: 'R', code: 'ZAR', name: 'South African Rand' },
    'NG': { symbol: '₦', code: 'NGN', name: 'Nigerian Naira' },
    'KE': { symbol: 'KSh', code: 'KES', name: 'Kenyan Shilling' },
    'GH': { symbol: '₵', code: 'GHS', name: 'Ghanaian Cedi' },
    'MA': { symbol: 'د.م.', code: 'MAD', name: 'Moroccan Dirham' },
    'TN': { symbol: 'د.ت', code: 'TND', name: 'Tunisian Dinar' },
    'DZ': { symbol: 'د.ج', code: 'DZD', name: 'Algerian Dinar' },
    'LY': { symbol: 'ل.د', code: 'LYD', name: 'Libyan Dinar' },
    'SD': { symbol: 'ج.س.', code: 'SDG', name: 'Sudanese Pound' },
    'ET': { symbol: 'Br', code: 'ETB', name: 'Ethiopian Birr' },
    'UG': { symbol: 'USh', code: 'UGX', name: 'Ugandan Shilling' },
    'TZ': { symbol: 'TSh', code: 'TZS', name: 'Tanzanian Shilling' },
    'RW': { symbol: 'RF', code: 'RWF', name: 'Rwandan Franc' },
    'BI': { symbol: 'FBu', code: 'BIF', name: 'Burundian Franc' },
    'DJ': { symbol: 'Fdj', code: 'DJF', name: 'Djiboutian Franc' },
    'SO': { symbol: 'S', code: 'SOS', name: 'Somali Shilling' },
    'ER': { symbol: 'Nfk', code: 'ERN', name: 'Eritrean Nakfa' },
    'SS': { symbol: '£', code: 'SSP', name: 'South Sudanese Pound' },
    'CF': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'TD': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'CM': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'CG': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'GA': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'GQ': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'ST': { symbol: 'Db', code: 'STN', name: 'São Tomé and Príncipe Dobra' },
    'AO': { symbol: 'Kz', code: 'AOA', name: 'Angolan Kwanza' },
    'MZ': { symbol: 'MT', code: 'MZN', name: 'Mozambican Metical' },
    'ZW': { symbol: 'Z$', code: 'ZWL', name: 'Zimbabwean Dollar' },
    'BW': { symbol: 'P', code: 'BWP', name: 'Botswana Pula' },
    'NA': { symbol: 'N$', code: 'NAD', name: 'Namibian Dollar' },
    'SZ': { symbol: 'L', code: 'SZL', name: 'Swazi Lilangeni' },
    'LS': { symbol: 'L', code: 'LSL', name: 'Lesotho Loti' },
    'MW': { symbol: 'MK', code: 'MWK', name: 'Malawian Kwacha' },
    'ZM': { symbol: 'ZK', code: 'ZMW', name: 'Zambian Kwacha' },
    'MG': { symbol: 'Ar', code: 'MGA', name: 'Malagasy Ariary' },
    'MU': { symbol: '₨', code: 'MUR', name: 'Mauritian Rupee' },
    'SC': { symbol: '₨', code: 'SCR', name: 'Seychellois Rupee' },
    'KM': { symbol: 'CF', code: 'KMF', name: 'Comorian Franc' },
    'YT': { symbol: '€', code: 'EUR', name: 'Euro' },
    'RE': { symbol: '€', code: 'EUR', name: 'Euro' },
    'CV': { symbol: '$', code: 'CVE', name: 'Cape Verdean Escudo' },
    'GW': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'GN': { symbol: 'FG', code: 'GNF', name: 'Guinean Franc' },
    'SL': { symbol: 'Le', code: 'SLE', name: 'Sierra Leonean Leone' },
    'LR': { symbol: 'L$', code: 'LRD', name: 'Liberian Dollar' },
    'CI': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'BF': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'ML': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'NE': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'SN': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'GM': { symbol: 'D', code: 'GMD', name: 'Gambian Dalasi' },
    'GN': { symbol: 'FG', code: 'GNF', name: 'Guinean Franc' },
    'MR': { symbol: 'UM', code: 'MRU', name: 'Mauritanian Ouguiya' },
    'ML': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'NE': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'BF': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'CI': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'SN': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'GM': { symbol: 'D', code: 'GMD', name: 'Gambian Dalasi' },
    'LR': { symbol: 'L$', code: 'LRD', name: 'Liberian Dollar' },
    'SL': { symbol: 'Le', code: 'SLE', name: 'Sierra Leonean Leone' },
    'GW': { symbol: 'CFA', code: 'XOF', name: 'West African CFA Franc' },
    'CV': { symbol: '$', code: 'CVE', name: 'Cape Verdean Escudo' },
    'RE': { symbol: '€', code: 'EUR', name: 'Euro' },
    'YT': { symbol: '€', code: 'EUR', name: 'Euro' },
    'KM': { symbol: 'CF', code: 'KMF', name: 'Comorian Franc' },
    'SC': { symbol: '₨', code: 'SCR', name: 'Seychellois Rupee' },
    'MU': { symbol: '₨', code: 'MUR', name: 'Mauritian Rupee' },
    'MG': { symbol: 'Ar', code: 'MGA', name: 'Malagasy Ariary' },
    'ZM': { symbol: 'ZK', code: 'ZMW', name: 'Zambian Kwacha' },
    'MW': { symbol: 'MK', code: 'MWK', name: 'Malawian Kwacha' },
    'LS': { symbol: 'L', code: 'LSL', name: 'Lesotho Loti' },
    'SZ': { symbol: 'L', code: 'SZL', name: 'Swazi Lilangeni' },
    'NA': { symbol: 'N$', code: 'NAD', name: 'Namibian Dollar' },
    'BW': { symbol: 'P', code: 'BWP', name: 'Botswana Pula' },
    'ZW': { symbol: 'Z$', code: 'ZWL', name: 'Zimbabwean Dollar' },
    'MZ': { symbol: 'MT', code: 'MZN', name: 'Mozambican Metical' },
    'AO': { symbol: 'Kz', code: 'AOA', name: 'Angolan Kwanza' },
    'ST': { symbol: 'Db', code: 'STN', name: 'São Tomé and Príncipe Dobra' },
    'GQ': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'GA': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'CG': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'CM': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'TD': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'CF': { symbol: 'FCFA', code: 'XAF', name: 'Central African CFA Franc' },
    'SS': { symbol: '£', code: 'SSP', name: 'South Sudanese Pound' },
    'ER': { symbol: 'Nfk', code: 'ERN', name: 'Eritrean Nakfa' },
    'SO': { symbol: 'S', code: 'SOS', name: 'Somali Shilling' },
    'DJ': { symbol: 'Fdj', code: 'DJF', name: 'Djiboutian Franc' },
    'BI': { symbol: 'FBu', code: 'BIF', name: 'Burundian Franc' },
    'RW': { symbol: 'RF', code: 'RWF', name: 'Rwandan Franc' },
    'TZ': { symbol: 'TSh', code: 'TZS', name: 'Tanzanian Shilling' },
    'UG': { symbol: 'USh', code: 'UGX', name: 'Ugandan Shilling' },
    'ET': { symbol: 'Br', code: 'ETB', name: 'Ethiopian Birr' },
    'SD': { symbol: 'ج.س.', code: 'SDG', name: 'Sudanese Pound' },
    'LY': { symbol: 'ل.د', code: 'LYD', name: 'Libyan Dinar' },
    'DZ': { symbol: 'د.ج', code: 'DZD', name: 'Algerian Dinar' },
    'TN': { symbol: 'د.ت', code: 'TND', name: 'Tunisian Dinar' },
    'MA': { symbol: 'د.م.', code: 'MAD', name: 'Moroccan Dirham' },
    'GH': { symbol: '₵', code: 'GHS', name: 'Ghanaian Cedi' },
    'KE': { symbol: 'KSh', code: 'KES', name: 'Kenyan Shilling' },
    'NG': { symbol: '₦', code: 'NGN', name: 'Nigerian Naira' },
    'ZA': { symbol: 'R', code: 'ZAR', name: 'South African Rand' },
    'EG': { symbol: '£', code: 'EGP', name: 'Egyptian Pound' },
    'SA': { symbol: 'ر.س', code: 'SAR', name: 'Saudi Riyal' },
    'AE': { symbol: 'د.إ', code: 'AED', name: 'UAE Dirham' },
    'IL': { symbol: '₪', code: 'ILS', name: 'Israeli Shekel' },
    'TR': { symbol: '₺', code: 'TRY', name: 'Turkish Lira' },
    'GE': { symbol: '₾', code: 'GEL', name: 'Georgian Lari' },
    'AM': { symbol: '֏', code: 'AMD', name: 'Armenian Dram' },
    'AZ': { symbol: '₼', code: 'AZN', name: 'Azerbaijani Manat' },
    'TM': { symbol: 'T', code: 'TMT', name: 'Turkmenistani Manat' },
    'TJ': { symbol: 'SM', code: 'TJS', name: 'Tajikistani Somoni' },
    'KG': { symbol: 'сом', code: 'KGS', name: 'Kyrgyzstani Som' },
    'UZ': { symbol: 'сўм', code: 'UZS', name: 'Uzbekistani Som' },
    'KZ': { symbol: '₸', code: 'KZT', name: 'Kazakhstani Tenge' },
    'BY': { symbol: 'Br', code: 'BYN', name: 'Belarusian Ruble' },
    'UA': { symbol: '₴', code: 'UAH', name: 'Ukrainian Hryvnia' },
    'RS': { symbol: 'дин', code: 'RSD', name: 'Serbian Dinar' },
    'HR': { symbol: 'kn', code: 'HRK', name: 'Croatian Kuna' },
    'BG': { symbol: 'лв', code: 'BGN', name: 'Bulgarian Lev' },
    'RO': { symbol: 'lei', code: 'RON', name: 'Romanian Leu' },
    'HU': { symbol: 'Ft', code: 'HUF', name: 'Hungarian Forint' },
    'CZ': { symbol: 'Kč', code: 'CZK', name: 'Czech Koruna' },
    'PL': { symbol: 'zł', code: 'PLN', name: 'Polish Zloty' },
    'DK': { symbol: 'kr', code: 'DKK', name: 'Danish Krone' },
    'NO': { symbol: 'kr', code: 'NOK', name: 'Norwegian Krone' },
    'SE': { symbol: 'kr', code: 'SEK', name: 'Swedish Krona' },
    'CH': { symbol: 'CHF', code: 'CHF', name: 'Swiss Franc' },
    'SG': { symbol: 'S$', code: 'SGD', name: 'Singapore Dollar' },
    'KR': { symbol: '₩', code: 'KRW', name: 'South Korean Won' },
    'MX': { symbol: '$', code: 'MXN', name: 'Mexican Peso' },
    'BR': { symbol: 'R$', code: 'BRL', name: 'Brazilian Real' },
    'IN': { symbol: '₹', code: 'INR', name: 'Indian Rupee' },
    'CN': { symbol: '¥', code: 'CNY', name: 'Chinese Yuan' },
    'JP': { symbol: '¥', code: 'JPY', name: 'Japanese Yen' },
    'AU': { symbol: 'A$', code: 'AUD', name: 'Australian Dollar' },
    'NL': { symbol: '€', code: 'EUR', name: 'Euro' },
    'ES': { symbol: '€', code: 'EUR', name: 'Euro' },
    'IT': { symbol: '€', code: 'EUR', name: 'Euro' },
    'FR': { symbol: '€', code: 'EUR', name: 'Euro' },
    'DE': { symbol: '€', code: 'EUR', name: 'Euro' },
    'GB': { symbol: '£', code: 'GBP', name: 'British Pound' },
    'CA': { symbol: 'C$', code: 'CAD', name: 'Canadian Dollar' },
    'US': { symbol: '$', code: 'USD', name: 'US Dollar' }
  }
  
  // Состояние для хранения определенной валюты
  const detectedCurrency = ref(null)
  const isDetecting = ref(false)
  
  // Функция для определения валюты по IP
  const detectCurrencyByIP = async () => {
    if (isDetecting.value) return
    
    isDetecting.value = true
    
    try {
      // Используем бесплатный API для определения страны по IP
      const response = await fetch('https://ipapi.co/json/')
      const data = await response.json()
      
      console.log('IP API response:', data)
      if (data.country_code && countryCurrencyMap[data.country_code]) {
        detectedCurrency.value = countryCurrencyMap[data.country_code]
        console.log('Detected currency for country', data.country_code, ':', detectedCurrency.value)
      } else {
        // Fallback на USD если страна не найдена
        detectedCurrency.value = { symbol: '$', code: 'USD', name: 'US Dollar' }
        console.log('Country not found, using USD fallback')
      }
    } catch (error) {
      console.error('Error detecting currency:', error)
      // Fallback на USD при ошибке
      detectedCurrency.value = { symbol: '$', code: 'USD', name: 'US Dollar' }
    } finally {
      isDetecting.value = false
    }
  }
  
  // Определяем валюту при инициализации
  onMounted(() => {
    detectCurrencyByIP()
  })
  
  const currentCurrency = computed(() => {
    // Если валюта уже определена по геолокации, используем её
    if (detectedCurrency.value) {
      console.log('Using detected currency:', detectedCurrency.value)
      return detectedCurrency.value
    }
    
    // Fallback на валюту по языку если геолокация не определена
    const fallbackCurrency = locale.value === 'ru' ? currencyMap['ru'] : currencyMap['en']
    console.log('Using fallback currency for locale', locale.value, ':', fallbackCurrency)
    return fallbackCurrency
  })
  
  const formatPrice = (price: number) => {
    const currency = currentCurrency.value
    return `${price}${currency.symbol}`
  }
  
  const getPriceForLocale = (ruPrice: number, enPrice: number) => {
    return locale.value === 'en' ? enPrice : ruPrice
  }
  
  return {
    currentCurrency,
    formatPrice,
    getPriceForLocale,
    detectedCurrency,
    isDetecting,
    detectCurrencyByIP
  }
}
