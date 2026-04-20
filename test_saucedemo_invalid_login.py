import pytest
from playwright.sync_api import Page, expect

@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("standard_user", "wrong_password"),
        ("unknown_user", "secret_sauce"),
        ("", "secret_sauce"),
        ("standard_user", ""),
        ("", ""),
    ],
)
def test_invalid_credentials_show_error(
    username: str,
    password: str,
    login,
    page: Page,
    sauce_base_url: str,
) -> None:
    login(username, password)

    error = page.locator("[data-test='error']")
    expect(error).to_be_visible()
    expect(page).to_have_url(sauce_base_url)
