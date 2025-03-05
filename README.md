# Тестирование виджета чата (AutoFAQ.ai)

## 1. Тест-кейсы

Ниже приведён список тест-кейсов для проверки виджета чата на странице [https://autofaq.ai](https://autofaq.ai).

### Обозначения

- **Приоритет**: High (высокий), Medium (средний), Low (низкий).
- **Категория**:
  - **F** (Functional) — функциональное тестирование
  - **UI** (User Interface) — проверка интерфейса
  - **C** (Compatibility) — проверка совместимости, адаптивности и т. п.


| **ID**   | **Название**                                                            | **Категория** | **Приоритет** | **Шаги**                                                                                                                                                                                                                                                           | **Ожидаемый результат**                                                                                                                          |
| -------- | ------------------------------------------------------------------------------- | ---------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **TC01** | Отображение виджета                                           | UI                     | High                   | 1. Открыть[https://autofaq.ai](https://autofaq.ai) <br> 2. Убедиться, что на странице виден чат-виджет (поле «Ваше имя», «Email», кнопка «Отправить»)                                       | Виджет чата присутствует на странице, кнопка «Отправить» кликабельна                                   |
| **TC02** | Валидация пустого имени                                    | F                      | High                   | 1. Открыть страницу<br> 2. Оставить поле «Ваше имя» пустым <br> 3. Заполнить корректный Email <br> 4. Нажать «Отправить»                                                                 | Появляется сообщение об ошибке (отсутствие имени)                                                                        |
| **TC03** | Валидация некорректного Email                             | F                      | High                   | 1. Заполнить поле «Ваше имя» валидными данными<br> 2. Ввести некорректный Email (без `@` и т. п.) <br> 3. Нажать «Отправить»                                                            | Появляется сообщение об ошибке (email неверный)                                                                                 |
| **TC04** | Успешная отправка валидных данных                 | F                      | High                   | 1. Заполнить поле «Ваше имя» корректно<br> 2. Заполнить корректный Email <br> 3. Нажать «Отправить»                                                                                                 | Нет ошибки, виджет переходит к следующему шагу / выводит сообщение об успешной отправке   |
| **TC05** | Адаптивность (мобильное разрешение)              | UI, C                  | Medium                 | 1. Открыть страницу в режиме эмуляции мобильного экрана (или задать viewport)<br> 2. Проверить корректность отображения виджета (размер, расположение) | Виджет не обрезается, элементы доступны для нажатия, сохраняется функциональность           |
| **TC06** | Backend: успешный POST-запрос                                     | F                      | High                   | 1. Отправить`POST` на `https://autofaq.ai/api/submit` с JSON телом: `{"name":"Test","email":"test@example.com"}`                                                                                                                                      | Ответ`200 OK`, в теле ответа статус «ok» (или иной признак успеха)                                                     |
| **TC07** | Backend: ошибка при некорректном email                     | F                      | High                   | 1. Отправить`POST` на `https://autofaq.ai/api/submit` с JSON телом: `{"name":"Test","email":"invalid-email"}`                                                                                                                                         | Ответ`400 Bad Request`, в теле ответа присутствует описание ошибки                                                       |
| **TC08** | Безопасность: проверка спецсимволов (XSS)       | F                      | Medium                 | 1. Ввести в поле «Ваше имя» строку с потенциально опасными символами, например`<script>alert(1)</script>` <br> 2. Нажать «Отправить»                                                  | Сервер корректно валидирует / экранирует спецсимволы, XSS-уязвимость не воспроизводится   |
| **TC09** | Падающий тест (для проверки Allure-отчётности) | -                      | -                      | Нет конкретных шагов (искусственный тест, «ломается» специально)                                                                                                                                                | Тест намеренно проваливается, чтобы в Allure отображались скриншоты и видео упавших тестов |

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
