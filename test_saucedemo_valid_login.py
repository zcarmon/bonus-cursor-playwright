import pytest
from playwright.sync_api import Page, expect

from conftest import load_accepted_users

@pytest.mark.parametrize("username", load_accepted_users())
def test_accepted_users_can_login(
    username: str,
    login,
    password: str,
    page: Page,
    sauce_base_url: str,
) -> None:
    login(username, password)

    expect(page).to_have_url(f"{sauce_base_url}inventory.html")
    expect(page.locator(".app_logo")).to_be_visible()
