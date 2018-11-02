# coding: utf-8
import csv

if __name__ == '__main__':
    head = ['sku', 'title', 'comment', 'price', 'info', 'manmanbuy']
    last = open('./last.csv', 'a+', newline='', encoding='utf-8')

    egg = open('./egg.csv', newline='')

    ereader = csv.DictReader(egg)
    last_writer = csv.DictWriter(last, head)

    last_writer.writeheader()

    for ei, edic in enumerate(ereader):
        print(ei,end="\r")
        sku = edic.get('sku')
        title = edic.get('title')
        comment = edic.get('comment')
        price = edic.get('price')
        manmanbuy = '-'
        info = ''
        with open('./history.csv', newline='', encoding='utf-8') as history:
            hreader = csv.DictReader(history)
            for hi, hdic in enumerate(hreader):
                hsku = hdic.get('sku')
                if hsku == sku:
                    man = hdic.get('manmanbuy')
                    if man != "验证码":
                        manmanbuy = man
                    break
        with open('./des.csv', newline='', encoding='utf-8') as des:
            dreader = csv.DictReader(des)
            for di, ddic in enumerate(dreader):
                dsku = ddic.get('sku')
                if dsku == sku:
                    info = ddic.get('attrs')
                    break
        last_writer.writerow({'sku': sku, 'title': title, 'comment': comment,
                              'price': price, 'manmanbuy': manmanbuy, 'info': info})

    egg.close()
    des.close()
    history.close()
    last.close()
