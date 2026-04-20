import re

from playwright.sync_api import Page, expect

USERNAME = "standard_user"


# Convert a price label like "$29.99" into a float value.
def _price_to_float(price_text: str) -> float:
    match = re.search(r"\$([0-9]+(?:\.[0-9]{2})?)", price_text)
    if not match:
        raise ValueError(f"Could not parse price from text: {price_text}")
    return float(match.group(1))


# Log in, add the 4 highest-priced items, and verify cart total matches.
def test_standard_user_adds_top_4_expensive_items_and_calculates_total(
    login,
    password: str,
    page: Page,
    sauce_base_url: str,
) -> None:
    login(USERNAME, password)

    expect(page).to_have_url(f"{sauce_base_url}inventory.html")

    inventory_items = page.locator(".inventory_item")
    item_count = inventory_items.count()
    assert item_count >= 4, "Expected at least 4 inventory items"

    # Build a sortable list of item prices and their corresponding "Add to cart" buttons.
    items_by_price: list[tuple[float, str]] = []
    for i in range(item_count):
        item = inventory_items.nth(i)
        price = _price_to_float(item.locator(".inventory_item_price").inner_text())
        add_button = item.get_by_role("button", name="Add to cart")
        button_id = add_button.get_attribute("id")
        assert button_id is not None
        items_by_price.append((price, button_id))

    top_4 = sorted(items_by_price, key=lambda pair: pair[0], reverse=True)[:4]
    expected_total = sum(price for price, _ in top_4)

    for _, button_id in top_4:
        page.locator(f'[id="{button_id}"]').click()
        page.wait_for_timeout(1100)

    expect(page.locator(".shopping_cart_badge")).to_have_text("4")

    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url(f"{sauce_base_url}cart.html")

    cart_prices = page.locator(".cart_item .inventory_item_price").all_inner_texts()
    cart_total = sum(_price_to_float(text) for text in cart_prices)

    assert len(cart_prices) == 4
    assert cart_total == expected_total

    page.wait_for_timeout(3000)
