from playwright.async_api import Page

class WidgetPage:
    def __init__(self, page: Page):
        self.page = page
        self.widget_button = page.locator("#chat21-launcher-button")
        self.widget_conversation = page.locator("#chat21-conversations")
        self.message_input = page.locator("#chat21-main-message-context")
        self.message_button_send = page.locator("#chat21-button-send")
        self.name_input = page.locator("#user-form_field_senderFullName")
        self.email_input = page.locator("#user-form_field_senderEmail")
        self.submit_button = page.locator("#chat21-message_userForm > div > div.form_panel > div.form_panel_actions > button")
        self.error_field = page.locator("#chat21-message_userForm > div > div.form_panel > div.form_panel_field.form_panel_field--error > div")
        self.success_message = page.locator("#chat21-sheet-content")
        self.messages = page.locator(".msg_block")


    async def goto(self, url: str):
        await self.page.goto(url)

    async def is_button_widget_visible(self) -> bool:
        return await self.widget_button.is_visible()

    async def click_widget_button(self):
        await self.widget_button.click()

    async def is_widget_visible(self) -> bool:
        return await self.widget_conversation.is_visible()

    async def fill_message(self, msg: str):
        await self.message_input.fill(msg)

    async def is_button_message_send_visible(self) -> bool:
        return await self.message_button_send.is_visible()

    async def is_button_message_send_disabled(self) -> bool:
        data_disabled = await self.message_button_send.get_attribute("data-disabled")
        return data_disabled == "true"

    async def click_message_button_send(self):
        await self.message_button_send.click()

    async def wait_for_message(self, text: str, timeout: int = 10000):
        await self.page.wait_for_selector(f".msg_block:has-text('{text}')", timeout=timeout)

    async def get_last_message_content(self) -> str:
        last_message_locator = self.messages.locator(".msg_content").last
        return await last_message_locator.text_content()

    async def fill_name(self, name: str):
        await self.name_input.fill(name)

    async def fill_email(self, email: str):
        await self.email_input.fill(email)

    async def click_submit(self):
        await self.submit_button.click()

    async def get_error_field_text(self) -> str:
        if await self.error_field.is_visible():
            return await self.error_field.inner_text()
        return ""

    async def get_success_text(self) -> str:
        if await self.success_message.is_visible():
            return await self.success_message.inner_text()
        return ""