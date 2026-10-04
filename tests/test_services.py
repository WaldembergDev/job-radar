from playwright.sync_api import Page, expect


def test_services_workana_titulo(page: Page):
    page.goto('https://www.workana.com/jobs?category=it-programming&language=pt')

    expect(page.locator('.project-item').first).to_be_visible()

    expect(page).to_have_url("https://www.workana.com/jobs?category=it-programming&language=pt")

    expect(page.locator('.project-body').first).to_be_visible()

    expect(page.locator('.bids').first).to_be_visible()
