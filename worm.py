# 20180314, rwang
from pyquery import PyQuery as pq
import requests
import csv
import sys

# encoding Utf-8
reload(sys)
sys.setdefaultencoding("Utf-8")

# creat csvfile
csvfile = file('info.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['Date', 'City', 'Firma', 'Branchen', 'URL'])

# get treffer number
url = 'http://www.expodatabase.de/aussteller/messen/index.php?i_cockpitfromdate=1.4.2018&i_cockpittodate=31.10.2018&none=9545&none=350000&i_besucherselect=1&i_timeselect=1&i_messetyp%5B%5D=1&i_messetyp%5B%5D=2&i_messetyp%5B%5D=3&i_messetyp%5B%5D=4&i_cpid=1598&i_cockpitkeywo=Deutschland&i_cockpitkeyfindwo=2&i_cockpitkeyfindart=1&i_nettost=&i_nettoen=&i_austellerst=&i_austelleren=&i_besucherst=12727&i_besucheren=350000&go.x=15&go.y=6&go=go'
html = pq(requests.get(url).text)
treffer = html('.search_result_head_treffer').text()
print 'Treffer number = ' + treffer + '.'

# init rowNumber counter
rowNumber = 0

for i in range(1, 8):
    # request html
    if i > 1:
        url = 'http://www.expodatabase.de/aussteller/messen/index.php?OK=1&sortierid=0&maxPerPage=20&i_cockpitfromdate=1.4.2018&i_cockpittodate=31.10.2018&i_besucherst=12727&i_besucheren=350000&i_besucherselect=1&i_timeselect=1&i_messetyp%5B0%5D=1&i_messetyp%5B1%5D=2&i_messetyp%5B2%5D=3&i_messetyp%5B3%5D=4&i_cpid=1598&i_cockpitkeywo=Deutschland&i_cockpitkeyfindwo=2&i_cockpitkeyfindart=1&currPage=' + str(i)
    print 'Requesting page ' + str(i) + ', url = ' + url + '.'
    html = pq(requests.get(url).text)

    # filter and save
    for j in range(0, len(html('tr'))):
        urlOut = 'http://www.expodatabase.de/aussteller/messen/' + str(html('tr').eq(j).find('.firma').find('a').attr('href'))
        firma = html('tr').eq(j).find('.firma').find('a').removeAttr('href').text()
        html('tr').eq(j).find('.branchen').find('strong').remove()
        branchen = html('tr').eq(j).find('.branchen').text()
        if firma:
            writer.writerow([html('tr').eq(j).find('.date').text(), html('tr').eq(j).find('.city').text(), firma, branchen, urlOut])
            rowNumber += 1

print 'Done. Got ' + str(rowNumber) + ' rows. Treffer number = ' + treffer + '.'
csvfile.close()