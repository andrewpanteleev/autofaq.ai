import pytest
import httpx
import allure
import json

BASE_URL = "https://chat.autofaq.ai"
USERS_URL = f"{BASE_URL}/api/webhooks/widget/6c24eb52-b1ab-4d78-8463-8556d4ee04b3/users"

@pytest.mark.asyncio
@allure.title("TC01 - Backend: GET /users возвращает корректные данные (High Priority)")
@allure.severity(allure.severity_level.BLOCKER)
async def test_get_users_valid():
    async with httpx.AsyncClient() as client:
        with allure.step("Отправляем GET запрос к /users"):
            response = await client.get(USERS_URL)

        with allure.step("Проверяем статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        data = response.json()

        with allure.step("Логируем полный ответ API"):
            print("Полученный ответ:", json.dumps(data, indent=4, ensure_ascii=False))

        with allure.step("Проверяем, что ответ является словарем и содержит 'id'"):
            assert isinstance(data, dict), f"Ответ не является словарем. Получено: {data}"
            assert "id" in data, f"В ответе отсутствует ключ 'id'. Полученные данные: {data}"


@pytest.mark.asyncio
@allure.title("TC02 - Backend: GET /users с неверным HTTP методом (High Priority)")
@allure.severity(allure.severity_level.BLOCKER)
async def test_get_users_invalid_method():
    async with httpx.AsyncClient() as client:
        with allure.step("Отправляем POST запрос к /users"):
            response = await client.post(USERS_URL, json={})
        with allure.step("Проверяем, что статус код указывает на ошибку"):
            assert response.status_code in (400, 405, 404), f"Ожидался статус 400, 405 или 404, получен {response.status_code}"


@pytest.mark.asyncio
@allure.title("TC03 - Падающий тест Backend (демонстрация Allure)")
@allure.severity(allure.severity_level.BLOCKER)
async def test_get_users_intentional_fail():
    async with httpx.AsyncClient() as client:
        with allure.step("Отправляем GET запрос к /users"):
            response = await client.get(USERS_URL)
        assert response.status_code == 500, f"Тест намеренно падается, т.к. код != 500 (пришёл {response.status_code})"

