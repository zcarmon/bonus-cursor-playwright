import json
from pathlib import Path
from typing import Callable

import pytest
from playwright.sync_api import Page

BASE_URL = "https://www.saucedemo.com/"
PASSWORD = "secret_sauce"


def load_accepted_users() -> list[str]:
    data_path = Path(__file__).parent / "test_data" / "accepted_users.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    return data["accepted_users"]


@pytest.fixture
def sauce_base_url() -> str:
    return BASE_URL


@pytest.fixture
def password() -> str:
    return PASSWORD


@pytest.fixture
def accepted_users() -> list[str]:
    return load_accepted_users()


@pytest.fixture
def login(page: Page, sauce_base_url: str) -> Callable[[str, str], None]:
    def _login(username: str, password: str) -> None:
        page.goto(sauce_base_url)
        page.get_by_placeholder("Username").fill(username)
        page.get_by_placeholder("Password").fill(password)
        page.get_by_role("button", name="Login").click()

    return _login
