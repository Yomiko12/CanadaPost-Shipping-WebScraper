from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import scraperClasses as sc
web = webdriver.Firefox()
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method
import os 

user_name = os.environ.get('USER')
password = os.environ.get('PASSWORD')

pricingList= []
items = []
provinces = []
provincePostalCodes = ['R3H1C2', 'L5P1B2', 'G2G0J4','E3B9G1', 'B2T1K2', 'A1A5T2','X0A0H0', 'X1A3T2', 'Y1A6E6','C1C1N2', 'V7B0A4', 'T9E0V3','S4W1B3']
provinceNames = ['Manitoba', 'Ontario', 'Quebec', 'New Brunswick', 'Nova Scotia', 'Newfoundland', 'Nunavut', 'Northwest Territories', 'Yukon Territories', 'Prince Edward Island', 'British Columbia', 'Alberta', 'Saskatchewan']
for i in range(13): provinces.append(sc.Province(provinceNames[i], provincePostalCodes[i]))


#######################
#USER MODIFIABLE VALUES
#######################
startLocationPostalCode = "R3X1W2"
items.append(sc.Item('Windshield', 16.2, 11.2, 6.5, 1.6))
items.append(sc.Item('Wallet', 10, 10, 10, 0.1))



######################
#FUNCTION DECLARATIONS
######################
def inputBoxSize(p): #Input corresponding sizing information for a given product
	web.find_element_by_xpath('//*[@id="length"]').clear()
	web.find_element_by_xpath('//*[@id="length"]').send_keys(str(p.length))
	web.find_element_by_xpath('//*[@id="width"]').clear()
	web.find_element_by_xpath('//*[@id="width"]').send_keys(str(p.width))
	web.find_element_by_xpath('//*[@id="height"]').clear()
	web.find_element_by_xpath('//*[@id="height"]').send_keys(str(p.height))
	web.find_element_by_xpath('//*[@id="weight"]').clear()
	web.find_element_by_xpath('//*[@id="weight"]').send_keys(str(p.weight))

def submitAndGetCost():#Return cost after all values have been inputted
	#Hide cookies popup
	try: web.find_element_by_xpath('/html/body/div[2]/div/div/cpc-footer/div[2]/div/div[2]/a').click()
	except: pass

	#Pricing page
	web.find_element_by_xpath('//*[@id="queryParcel:far_biz_common_fqp_continue"]').click()
	time.sleep(2)

	#Get price
	price =  web.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/form/div/div[2]/div[3]/div/div/dl/dd[1]/div/div/div[1]/div[2]/table/tbody/tr[7]/td[2]/strong').text
	price = float(price[1:])
	tax = web.find_element_by_xpath('/html/body/div[2]/div/div/div[2]/div/form/div/div[2]/div[3]/div/div/dl/dd[1]/div/div/div[1]/div[2]/table/tbody/tr[6]/td[2]').text
	tax = float(tax[1:])
	#Return
	web.execute_script("window.history.go(-1)")
	time.sleep(2)
	return price-tax

def printPrice():
	print (pricingList[-1].productName)
	print (pricingList[-1].locationName)
	print (pricingList[-1].shippingPrice)
	print('')

#################
#MAIN STARTS HERE
#################
#Go to canada post website
web.get('https://www.canadapost-postescanada.ca/information/app/far/business/findARate?execution=e2s1')
time.sleep(2)
web.find_element_by_xpath('/html/body/div[2]/div/div/cpc-header/div[2]/div[1]/nav/div[1]/section/ul/li[4]').click()
time.sleep(2)
web.find_element_by_xpath('//*[@id="usernameLarge"]').send_keys(user_name)
web.find_element_by_xpath('//*[@id="passwordLarge"]').send_keys(password)
web.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/form/input[3]').click()
time.sleep(5)
web.get('https://www.canadapost-postescanada.ca/information/app/far/business/findARate?execution=e2s1')
#Input start location postal code
web.find_element_by_xpath('//*[@id="fromPostalCode"]').send_keys(startLocationPostalCode)



#Iterate through all items
for i in range(len(items)):
	

	#Iterate through all location selection types
	for j in range(3):

		if j==0: #Get Canada shipping costs
			inputBoxSize(items[i])
			web.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/form/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/label').click()
			web.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/form/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/label').click()
			#Iterate through all provinces/territories
			for k in range(len(provinces)):
				try:
					#Clear and replace with new postal code
					web.find_element_by_xpath('//*[@id="toPostalCode"]').clear()
					web.find_element_by_xpath('//*[@id="toPostalCode"]').send_keys(provinces[k].postalCode)
					#Get price
					price = submitAndGetCost()
					#Add price information to database. FORMAT: product#, shipping type, location, price
					pricingList.append(sc.priceInfo(items[i].productName, provinces[k].provinceName, price))
					printPrice()
				except:
					print("Failed to get price for ", items[i].productName, " in ", provinces[k].provinceName, " (", provinces[k].postalCode, ")")
					time.sleep(5)

		if j==1: #Get America shipping costs
			select = Select(web.find_element_by_xpath('//*[@id="toDestination"]'))
			select.select_by_index(1)
			time.sleep(3)
			web.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/form/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/label').click()
			web.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div[2]/div/div[3]/form/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/label').click()
			inputBoxSize(items[i])

			for k in range(63):
				try:
					#Pick next state/territory
					select = Select(web.find_element_by_xpath('//*[@id="toUSState"]'))
					select.select_by_index(k+1)

					#Get price
					price = submitAndGetCost()
					#Add price information to database. FORMAT: product#, shipping type, location, price
					pricingList.append(sc.priceInfo(items[i].productName, ('State#'+str(k+1)), price))
					printPrice()
				except:
					print( "Failed to get price for ", items[i].productName, " in ", ( 'State#'+str(k+1) ) )
					time.sleep(5)