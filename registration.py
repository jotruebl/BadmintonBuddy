import logging
import os
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from emailer import EmailSender

logger = logging.getLogger(__name__)


HOST = "https://anc.ca.apm.activecommunities.com"


class RegistrationService:
    def __init__(
        self,
        username,
        password,
        email_sender_address,
        email_sender_password,
        is_dry_run=False,
    ):
        logger.info("Registration service initialized")
        self.username = username
        self.password = password
        self.email_sender_address = email_sender_address
        self.email_sender_password = email_sender_password
        self.is_dry_run_mode = is_dry_run

    def headless_register(self, email_notification_target_address, just_email):
        if email_notification_target_address:
            logger.info(
                f"Sending email notification to: {email_notification_target_address}",
            )
            email_sender = EmailSender(
                sender_email=self.email_sender_address,
                sender_password=self.email_sender_password,
            )

            email_sender.send_email(
                receiver_email=email_notification_target_address,
                # subject="Badminton Registration",
                # body="Your registration was successful.",
                subject="gogot",
                body="you are a gogot",
            )
            if just_email:
                return
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=chrome_options)
        try:
            self._login()
            self._click_enroll_now()
            self._select_participant()
            self._add_to_cart()
            self._checkout()
            result = self._pay()
        finally:
            self.driver.quit()

        if email_notification_target_address:
            email_sender = EmailSender(
                sender_email=self.email_sender_address,
                sender_password=self.email_sender_password,
            )

            email_sender.send_email(
                receiver_email=email_notification_target_address,
                # subject="Badminton Registration",
                # body="Your registration was successful.",
                subject="gogot",
                body=f"finished. dry_run_status: {self.is_dry_run_mode}",
            )

    def _pay(self):
        if self.is_dry_run_mode:
            logger.info("Dry run enabled. Skipping payment.")
            return
        secret_code = os.getenv("CVV_CODE", None)  # Replace with the actual CVV code
        if not secret_code:
            logger.error("CVV code not found. Payment cannot be completed.")
            raise Exception("CVV code not found. Payment cannot be completed.")
        cvv_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "form_group_input3__cvv"))
        )
        cvv_input.send_keys(secret_code)

        pay_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pay__button"))
        )
        pay_button.click()
        logger.info("Clicked 'Pay' button to complete the transaction.")

    def _checkout(self):
        check_out_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.checkout__button"))
        )
        check_out_button.click()
        logger.info("Clicked 'Check out'.")

    def _add_to_cart(self):
        add_to_cart_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fee-summary__add-to-cart-button")
            )
        )
        add_to_cart_button.click()
        logger.info("Clicked 'Add to Cart'.")

    def _select_participant(self):
        dropdown_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".dropdown__button"))
        )
        dropdown_button.click()

        dropdown_menu = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.dropdown__menu"))
        )

        participant_option = self.driver.find_element(
            By.XPATH, "//li[@title='Khushboo Jhugroo']"
        )

        actions = ActionChains(self.driver)
        actions.move_to_element(participant_option).click().perform()
        logger.info("Selected participant: Khushboo Jhugroo")

    def _click_enroll_now(self):
        self.driver.get(
            "https://anc.ca.apm.activecommunities.com/vancouver/activity/search?onlineSiteId=0&activity_select_param=2&center_ids=53&activity_keyword=Badminton%20&viewMode=list"
        )
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "activity-container"))
        )
        activities = self.driver.find_elements(By.CLASS_NAME, "activity-container")
        for activity in activities:
            activity_name = activity.find_element(
                By.CSS_SELECTOR, ".activity-card-info__name h3 a span"
            ).text.strip()
            if activity_name == "Badminton":
                try:
                    enroll_button = activity.find_element(
                        By.CSS_SELECTOR,
                        ".activity-card__fee-action-wrapper .activity-card__action-button button",
                    )
                    if enroll_button:
                        enroll_button.click()
                        logger.info("Clicked on 'Enroll Now' for Badminton activity.")
                        break
                except Exception as e:
                    logger.error(f"Error clicking 'Enroll Now' button: {e}")
                    continue
        else:
            logger.info("No 'Enroll Now' button found for the Badminton activity.")
            raise Exception("No 'Enroll Now' button found for the Badminton activity.")

    def _login(self):
        self.driver.get("https://anc.ca.apm.activecommunities.com/vancouver/signin")

        email_field = self.driver.find_element(
            By.CSS_SELECTOR, "input[aria-label='Email address Required']"
        )
        email_field.send_keys(self.username)

        password_field = self.driver.find_element(
            By.CSS_SELECTOR, "input[aria-label='Password Required']"
        )
        password_field.send_keys(self.password)

        sign_in_button = self.driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        )
        sign_in_button.click()

        WebDriverWait(self.driver, 10).until(EC.url_contains("/vancouver/"))
        logger.info("Current URL after login attempt:", self.driver.current_url)
