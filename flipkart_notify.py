from plyer import notification
from bs4 import BeautifulSoup
import requests
import threading
import time
import winsound

productsTrack = []


def trackPrice(product):
    try:
        r = requests.get(product['product'])

        soup = BeautifulSoup(r.content, 'html5lib')

    except Exception as msg:
        print(msg)
        print("Couldn't get product details")
        print('Restart Process')
        return addProducts()

    productDet = soup.find('div', attrs={'class': 'aMaAEs'})
    product['productName'] = productDet.span.text

    currentPrice = (productDet.find('div', attrs={'class': "_30jeq3 _16Jk6d"})).text
    product['currentPrice'] = currentPrice

    if int(product['currentPrice'][1:].replace(",", "")) <= product['thresholdPrice']:

        sendNotification(product)
        print('Notification Complete')

    else:
        print('Current price of', product['productName'], 'is', product['currentPrice'])


def addProducts():
    try:
        productsTrack.append(
            {'product': input('Enter Product URL : '), 'thresholdPrice': int(input('Enter Threshold Price : '))})
        print(productsTrack)
    except:
        print('Invalid Entry')
    if input('Do you wish to track more products (y/n)? ') in ('y', 'Y'):
        addProducts()


def sendNotification(product):
    winsound.PlaySound('laser.wav', winsound.SND_FILENAME)

    notification.notify(
        title=(product['productName'][:63]) if len(product['productName']) > 64 else product['productName'],
        message='Current Price is ' + product['currentPrice'],
        app_icon='flipkart.ico',
        app_name='Flipkart Notify',
        timeout=1 * 60 * 60,
    )
    print(product['productName'], 'is now available at Rs.', product['currentPrice'][1:].replace(",", ""))


if __name__ == '__main__':

    addProducts()

    while True:
        for item in productsTrack:
            t = threading.Thread(target=trackPrice(item), args=(productsTrack,))

            t.start()
            t.join()
        time.sleep(30)
