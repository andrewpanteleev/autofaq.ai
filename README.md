# Тестирование виджета чата (AutoFAQ.ai)

## 1. Тест-кейсы

Ниже приведён список тест-кейсов для проверки виджета чата на странице [https://autofaq.ai](https://autofaq.ai).

## Backend тест-кейсы

### TC01 - Backend: GET /users возвращает корректные данные (High Priority)

**Приоритет:** Блокирующий**Шаги:**

1. Отправить GET-запрос к `/users`
2. Проверить, что статус-код 200
3. Проверить, что ответ является словарем и содержит ключ `id`

**Ожидаемый результат:**
Запрос успешно выполняется, возвращая JSON-ответ с корректными данными.

---

### TC02 - Backend: GET /users с неверным HTTP методом (High Priority)

**Приоритет:** Блокирующий**Шаги:**

1. Отправить POST-запрос к `/users`
2. Проверить, что статус-код 400, 405 или 404

**Ожидаемый результат:**
Сервер корректно обрабатывает неверный метод запроса, возвращая соответствующую ошибку.

---

### TC03 - Падающий тест Backend (демонстрация Allure)

**Приоритет:** Блокирующий**Шаги:**

1. Отправить GET-запрос к `/users`
2. Проверить, что статус-код 500

**Ожидаемый результат:**
Тест намеренно должен падать, так как ожидаемый статус 500.

---

## Frontend тест-кейсы

### TC01 - Отображение кнопки виджета

**Приоритет:** Блокирующий**Шаги:**

1. Открыть страницу
2. Проверить, что кнопка виджета видима

**Ожидаемый результат:**
Кнопка виджета отображается.

---

### TC02 - Отображение виджета

**Приоритет:** Блокирующий**Шаги:**

1. Кликнуть на кнопку виджета
2. Проверить, что виджет отображается

**Ожидаемый результат:**
Виджет становится видимым.

---

### TC03 - Отправка сообщения без предоставления данных

**Приоритет:** Блокирующий**Шаги:**

1. Кликнуть на кнопку виджета
2. Проверить, что кнопка отправки сообщения недоступна
3. Ввести "привет"
4. Отправить сообщение
5. Проверить, что ответ содержит "Привет!"

**Ожидаемый результат:**
Получен ожидаемый ответ "Привет!".

---

### TC04 - Успешная отправка валидных данных, сообщения и получение ответа

**Приоритет:** Блокирующий**Шаги:**

1. Кликнуть на кнопку виджета
2. Ввести имя и email
3. Подтвердить ввод
4. Проверить, что отображается приглашение задать вопрос
5. Ввести "привет"
6. Отправить сообщение
7. Проверить, что ответ содержит "Привет!"

**Ожидаемый результат:**
Форма успешно отправляется, а ответ содержит "Привет!".

---

### TC05 - Валидация пустого Email

**Приоритет:** Критический**Шаги:**

1. Кликнуть на кнопку виджета
2. Ввести имя, но оставить email пустым
3. Подтвердить ввод
4. Проверить сообщение об ошибке

**Ожидаемый результат:**
Ошибка: "Требуется указать почту."

---

### TC06 - Валидация некорректного Email

**Приоритет:** Критический**Шаги:**

1. Кликнуть на кнопку виджета
2. Ввести имя
3. Ввести email в неверном формате (например, `invalid-email`)
4. Подтвердить ввод
5. Проверить сообщение об ошибке

**Ожидаемый результат:**
Ошибка: "Почта имеет неверный формат."

---

### TC07 - Адаптивность на мобильном разрешении

**Приоритет:** Нормальный**Шаги:**

1. Установить разрешение экрана 375x812
2. Открыть страницу
3. Проверить, что кнопка виджета отображается
4. Кликнуть на кнопку виджета
5. Проверить, что виджет видим

**Ожидаемый результат:**
Виджет и кнопка корректно отображаются на мобильном разрешении.

---

### TC08 - Падающий тест (демонстрация Allure)

**Приоритет:** Нормальный**Шаги:**

1. Кликнуть на кнопку виджета
2. Проверить текст кнопки отправки (ожидается "Не Отправить")

**Ожидаемый результат:**
Тест намеренно падает, так как текст не совпадает.

---

**Примечание:**
Тесты используют `pytest`, `allure` и `httpx` для backend, а также Playwright для frontend.

## 2. Краткое описание автотестов

- **Frontend (Playwright)**:

  - Тесты на валидацию форм (пустое имя, некорректный Email, успешная отправка).
  - Проверка отображения виджета и адаптивности.
  - Падающий тест для демонстрации отчётов.
- **Backend (Pytest + httpx)**:

  - Проверка корректного ответа при валидных данных (200 OK).
  - Проверка ошибки при некорректном Email (400 Bad Request).
  - Падающий тест для демонстрации отчётов (проверка неверного статус-кода).

Все тесты написаны асинхронно (используя `pytest-asyncio`), упакованы в Docker, при запуске формируют Allure-отчёт с видео и скриншотами упавших тестов.

## 3. Запуск в Docker

1. Собрать образ:

   ```bash
   docker build -t autofaq-tests -f docker/Dockerfile .
   ```
2. Запустить контейнер (с сохранением результатов Allure):

   ```bash
   docker run --rm -it -v "%cd%\allure-results:/app/allure-results" autofaq-tests
   ```
3. Сгенерировать отчёт:

   ```bash
   allure generate allure-results -o allure-report --clean
   ```
4. Открыть отчёт:

   ```bash
   allure open allure-report
   ```
