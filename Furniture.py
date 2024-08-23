
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import sqlite3, random
from Backend import myDB
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import re,base64
from getpass import getpass
from Notification import sendNotification



class Furniture(webdriver.Chrome):
    
    def __init__(self,path = r'YourWebBrowserPath'):
        self.driverpath = path
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.binary_location = path
        super().__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        self.DB=myDB()
    

    def landFirstPage(self, url ='https://www.woodenstreet.com/furniture-store-chennai' ):
        self.get(url)


    def closeModal(self):
        registerModal = self.find_element(By.CLASS_NAME, 'swpmodal-container')
        closeButton = registerModal.find_element(By.XPATH, '//*[@id="loginclose1"]')
        closeButton.click()


    def selectSignIn(self):
        registerModal = self.find_element(By.CLASS_NAME, 'swpmodal-container')
        signInLink = registerModal.find_element(By.XPATH, '//*[@id="register_form_pop"]/div[5]/p[1]/a')
        signInLink.click()


    def loginIn(self):
        UserInfo = self.readUserInfo()
        loginModal = self.find_element(By.XPATH, '//*[@id="login-pop"]')
        emailTextBox = loginModal.find_element(By.XPATH, '//*[@id="login_email"]')
        emailTextBox.send_keys(UserInfo[0])
        passwordTextBox = loginModal.find_element(By.XPATH, '//*[@id="password"]')
        passwordTextBox.send_keys(UserInfo[1] + Keys.RETURN)
        

    def wishlist(self):
        self.refresh()
        navBar = self.find_element(By.XPATH, '/html/body/header/div')
        wishlistButton = navBar.find_element(By.XPATH, '/html/body/header/div/a[3]')
        wishlistButton.click()
        self.DB.createDB()


    def replaceSignInDetails(self):
        while True:
            email = input("Enter email: ")
            if re.match(r'^[\w\.-]+@[\w\.-]+$', email):
                break
            else:
                print("Invalid email format. Please try again.")

        passwrd = getpass("Enter password: ")
        encoded_email = base64.b64encode(email.encode())
        encoded_password = base64.b64encode(passwrd.encode())

        with open('Secret.dat', 'wb') as file:
            file.write(encoded_email + b'\n')
            file.write(encoded_password)

    def readUserInfo(self):
        with open('Secret.dat', 'rb') as file:
            lines = file.readlines()
            decoded_email = base64.b64decode(lines[0]).decode().strip()
            decoded_password = base64.b64decode(lines[1]).decode().strip()
        return [decoded_email, decoded_password]


    def parseWishList(self):
        self.refresh()
        wishlist_items = self.find_elements(By.CSS_SELECTOR, '.li_wish')
        conn = sqlite3.connect('wishlist.db')
        cursor = conn.cursor()
        decreased_items = []

        for item in wishlist_items:
            item_name = item.find_element(By.CSS_SELECTOR, 'a.name').text.strip()
            item_price = float(item.find_element(By.CSS_SELECTOR, 'strong').text.strip().replace('Rs ', '').replace(',', ''))
            item_url = item.find_element(By.CSS_SELECTOR, 'a.name').get_attribute('href')

            cursor.execute("SELECT id, price FROM items WHERE name = ? ORDER BY timestamp DESC LIMIT 1", (item_name,))
            recent_item_data = cursor.fetchone()
            

            if recent_item_data:
                recent_item_id, stored_price = recent_item_data
                if item_price < stored_price:
                    cursor.execute("INSERT INTO items (name,price,url,timestamp) VALUES (?,?,?,CURRENT_TIMESTAMP)", (item_name,item_price,item_url))
                    decreased_items.append((item_name, item_price))
            else:
                cursor.execute("INSERT INTO items (name, price, url, timestamp) VALUES (?, ?, ?,CURRENT_TIMESTAMP)", (item_name, item_price, item_url))
        if len(decreased_items) !=0:
            self.plotItems(decreased_items, cursor)
            sendNotification(self.readUserInfo()[0], decreased_items) 

        conn.commit()
        conn.close()


    def insertDummyData(self):
        current_timestamp = datetime.now()

        items_data = [
            ("Antique Gold Mild Steel Contemporary Wall Light", 2500.0, "https://www.woodenstreet.com/product/antique-gold-mild-steel-contemporary-wall-light"),
            ("Biped Brown Wooden Floor Lamp", 9000.0, "https://www.woodenstreet.com/product/biped-brown-wooden-floor-lamp"),
            ("GetRest LuxeAdapt 12 ErgoMax Organic Latex 7 layered Mattress with Biocrystal Stress Relief and Airflow Cooling (12 inch, King Size, 72 x 72)", 50000.0, "https://www.woodenstreet.com/product/getrest-luxeadapt-12-ergomax-org-latex-7-layer-mattres-biocrystal-relief-airflow-12-king-72-72"),
            ("Alfonso Right Aligned Convertible Sofa Cum Bed (Cotton, Indigo Ink)", 52000.0, "https://www.woodenstreet.com/product/alfonso-fabric-sofa-cum-bed-blue"),
            ("Paxton Premium Velvet 3 Seater Fabric Sofa Cum Bed (Dark Olive Green)", 13000.0, "https://www.woodenstreet.com/product/paxton-fabric-sofa-cum-bed-dark-olive-green"),
            ("Riota Sheesham Wood Sofa Bed With Storage (King Size, Honey Teal Aqua Marine)", 45000.0, "https://www.woodenstreet.com/product/riota-sheesham-wood-sofa-bed-with-storage-king-size-honey-teal-aqua-marine"),
            ("Sereta Sheesham Wood Sofa Cum Bed (King Size, Honey Finish)", 46000.0, "https://www.woodenstreet.com/product/sereta-sofa-cum-bed-honey-finish"),
            ("Penguin Bamboo Bliss High Density HR Memory Foam Mattress (6 inch, Queen Size, 78 x 60)", 17000.0, "https://www.woodenstreet.com/product/penguin-bamboo-bliss-high-density-hr-memory-foam-mattress-6-inch-queen-size-78-x-60"),
            ("Kosmo Universal 2 Door Sliding Wardrobe (Exotic Teak Finish)", 70000.0, "https://www.woodenstreet.com/product/kosmo-universal-2-door-sliding-wardrobe-in-natural-teak-finish")
        ]

        for i in range(1,4):
            for item_name, item_price, item_url in items_data:
                dummy_price = random.uniform(item_price - 5000, item_price + 5000)
                past_timestamp = current_timestamp - timedelta(days=i)

                self.DB.EstbConn()
                self.DB.cursor.execute("INSERT INTO items (name, price, url, timestamp) VALUES (?, ?, ?, ?)",
                                       (item_name, dummy_price, item_url, past_timestamp))
                self.DB.closeConn()


    def plotItems(self, secquence, dbCon):
        plt.figure(figsize=(10, 8 * len(secquence))) 

        for idx, (name, price) in enumerate(secquence, 1):
            plt.subplot(len(secquence), 1, idx)  
            dbCon.execute("SELECT DATE(timestamp), price FROM items WHERE name = ? ORDER BY timestamp", (name,))
            data = dbCon.fetchall()
            dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
            prices = [row[1] for row in data]
            plt.plot(dates, prices, marker='o', linestyle='-')

            last_price = prices[-1]
            plt.axhline(y=last_price, color='gray', linestyle='--', linewidth=0.5)

            plt.xlabel('Date')
            plt.ylabel('Price (Rs)')
            plt.title(f'{name} Price Trend')
            plt.xticks(rotation=45)
            plt.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()
        plt.show()

    def run(self):
        self.landFirstPage()
        self.selectSignIn()
        self.loginIn()
        self.wishlist()
        self.parseWishList()

    def changeUserRun(self):
        self.replaceSignInDetails()
        self.landFirstPage()
        self.selectSignIn()
        self.loginIn()
        self.wishlist()
        self.parseWishList()



