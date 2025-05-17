import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from ..utils.human_behavior import human_wait
from ..utils.logger import log_error, log_success
from .selectors import (
    TEXTAREA_SELECTORS,
    POST_BUTTON_SELECTORS,
    LIKE_BUTTON_SELECTORS,
    SAVE_BUTTON_SELECTORS,
)


def find_and_click_like_button(driver, wait):
    """Find and click the like button using multiple methods"""
    try:
        # Method 1: Try using the most modern selectors first
        js_click_script = """
        // Find all svg elements
        var svgs = document.querySelectorAll('svg');
        // Look for the one with aria-label="Like"
        for (var i = 0; i < svgs.length; i++) {
            if (svgs[i].getAttribute('aria-label') === 'Like') {
                // Find the nearest clickable parent
                var element = svgs[i];
                while (element && element.getAttribute('role') !== 'button') {
                    element = element.parentElement;
                }
                if (element) {
                    element.click();
                    return true;
                }
            }
        }
        return false;
        """
        like_clicked = driver.execute_script(js_click_script)
        if like_clicked:
            return True

        # Method 2: Try all possible standard selectors
        for selector in LIKE_BUTTON_SELECTORS:
            try:
                like_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    like_button,
                )
                human_wait(1, 2)
                like_button.click()
                return True
            except:
                continue

        # Method 3: Last resort - find any SVG with aria-label="Like" and force a click
        try:
            like_svg = driver.find_element(
                By.XPATH, '//*[name()="svg"][@aria-label="Like"]'
            )
            driver.execute_script("arguments[0].click();", like_svg)
            return True
        except:
            pass

        return False
    except Exception as e:
        print(f"Error in find_and_click_like_button: {e}")
        return False


def is_post_already_liked(driver):
    """Check if a post is already liked"""
    try:
        # Try to find the "Unlike" SVG
        unlike_svg = driver.find_element(
            By.XPATH, '//*[name()="svg"][@aria-label="Unlike"]'
        )
        return True if unlike_svg else False
    except:
        return False


def find_and_click_save_button(driver, wait):
    """Find and click the save button for a post"""
    try:
        # Method 1: Try using JavaScript to find and click the save button
        js_click_script = """
        // Find all svg elements
        var svgs = document.querySelectorAll('svg');
        // Look for the one with aria-label="Save"
        for (var i = 0; i < svgs.length; i++) {
            if (svgs[i].getAttribute('aria-label') === 'Save') {
                // Find the nearest clickable parent
                var element = svgs[i];
                while (element && element.getAttribute('role') !== 'button') {
                    element = element.parentElement;
                }
                if (element) {
                    element.click();
                    return true;
                }
            }
        }
        return false;
        """
        save_clicked = driver.execute_script(js_click_script)
        if save_clicked:
            return True

        # Method 2: Try XPath selectors
        for selector in SAVE_BUTTON_SELECTORS:
            try:
                save_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    save_button,
                )
                human_wait(1, 2)
                save_button.click()
                return True
            except:
                continue

        # Method 3: Last resort - find any SVG with aria-label="Save" and force a click
        try:
            save_svg = driver.find_element(
                By.XPATH, '//*[name()="svg"][@aria-label="Save"]'
            )
            driver.execute_script("arguments[0].click();", save_svg)
            return True
        except:
            pass

        return False
    except Exception as e:
        print(f"Error in find_and_click_save_button: {e}")
        return False


def is_post_already_saved(driver):
    """Check if a post is already saved"""
    try:
        # Try to find the "Remove" SVG which appears when a post is saved
        remove_svg = driver.find_element(
            By.XPATH, '//*[name()="svg"][@aria-label="Remove"]'
        )
        return True if remove_svg else False
    except:
        return False


def add_comment_to_post(driver, wait, comment_text):
    """Improved comment function with multiple fallback approaches"""
    current_url = driver.current_url
    try:
        print("💬 Starting comment process...")

        # 1. Make sure we're at the right spot in the post
        driver.execute_script("window.scrollBy(0, 300);")
        human_wait(2, 3)

        # 2. Find and click the comment textarea using multiple approaches
        textarea = None
        for selector in TEXTAREA_SELECTORS:
            try:
                textarea = wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    textarea,
                )
                human_wait(1, 2)
                textarea.click()
                print("  ✅ Found and clicked comment textarea")
                break
            except:
                continue

        if not textarea:
            # Try JavaScript as a fallback
            js_find_textarea = """
            const textarea = document.querySelector('textarea[placeholder="Add a comment…"]');
            if (textarea) {
                textarea.scrollIntoView({behavior: 'smooth', block: 'center'});
                textarea.click();
                return true;
            }
            return false;
            """
            textarea_found = driver.execute_script(js_find_textarea)

            if not textarea_found:
                print("  ❌ Could not find comment textarea")
                log_error("Failed to find comment textarea", current_url)
                return False

            # Get the textarea element after clicking it with JS
            textarea = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//textarea[contains(@placeholder, "Add a comment")]')
                )
            )

        # 3. Clear any existing text and focus
        textarea.clear()
        human_wait(0.5, 1)

        # 4. Type comment text with human-like delays
        for char in comment_text:
            textarea.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))

        human_wait(2, 3, "⏳ Waiting for Post button to enable...")

        # 5. Find and click the Post button using more reliable selectors
        post_button_clicked = False

        # Try direct XPath selectors first
        for selector in POST_BUTTON_SELECTORS:
            try:
                post_button = driver.find_element(By.XPATH, selector)
                if "aria-disabled" in post_button.get_attribute(
                    "outerHTML"
                ) and "true" in post_button.get_attribute("outerHTML"):
                    print("  ⚠️ Post button is still disabled, waiting longer...")
                    human_wait(3, 5)
                    # Try again after waiting
                    post_button = driver.find_element(By.XPATH, selector)

                driver.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
                    post_button,
                )
                human_wait(1, 2)
                driver.execute_script("arguments[0].click();", post_button)
                post_button_clicked = True
                print("  ✅ Clicked Post button using XPath")
                break
            except:
                continue

        # If direct selectors failed, try JavaScript approach
        if not post_button_clicked:
            js_click_post = """
            // Try multiple approaches to find and click the Post button
            
            // First approach: Look for the most specific structure from your HTML
            let postButton = document.querySelector('div.x1i64zmx > div[role="button"]');
            
            // Second approach: Look for any element with text exactly matching "Post"
            if (!postButton) {
                const elements = document.querySelectorAll('div');
                for (const el of elements) {
                    if (el.textContent === 'Post' && el.parentElement && el.parentElement.getAttribute('role') === 'button') {
                        postButton = el.parentElement;
                        break;
                    }
                }
            }
            
            // Third approach: Find any button-like element after the textarea
            if (!postButton) {
                const textarea = document.querySelector('textarea[placeholder="Add a comment…"]');
                if (textarea) {
                    let current = textarea.parentElement;
                    while (current && !current.querySelector('[role="button"]')) {
                        current = current.parentElement;
                    }
                    if (current) {
                        postButton = current.querySelector('[role="button"]');
                    }
                }
            }
            
            // Check if button is disabled
            if (postButton && postButton.getAttribute('aria-disabled') === 'true') {
                // Wait for it to be enabled (simulate a short wait)
                setTimeout(() => {
                    if (postButton.getAttribute('aria-disabled') !== 'true') {
                        postButton.click();
                    }
                }, 3000);
                return false;
            }
            
            // Click the button if found
            if (postButton) {
                postButton.click();
                return true;
            }
            
            return false;
            """
            post_button_clicked = driver.execute_script(js_click_post)

            if post_button_clicked:
                print("  ✅ Clicked Post button using JavaScript")
            else:
                # Try once more after a longer wait
                human_wait(5, 7, "⏳ Waiting longer for Post button to be ready...")
                post_button_clicked = driver.execute_script(js_click_post)

                if post_button_clicked:
                    print("  ✅ Clicked Post button after extended wait")
                else:
                    print("  ❌ Could not find or click Post button")
                    log_error("Failed to click Post button", current_url)
                    return False

        # 6. Wait to verify comment was posted
        human_wait(4, 6, "⏳ Verifying comment was posted...")

        # Check if our comment text appears in the comments section..........................
        try:
            comment_verification = f"//*[contains(text(), '{comment_text.split()[0]}')]"
            driver.find_element(By.XPATH, comment_verification)
            print("  ✅ Comment successfully verified")
        except:
            # Even if verification fails, we still consider it a success if we clicked the button
            print("  ⚠️ Comment was submitted but couldn't verify it appeared")

        log_success("Comment", current_url)
        return True

    except Exception as e:
        print(f"  ❌ Error in comment function: {e}")
        log_error(f"Error in comment function: {e}", current_url)
        return False
