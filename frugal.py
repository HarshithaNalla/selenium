'''
Created on 24 Nov 2024

@author: nalla
'''
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import time
import random
import string
from selenium.webdriver.common.keys import Keys


class OrangeHRMAutomation:
    def __init__(self):
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        
        # Initialize the WebDriver
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)
        
    def login(self, username, password):
        """Login to OrangeHRM"""
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        
        # Print URL and Title
        print(f"Current URL: {self.driver.current_url}")
        print(f"Page Title: {self.driver.title}")
        
        # Login
        self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(username)
        self.wait.until(EC.presence_of_element_located((By.NAME, "password"))).send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        
    def add_employee(self, first_name, middle_name, last_name):
        """Add a new employee with login details"""
        # Navigate to PIM
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))).click()
        time.sleep(2)  # Short wait for page load
        
        # Click Add Employee
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()
        
        # Fill employee details
        self.wait.until(EC.presence_of_element_located((By.NAME, "firstName"))).send_keys(first_name)
        self.driver.find_element(By.NAME, "middleName").send_keys(middle_name)
        self.driver.find_element(By.NAME, "lastName").send_keys(last_name)
        
        # Enable login details
        create_login_checkbox = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//span[contains(@class, 'oxd-switch-input')]")))
        create_login_checkbox.click()
        
        # Generate random username and password
        employee_username = "harshi_72"
        employee_password = "harshi_07"
        
        # Fill login details
        username_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//label[contains(text(), 'Username')]/../..//input")))
        username_field.clear()
        username_field.send_keys(employee_username)
        
        password_fields = self.driver.find_elements(By.XPATH, "//input[@type='password']")
        password_fields[0].send_keys(employee_password)
        password_fields[1].send_keys(employee_password)
        
        # Save employee
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
        time.sleep(3)  # Wait for save to complete
        
        return employee_username, employee_password
        
    def assign_admin_role(self, employee_name, username, password):
        try:
            # Navigate to Admin
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Admin']"))).click()
            time.sleep(2)
    
            # Click Add User
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()
            time.sleep(2)
    
            # Select User Role dropdown and choose Admin
            user_role_dropdown = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'User Role')]/../..//div[contains(@class, 'oxd-select-text')]")))
            user_role_dropdown.click()
            time.sleep(1)
            
            admin_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='listbox']//span[text()='Admin']")))
            admin_option.click()
    
            # Select Status dropdown and choose Enabled
            status_dropdown = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Status')]/../..//div[contains(@class, 'oxd-select-text')]")))
            status_dropdown.click()
            time.sleep(1)
            
            enabled_option = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='listbox']//span[text()='Enabled']")))
            enabled_option.click()
    
            # Enhanced employee name input and selection
            employee_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Employee Name')]/../..//input")))
            employee_input.clear()
    
            # Type employee name character by character
            for char in employee_name:
                employee_input.send_keys(char)
                time.sleep(0.3)  # Slow down typing to allow dropdown to update
            
            time.sleep(2)  # Wait for dropdown to appear
    
            try:
                # Try first approach - exact match
                employee_option = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH, 
                        f"//div[@role='listbox']//span[contains(text(), '{employee_name}')]"
                    ))
                )
                self.driver.execute_script("arguments[0].click();", employee_option)
            except Exception as e:
                self.logger.warning(f"First attempt to select employee failed: {str(e)}")
                try:
                    # Try second approach - partial match
                    employee_option = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((
                            By.XPATH, 
                            f"//div[@role='listbox']//span"
                        ))
                    )
                    self.driver.execute_script("arguments[0].click();", employee_option)
                except Exception as e:
                    self.logger.warning(f"Second attempt to select employee failed: {str(e)}")
                    # Try third approach - using keyboard
                    employee_input.send_keys(Keys.ARROW_DOWN)
                    time.sleep(1)
                    employee_input.send_keys(Keys.ENTER)
    
            time.sleep(2)  # Wait after employee selection
    
            # Enter username
            username_field = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//label[contains(text(), 'Username')]/../..//input")))
            username_field.clear()
            username_field.send_keys(username)
    
            # Enter password in both fields
            password_fields = self.driver.find_elements(By.XPATH, "//input[@type='password']")
            for field in password_fields:
                field.clear()
                field.send_keys(password)
                time.sleep(0.5)
    
            # Save admin user
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
            time.sleep(3)
    
        except Exception as e:
            self.logger.error(f"Failed to assign admin role: {str(e)}")
            self.take_screenshot("assign_admin_error")
            raise

    def logout(self):
        """Logout from OrangeHRM"""
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))).click()
        time.sleep(1)  # Wait for dropdown
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Logout']"))).click()
        
    def close_browser(self):
        """Close the browser"""
        self.driver.quit()

def main():
    # Initialize the automation
    orange_hrm = OrangeHRMAutomation()
    
    try:
        # Login as admin
        orange_hrm.login("Admin", "admin123")
        time.sleep(2)  # Wait for dashboard to load
        
        # Add new employee
        first_name = "John"
        middle_name = "William"
        last_name = "Doe"
        employee_username, employee_password = orange_hrm.add_employee(first_name, middle_name, last_name)
        
        # Wait for employee creation to complete
        time.sleep(3)
        
        # Assign admin role
        full_name = f"{first_name} {middle_name} {last_name}"
        orange_hrm.assign_admin_role(full_name, employee_username, employee_password)
        
        # Logout
        orange_hrm.logout()
        
        # Wait before logging in with new credentials
        time.sleep(2)
        
        # Login with new admin credentials
        orange_hrm.login(employee_username, employee_password)
        
        # Wait to see the logged-in state
        time.sleep(3)
        
        # Final logout
        orange_hrm.logout()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Close the browser
        orange_hrm.close_browser()

if __name__ == "__main__":
    main()   