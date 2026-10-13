import re
from playwright.sync_api import expect

def test_user_creates_car_in_browser(page, live_server):
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Toyota")
    page.get_by_label("Model", exact=True).fill("Yaris")
    page.get_by_label("Year", exact=True).fill("2020")
    page.get_by_label("Color", exact=False).fill("Blue")
    page.get_by_role("button", name="Create car").click()
    expect(page).to_have_url(re.compile(r"/cars/\d+$"))
    expect(page.locator("#car-title")).to_contain_text("Toyota Yaris")

def test_user_edits_car_and_change_survives_reload(page, live_server):
    # 1.新建车辆
    page.goto(f"{live_server}/cars/new")
    page.get_by_label("Make", exact=True).fill("Honda")
    page.get_by_label("Model", exact=True).fill("Civic")
    page.get_by_label("Year", exact=True).fill("2022")
    page.get_by_label("Color", exact=False).fill("Silver")
    page.get_by_role("button", name="Create car").click()
    # 2.点击Edit car链接
    page.get_by_role("link", name="Edit car").click()
    # 3.修改字段
    page.get_by_label("Model", exact=True).fill("Accord")
    page.get_by_label("Year", exact=True).fill("2023")
    page.get_by_role("button", name="Save changes").click()
    # 4.校验修改后页面
    expect(page.locator("#car-title")).to_contain_text("Honda Accord")
    # 5.页面刷新，确认修改持久化
    page.reload()
    expect(page.locator("#car-title")).to_contain_text("Honda Accord")
    expect(page.locator("#car-model")).to_have_text("Accord")
    expect(page.locator("#car-year")).to_have_text("2023")
