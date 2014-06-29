# -*- coding: utf-8 -*-
__author__ = 'Иван'
import urllib
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import Selenium2Library

# steam  tax 15%
# new API
""" http://steamcommunity.com/market/search/render/?query=Treasures+key&start=0&count=10 """

def get_some_offers(driver):
    driver.get("http://dota2lounge.com/?p=1")
    left_elems = driver.find_elements_by_class_name("left")
    right_elems = driver.find_elements_by_class_name("right")
    links = driver.find_elements_by_css_selector(".tradeheader a")
    link_list = []
    for el in links:
        #print el.get_attribute("href")
        link_list.append(el.get_attribute("href"))
    return left_elems, right_elems, link_list

def get_price_selenium(name):
    format_name = "&q="+"+".join(name.strip().split(" "))
    driver_retriever.get("http://steamcommunity.com/market/search?appid=570" + format_name)
    try:
        price = driver_retriever.find_element_by_css_selector(".market_table_value span").get_attribute("innerHTML")
        quantity = driver_retriever.find_element_by_css_selector("span.market_listing_num_listings_qty").get_attribute("innerHTML")
        #print "Name: ", name, " price: ", price, " Quantity: ", quantity
        money_val = float(price.split(" ")[0].lstrip("$"))
        #print money_val
        return money_val
    except:
        #print "bad name: ", name
        return False

def get_price_urllib(old_name):
    #print name
    name = "+".join(old_name.split(" "))
    counter = 0
    received = False
    error = False
    number = False
    while not received and counter < 2 and not error:
        try:
            f = urllib.urlopen(u"http://steamcommunity.com/market/search/render/?query=%s&start=0&count=1" % name.encode("utf-8"))
            string = f.read()
            if len(string) > 500:
                received = True
                try:
                    string = string[string.index("&#36;")+5:]
                    number = float(string[:string.index(" USD<\/span>")])
                    #print number
                except:
                    error = True
                    #print "error"
            else:
                #print "connection error"
                number = get_price_selenium(name)
                if number:
                    received = True
                else:
                    error = True
                    time.sleep(0.3)
                    counter += 1
        except:
            number = get_price_selenium(name)
            if number:
                received = True
            else:
                error = True
                time.sleep(0.3)
                counter += 1

    return number


def get_names_from_offers(l, r, link_list):
    offers_list = []
    index = 0
    for l_elem in l:
        r_list = []
        l_list = []
        #print "left_items:"
        l_items = l_elem.find_elements_by_css_selector(".name b")
        for item in l_items:
            inner_html = item.get_attribute("innerHTML")
            #print inner_html
            l_list.append(inner_html)
        #print "___________________"
        #print "right_items:"
        r_items = r[index].find_elements_by_css_selector(".name b")
        for item in r_items:
            inner_html = item.get_attribute("innerHTML")
            #print inner_html
            r_list.append(inner_html)

        #print "___________________"
        offers_list.append([l_list, r_list, link_list[index]])
        index += 1
    return offers_list


def analyse_offers(offers, driver_retriever=None):
    #driver_retriever.get("http://steamcommunity.com/market/search?appid=570")
    #for offer in offers:
    #    print "LEFT:"
    #    for name in offer[0]:
    #        print name, "-- name"
    #    print "RIGHT:"
    #    for name in offer[1]:
    #        print name, "-- name"
    total_income = 0
    for offer in offers:
        total_left = 0
        total_right = 0
        errors = 0
        #print "LEFT:--------------------------------"
        name_pile = ""
        for name in offer[0]:
            name_pile += " " + name
        for name in offer[1]:
            name_pile += " " + name
        name_pile = name_pile.lower()
        if "any" in name_pile or "other" in name_pile or "player card" in name_pile or "offers" in name_pile:
            #print "bad offer..."
            continue

        for name in offer[0]:
            #money_val = get_price_selenium(name)
            money_val = get_price_urllib(name)
            if money_val:
                total_left += money_val
            else:
                errors += 1
        #print "RIGHT:--------------------------------"
        if errors == 0:
            for name in offer[1]:
                #money_val = get_price_selenium(name)
                money_val = get_price_urllib(name)
                if money_val:
                    total_right += money_val
                else:
                    errors += 1

        if errors == 0:
            investment = (total_right + total_left*0.15)
            result = total_left - investment
            if result > 1:
                profit = result/investment*100
                print "***************************************************************"
                if 20 < profit < 200:
                    print "RESULT: ", result,
                    print "LEFT: ", total_left, " RIGHT: ", total_right, '   %loss: ', total_left*0.15
                    print " OFFER LINK: ", offer[2]
                    print "VERY GOOD OFFER, profit: ", profit, "%"
                    print "***************************************************************"
                    total_income += result
                else:
                    #print " OFFER LINK: ", offer[2]
                    #print "mediocre offer, profit: ", profit, "%"
                    print "***************************************************************"
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    print "TOAL INCOME: ", total_income, "!"
    print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
    return 0




#driver_getter = webdriver.Firefox()
#driver_retriever = webdriver.Firefox()
##driver = webdriver.Chrome("http://localhost:9515")
##driver.get("http://www.google.com")
##for n in range(10):
#
#
##driver.get("http://www.python.org")
#for sss in range(60):
#    print "RUN #: ", sss+1
#    driver_getter.get("http://dota2lounge.com/?p=1")
#    l, r, links = get_some_offers(driver_getter)
#    offers = get_names_from_offers(l, r, links)
#    #analyse_offers(offers, driver_retriever)
#    analyse_offers(offers)
#driver_getter.close()
##driver_retriever.close()
##print offers
#



#elem = driver.find_element_by_name("q")
#elem.send_keys(u"Набор карточек игроков (2014)")
#elem.send_keys(Keys.RETURN)
#driver.find_element_by_id("resultlink_0").click()

#driver.close()