import pytest
import allure
import os
import asyncio
from playwright.async_api import async_playwright


@pytest.fixture(scope="function")
async def page(request):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--disable-gpu"])
        video_dir = "/tmp/videos"
        os.makedirs(video_dir, exist_ok=True)
        context = await browser.new_context(
            record_video_dir=video_dir,
            record_video_size={"width": 1280, "height": 720}
        )
        page = await context.new_page()
        yield page

        video_obj = page.video
        video_path = await video_obj.path() if video_obj else None
        setattr(request.node, "video_path", video_path)
        await context.close()
        await browser.close()


@pytest.fixture(scope="function", autouse=True)
def attach_failed_video(request):
    yield
    video_path = getattr(request.node, "video_path", None)
    if request.node.rep_call.failed and video_path and os.path.exists(video_path):
        with open(video_path, "rb") as f:
            allure.attach(f.read(), name="Test Video", attachment_type=allure.attachment_type.WEBM)


def attach_failed_screenshot(page, test_name):
    loop = asyncio.get_event_loop()
    screenshot_path = f"allure-results/{test_name}.png"
    loop.run_until_complete(page.screenshot(path=screenshot_path))
    with open(screenshot_path, "rb") as img_file:
        allure.attach(img_file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "rep_" + report.when, report)

    if report.when == "call" and report.failed:
        page_obj = item.funcargs.get("page")
        if page_obj:
            attach_failed_screenshot(page_obj, item.name)

