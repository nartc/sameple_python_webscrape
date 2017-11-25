from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import base64
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import pymongo

myUrl = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage_false_0&entitySelectingHelper.selectedEntity=&zip=63034#resultsPage=1'
detailLinks = []

#MongoClient
mongo_client = pymongo.MongoClient("localhost", 27017)
db = mongo_client.cars_database
cars = db.cars


# Grab Individual URL
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(myUrl)
wait = WebDriverWait(driver, 100)
time.sleep(1)
elems = driver.find_elements(By.CSS_SELECTOR, "div[id^='listing_']")

filename = "cars.csv"
f = open(filename, "w")

headers = "year, make, model, full_name, current_price, estimated_payment, mileage, detail_link\n"

f.write(headers)

for elem in elems:
    detailLinkPlaceHolder = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage_false_0&entitySelectingHelper.selectedEntity=&zip=63034#listing='

    idPlaceholder = elem.get_attribute("id").split("_")[1]
    detailLinkPlaceHolder += idPlaceholder
    detailLinks.append(detailLinkPlaceHolder)

    #img
    img_container = elem.find_element(By.CLASS_NAME, "cg-dealFinder-result-img")
    img_src_container = img_container.find_element(By.ID, idPlaceholder)
    img_file_name = img_src_container.get_attribute("src")
    if img_file_name.split('.')[0] == '//static':
        img_file_name = 'https:' + img_file_name

    img_file = BytesIO(urlopen(img_file_name).read())
    img_raw = Image.open(img_file)
    buffer = BytesIO()
    if img_file_name.endswith('.jpeg'):
        img_raw.save(buffer, format="JPEG")
    elif img_file_name.endswith('.png'):
        img_raw.save(buffer, format="PNG")
    

    #car_img
    car_img_b64 = base64.b64encode(buffer.getvalue())


    car_name_tag = elem.find_element(By.CLASS_NAME, "cg-dealFinder-result-model")

    # carName
    car_name = car_name_tag.text

    car_name_split = car_name.split(" ")

    # carInfo
    car_year = car_name_split[0]
    car_make = car_name_split[1]
    if car_make == 'BMW':
        if car_name_split[3] == 'Series':
            if len(car_name_split) > 4:
                if car_name_split[4] == 'Gran':
                    car_model = car_name_split[6]

                car_model = car_name_split[4]
            else:
                car_model = car_name_split[2]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Chrysler':
        if car_name_split[2] == 'Town':
            car_model = car_name_split[2] + ' ' + car_name_split[3] + ' ' + car_name_split[4]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Dodge':
        if car_name_split[2] == 'Ram':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        elif car_name_split[2] == 'Grand':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'GMC':
        if len(car_name_split) > 3:
            if car_name_split[3] == 'XL':
                car_model = car_name_split[2] + ' ' + car_name_split[3]
            elif car_name_split[2] == 'Sierra':
                car_model = car_name_split[2] + ' ' + car_name_split[3]
            else:
                car_model = car_name_split[2]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Jeep':
        if car_name_split[2] == 'Grand':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Land':
        car_make = car_name_split[1] + ' ' + car_name_split[2]
        if car_name_split[4] == 'Rover':
            car_model = car_name_split[3] + ' ' + car_name_split[4]
        else:
            car_model = car_name_split[3]
    elif car_make == 'Lexus':
        car_model = car_name_split[2] + ' ' + car_name_split[3]
    elif car_make == 'Mercedes-Benz':
        if len(car_name_split) > 3:
            car_model = car_name_split[3] + ' ' + car_name_split[4]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Pontiac':
        if car_name_split[2] == 'Grand':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Porsche':
        if car_name_split[2] == 'Macan':
            car_model = car_name_split[2]
        else:
            car_model = car_name_split[2] + ' ' + car_name_split[3]
    elif car_make == 'Toyota':
        if len(car_name_split) > 3:
            if car_name_split[3] == 'Solara':
                car_model = car_name_split[2] + ' ' + car_name_split[3]
            else:
                car_model = car_name_split[2]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Chevrolet':
        if car_name_split[2] == 'Silverado':
            if len(car_name_split) > 3:
                car_model = car_name_split[2] + ' ' + car_name_split[3]
        elif car_name_split[2] == 'Monte':
            if len(car_name_split) > 3:
                car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Hyundai':
        if car_name_split[2] == 'Santa':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Jaguar':
        if car_name_split[2] == 'XJ-Series':
            car_model = car_name_split[3]
        else:
            car_model = car_name_split[2]
    elif car_make == 'Saturn':
        if car_name_split[2] == 'Sky':
            car_model = car_name_split[2] + ' ' + car_name_split[3]
        else:
            car_model = car_name_split[2]
    else:
        car_model = car_name_split[2]

    price_tag = elem.find_element(By.CSS_SELECTOR, "span[class='cg-dealFinder-priceAndMoPayment']")
    prices = price_tag.text
    split_prices = prices.split(" ")

    # carPrice + estPmt
    current_price = split_prices[0]
    current_car_price = current_price.replace("$", "")
    current_price = current_car_price.replace(",", "")
    if len(split_prices) == 4:
        est_pmt = split_prices[2]
    elif len(split_prices) == 3:
        est_pmt = split_prices[1]

    est_payment = est_pmt.replace(",", "")

    mileage_tag = elem.find_element(By.CSS_SELECTOR, ".cg-dealFinder-result-stats p:nth-child(2)")
    mileage_tag_text = mileage_tag.text
    milage_tag_split = mileage_tag_text.split(" ")

    # carMileage
    car_mileage = milage_tag_split[1]
    car_mile = car_mileage.replace(",", "")

    #current_price
    

    f.write(car_year + "," + car_make + "," + car_model + "," + car_name + "," + current_price + "," + est_payment + "," + car_mile + "," + detailLinkPlaceHolder + "\n")

    car={
        "carYear": car_year,
        "carMake": car_make,
        "carModel": car_model,
        "carFullName": car_name,
        "currentPrice": current_price,
        "estimatedPayment": est_payment,
        "carMileage": car_mile,
        "detailLink": detailLinkPlaceHolder,
        "carImage": car_img_b64
    }

    cars.insert_one(car)


while True:
    try:
        next_button = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nextPageElement")), "No more Next button")
        next_button.click()
        time.sleep(2)
        elems = driver.find_elements(By.CSS_SELECTOR, "div[id^='listing_']")
        for elem in elems:
            detailLinkPlaceHolder = 'https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePage_false_0&entitySelectingHelper.selectedEntity=&zip=63034#listing='

            idPlaceholder = elem.get_attribute("id").split("_")[1]
            detailLinkPlaceHolder += idPlaceholder
            detailLinks.append(detailLinkPlaceHolder)

            #img
            img_container = elem.find_element(By.CLASS_NAME, "cg-dealFinder-result-img")
            img_src_container = img_container.find_element(By.ID, idPlaceholder)
            img_file_name = img_src_container.get_attribute("src")
            if img_file_name.split('.')[0] == '//static':
                img_file_name = 'https:' + img_file_name

            img_file = BytesIO(urlopen(img_file_name).read())
            img_raw = Image.open(img_file)
            buffer = BytesIO()
            if img_file_name.endswith('.jpeg'):
                img_raw.save(buffer, format="JPEG")
            elif img_file_name.endswith('.png'):
                img_raw.save(buffer, format="PNG")
            

            #car_img
            car_img_b64 = base64.b64encode(buffer.getvalue())

            car_name_tag = elem.find_element(By.CLASS_NAME, "cg-dealFinder-result-model")

            # carName
            car_name = car_name_tag.text

            car_name_split = car_name.split(" ")

            # carInfo
            car_year = car_name_split[0]
            car_make = car_name_split[1]
            if car_make == 'BMW':
                if car_name_split[3] == 'Series':
                    if len(car_name_split) > 4:
                        if car_name_split[4] == 'Gran':
                            car_model = car_name_split[6]

                        car_model = car_name_split[4]
                    else:
                        car_model = car_name_split[2]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Chrysler':
                if car_name_split[2] == 'Town':
                    car_model = car_name_split[2] + ' ' + car_name_split[3] + ' ' + car_name_split[4]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Dodge':
                if car_name_split[2] == 'Ram':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                elif car_name_split[2] == 'Grand':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'GMC':
                if len(car_name_split) > 3:
                    if car_name_split[3] == 'XL':
                        car_model = car_name_split[2] + ' ' + car_name_split[3]
                    elif car_name_split[2] == 'Sierra':
                        car_model = car_name_split[2] + ' ' + car_name_split[3]
                    else:
                        car_model = car_name_split[2]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Jeep':
                if car_name_split[2] == 'Grand':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Land':
                car_make = car_name_split[1] + ' ' + car_name_split[2]
                if car_name_split[4] == 'Rover':
                    car_model = car_name_split[3] + ' ' + car_name_split[4]
                else:
                    car_model = car_name_split[3]
            elif car_make == 'Lexus':
                car_model = car_name_split[2] + ' ' + car_name_split[3]
            elif car_make == 'Mercedes-Benz':
                if len(car_name_split) > 3:
                    car_model = car_name_split[3] + ' ' + car_name_split[4]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Pontiac':
                if car_name_split[2] == 'Grand':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Porsche':
                if car_name_split[2] == 'Macan':
                    car_model = car_name_split[2]
                else:
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
            elif car_make == 'Toyota':
                if len(car_name_split) > 3:
                    if car_name_split[3] == 'Solara':
                        car_model = car_name_split[2] + ' ' + car_name_split[3]
                    else:
                        car_model = car_name_split[2]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Chevrolet':
                if car_name_split[2] == 'Silverado':
                    if len(car_name_split) > 3:
                        car_model = car_name_split[2] + ' ' + car_name_split[3]
                elif car_name_split[2] == 'Monte':
                    if len(car_name_split) > 3:
                        car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Hyundai':
                if car_name_split[2] == 'Santa':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Jaguar':
                if car_name_split[2] == 'XJ-Series':
                    car_model = car_name_split[3]
                else:
                    car_model = car_name_split[2]
            elif car_make == 'Saturn':
                if car_name_split[2] == 'Sky':
                    car_model = car_name_split[2] + ' ' + car_name_split[3]
                else:
                    car_model = car_name_split[2]
            else:
                car_model = car_name_split[2]

            price_tag = elem.find_element(By.CSS_SELECTOR, "span[class='cg-dealFinder-priceAndMoPayment']")
            prices = price_tag.text
            split_prices = prices.split(" ")

            # carPrice + estPmt
            current_price = split_prices[0]
            current_car_price = current_price.replace("$", "")
            current_price = current_car_price.replace(",", "")

            if len(split_prices) == 4:
                est_pmt = split_prices[2]
            elif len(split_prices) == 3:
                est_pmt = split_prices[1]

            est_payment = est_pmt.replace(",", "")

            mileage_tag = elem.find_element(By.CSS_SELECTOR, ".cg-dealFinder-result-stats p:nth-child(2)")
            mileage_tag_text = mileage_tag.text
            milage_tag_split = mileage_tag_text.split(" ")

            # carMileage
            car_mileage = milage_tag_split[1]
            car_mile = car_mileage.replace(",", "")
            
            f.write(car_year + "," + car_make + "," + car_model + "," + car_name + "," + current_price + "," + est_payment + "," + car_mile + "," + detailLinkPlaceHolder + "\n")

            car={
                "carYear": car_year,
                "carMake": car_make,
                "carModel": car_model,
                "carFullName": car_name,
                "currentPrice": current_price,
                "estimatedPayment": est_payment,
                "carMileage": car_mile,
                "detailLink": detailLinkPlaceHolder,
                "carImage": car_img_b64
            }

            cars.insert_one(car)

    except TimeoutException:
        break
    
    

    
f.close()

time.sleep(0.2)
print(len(detailLinks))


