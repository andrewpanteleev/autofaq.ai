import pytest
import allure
from pages.widget_page import WidgetPage


@pytest.fixture
async def widget_page(page):
    widget = WidgetPage(page)
    await widget.goto("https://autofaq.ai")
    return widget


@pytest.mark.asyncio
@allure.title("TC01 - Отображение кнопки виджета")
@allure.severity(allure.severity_level.BLOCKER)
async def test_widget_button_visibility(widget_page):
    assert await widget_page.is_button_widget_visible(), "Кнопка виджета не отображается"


@pytest.mark.asyncio
@allure.title("TC02 - Отображение виджета")
@allure.severity(allure.severity_level.BLOCKER)
async def test_widget_visibility(widget_page):
    await widget_page.widget_button.click()
    assert await widget_page.is_widget_visible(), "Виджет не отображается"


@pytest.mark.asyncio
@allure.title("TC03 - Отправка сообщения без предоставления данных")
@allure.severity(allure.severity_level.BLOCKER)
async def test_send_message(widget_page):
    await widget_page.widget_button.click()
    assert await widget_page.is_button_message_send_disabled(), "Кнопка для отправки сообщения доступна для нажатия"
    await widget_page.fill_message("привет")
    await widget_page.message_button_send.click()
    await widget_page.wait_for_message("Привет!")
    message_content = await widget_page.get_last_message_content()
    assert message_content == "Привет!"


@pytest.mark.asyncio
@allure.title("TC04 - Успешная отправка валидных данных, сообщения и получение ответа")
@allure.severity(allure.severity_level.BLOCKER)
async def test_valid_submission(widget_page):
    await widget_page.widget_button.click()
    assert await widget_page.is_button_message_send_disabled(), "Кнопка для отправки сообщения доступна для нажатия"
    await widget_page.fill_name("Test_user")
    await widget_page.fill_email("test@example.com")
    await widget_page.click_submit()

    success_text = await widget_page.get_success_text()
    assert "напишите свой вопрос и я постараюсь вам помочь" in success_text.lower() or success_text != "", \
        "Не отобразилось сообщение о том, что можно задать свой вопрос"

    await widget_page.fill_message("привет")
    await widget_page.message_button_send.click()
    await widget_page.wait_for_message("Привет!")
    message_content = await widget_page.get_last_message_content()
    assert message_content == "Привет!"


@pytest.mark.asyncio
@allure.title("TC05 - Валидация пустого Email")
@allure.severity(allure.severity_level.CRITICAL)
async def test_empty_email(widget_page):
    await widget_page.widget_button.click()
    await widget_page.fill_name("Test_user")
    await widget_page.fill_email("")
    await widget_page.click_submit()

    error_text = await widget_page.get_error_field_text()
    assert "требуется указать почту." in error_text.lower(), f"Ожидали ошибку о пустом email, получили: {error_text}"


@pytest.mark.asyncio
@allure.title("TC06 - Валидация некорректного Email")
@allure.severity(allure.severity_level.CRITICAL)
async def test_invalid_email(widget_page):
    await widget_page.widget_button.click()
    await widget_page.fill_name("Test_user")
    await widget_page.fill_email("invalid-email")
    await widget_page.click_submit()

    error_text = await widget_page.get_error_field_text()
    assert "почта имеет неверный формат." in error_text.lower(), f"Ожидали ошибку о неверном формате email, получили: {error_text}"


@pytest.mark.asyncio
@allure.title("TC07 - Адаптивность на мобильном разрешении")
@allure.severity(allure.severity_level.NORMAL)
async def test_mobile_viewport(page):
    await page.set_viewport_size({"width": 375, "height": 812})
    widget = WidgetPage(page)
    await widget.goto("https://autofaq.ai")
    assert await widget.is_button_widget_visible(), "Кнопка виджета не видна на мобильном разрешении"
    await widget.widget_button.click()
    assert await widget.is_widget_visible(), "Виджет не виден на мобильном разрешении"


@pytest.mark.asyncio
@allure.title("TC08 - Падающий тест (демонстрация Allure)")
@allure.severity(allure.severity_level.NORMAL)
async def test_intentional_fail(widget_page):
    await widget_page.widget_button.click()
    actual_button_text = await widget_page.submit_button.inner_text()
    expected_text = "Не Отправить"
    assert actual_button_text == expected_text, \
        f"Специально падаем: {actual_button_text} != {expected_text}"

