"""
Test Helper utilities for Playwright automation framework.

This module provides utility functions and helper methods for common test operations
including screenshots, element waits, clicks, fills, and other browser interactions.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Any

from playwright.sync_api import Page, Locator, expect


class TestHelper:
    """Helper class providing utility functions for test automation."""

    def __init__(self, page: Page, screenshots_dir: str = "screenshots"):
        """
        Initialize the TestHelper.

        Args:
            page: Playwright Page object
            screenshots_dir: Directory path for saving screenshots
        """
        self.page = page
        self.screenshots_dir = screenshots_dir
        self._ensure_screenshots_dir()

    def _ensure_screenshots_dir(self) -> None:
        """Create screenshots directory if it doesn't exist."""
        Path(self.screenshots_dir).mkdir(parents=True, exist_ok=True)

    def take_screenshot(self, name: Optional[str] = None, full_page: bool = False) -> str:
        """
        Capture a screenshot of the current page.

        Args:
            name: Name for the screenshot file (without extension)
            full_page: If True, captures the entire page, otherwise just viewport

        Returns:
            Path to the saved screenshot file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = name or f"screenshot_{timestamp}"
        filepath = os.path.join(self.screenshots_dir, f"{filename}.png")

        self.page.screenshot(path=filepath, full_page=full_page)
        return filepath

    def wait_for_element(
        self, selector: str, timeout: int = 30000, state: str = "visible"
    ) -> Locator:
        """
        Wait for an element to appear and reach a specific state.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
            state: State to wait for ("attached", "detached", "visible", "hidden")

        Returns:
            Locator object if element is found

        Raises:
            TimeoutError: If element is not found within timeout
        """
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def safe_click(
        self, selector: str, timeout: int = 30000, force: bool = False
    ) -> None:
        """
        Safely click an element with wait.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
            force: Force click even if element is not clickable
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.click(force=force)

    def safe_fill(
        self, selector: str, text: str, timeout: int = 30000, delay: int = 0
    ) -> None:
        """
        Safely fill an input field with text.

        Args:
            selector: CSS selector or XPath of the input element
            text: Text to fill in
            timeout: Timeout in milliseconds
            delay: Delay between keypresses in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.fill(text, delay=delay)

    def safe_type(
        self, selector: str, text: str, timeout: int = 30000, delay: int = 0
    ) -> None:
        """
        Safely type text into an element character by character.

        Args:
            selector: CSS selector or XPath of the input element
            text: Text to type
            timeout: Timeout in milliseconds
            delay: Delay between keypresses in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.type(text, delay=delay)

    def safe_select_option(
        self, selector: str, value: str, timeout: int = 30000
    ) -> None:
        """
        Safely select an option from a dropdown.

        Args:
            selector: CSS selector or XPath of the select element
            value: Value of the option to select
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.select_option(value)

    def get_text(self, selector: str, timeout: int = 30000) -> str:
        """
        Get text content of an element.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Returns:
            Text content of the element
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        return locator.text_content() or ""

    def get_attribute(
        self, selector: str, attribute: str, timeout: int = 30000
    ) -> Optional[str]:
        """
        Get attribute value of an element.

        Args:
            selector: CSS selector or XPath of the element
            attribute: Name of the attribute
            timeout: Timeout in milliseconds

        Returns:
            Attribute value or None if not found
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        return locator.get_attribute(attribute)

    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is visible.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Returns:
            True if element is visible, False otherwise
        """
        try:
            self.wait_for_element(selector, timeout=timeout, state="visible")
            return True
        except Exception:
            return False

    def is_element_present(self, selector: str, timeout: int = 5000) -> bool:
        """
        Check if an element is present in the DOM.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Returns:
            True if element is present, False otherwise
        """
        try:
            self.wait_for_element(selector, timeout=timeout, state="attached")
            return True
        except Exception:
            return False

    def count_elements(self, selector: str) -> int:
        """
        Count the number of elements matching a selector.

        Args:
            selector: CSS selector or XPath of the elements

        Returns:
            Number of elements found
        """
        return self.page.locator(selector).count()

    def check_checkbox(self, selector: str, timeout: int = 30000) -> None:
        """
        Check a checkbox element.

        Args:
            selector: CSS selector or XPath of the checkbox
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        if not locator.is_checked():
            locator.check()

    def uncheck_checkbox(self, selector: str, timeout: int = 30000) -> None:
        """
        Uncheck a checkbox element.

        Args:
            selector: CSS selector or XPath of the checkbox
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        if locator.is_checked():
            locator.uncheck()

    def is_checkbox_checked(self, selector: str, timeout: int = 30000) -> bool:
        """
        Check if a checkbox is checked.

        Args:
            selector: CSS selector or XPath of the checkbox
            timeout: Timeout in milliseconds

        Returns:
            True if checkbox is checked, False otherwise
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        return locator.is_checked()

    def scroll_to_element(self, selector: str, timeout: int = 30000) -> None:
        """
        Scroll to an element.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.scroll_into_view_if_needed()

    def hover_element(self, selector: str, timeout: int = 30000) -> None:
        """
        Hover over an element.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.hover()

    def double_click_element(self, selector: str, timeout: int = 30000) -> None:
        """
        Double-click an element.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.dblclick()

    def right_click_element(self, selector: str, timeout: int = 30000) -> None:
        """
        Right-click (context menu) on an element.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.click(button="right")

    def clear_field(self, selector: str, timeout: int = 30000) -> None:
        """
        Clear the content of an input field.

        Args:
            selector: CSS selector or XPath of the input element
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.clear()

    def press_key(self, selector: str, key: str, timeout: int = 30000) -> None:
        """
        Press a key in an element.

        Args:
            selector: CSS selector or XPath of the element
            key: Key to press (e.g., "Enter", "Tab", "Escape")
            timeout: Timeout in milliseconds
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        locator.press(key)

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a URL.

        Args:
            url: URL to navigate to
        """
        self.page.goto(url)

    def reload_page(self) -> None:
        """Reload the current page."""
        self.page.reload()

    def go_back(self) -> None:
        """Navigate back to the previous page."""
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward to the next page."""
        self.page.go_forward()

    def wait_for_url(
        self, url_pattern: str, timeout: int = 30000
    ) -> None:
        """
        Wait for the page to navigate to a specific URL.

        Args:
            url_pattern: URL pattern to wait for
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_url(url_pattern, timeout=timeout)

    def wait_for_function(
        self, function: Callable, timeout: int = 30000
    ) -> Any:
        """
        Wait for a function to return a truthy value.

        Args:
            function: Function to evaluate
            timeout: Timeout in milliseconds

        Returns:
            Return value of the function
        """
        return self.page.wait_for_function(function, timeout=timeout)

    def execute_script(self, script: str, *args) -> Any:
        """
        Execute JavaScript code in the page context.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script

        Returns:
            Return value of the script
        """
        return self.page.evaluate(script, *args)

    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """
        Wait for page to reach a specific load state.

        Args:
            state: Load state to wait for ("load", "domcontentloaded", "networkidle")
        """
        self.page.wait_for_load_state(state)

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Returns:
            Current page URL
        """
        return self.page.url

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Returns:
            Page title
        """
        return self.page.title()

    def assert_text_visible(
        self, selector: str, expected_text: str, timeout: int = 30000
    ) -> None:
        """
        Assert that an element contains expected text.

        Args:
            selector: CSS selector or XPath of the element
            expected_text: Expected text content
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If element text doesn't match expected
        """
        locator = self.wait_for_element(selector, timeout=timeout)
        expect(locator).to_contain_text(expected_text, timeout=timeout)

    def assert_element_visible(self, selector: str, timeout: int = 30000) -> None:
        """
        Assert that an element is visible.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If element is not visible
        """
        locator = self.page.locator(selector)
        expect(locator).to_be_visible(timeout=timeout)

    def assert_element_enabled(self, selector: str, timeout: int = 30000) -> None:
        """
        Assert that an element is enabled.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If element is not enabled
        """
        locator = self.page.locator(selector)
        expect(locator).to_be_enabled(timeout=timeout)

    def assert_element_disabled(self, selector: str, timeout: int = 30000) -> None:
        """
        Assert that an element is disabled.

        Args:
            selector: CSS selector or XPath of the element
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If element is not disabled
        """
        locator = self.page.locator(selector)
        expect(locator).to_be_disabled(timeout=timeout)

    def assert_checkbox_checked(self, selector: str, timeout: int = 30000) -> None:
        """
        Assert that a checkbox is checked.

        Args:
            selector: CSS selector or XPath of the checkbox
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If checkbox is not checked
        """
        locator = self.page.locator(selector)
        expect(locator).to_be_checked(timeout=timeout)

    def assert_checkbox_unchecked(self, selector: str, timeout: int = 30000) -> None:
        """
        Assert that a checkbox is unchecked.

        Args:
            selector: CSS selector or XPath of the checkbox
            timeout: Timeout in milliseconds

        Raises:
            AssertionError: If checkbox is checked
        """
        locator = self.page.locator(selector)
        expect(locator).not_to_be_checked(timeout=timeout)
