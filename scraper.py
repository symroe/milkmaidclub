import re
import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urllib2

import icalendar
from datetime import datetime, timedelta

urls = (
    'http://www.milkmaidmusic.co.uk/futuregigs.html',
    'http://www.milkmaidmusic.co.uk/futuregigs2.html',
    )

cal = icalendar.Calendar()
cal.add('prodid', '-//Milk Made Club Events//mxm.dk//')
cal.add('version', '2.0')
    
for page, url in enumerate(urls):
    rows = {}
    req = urllib2.urlopen(url)
    soup = BeautifulSoup.BeautifulSoup(req, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

    for cell in soup.findAll(id=re.compile('table_')):
        row_id = cell['id'].split('_')[1]
        if not rows.get(row_id):
            rows[row_id] = []

        rows[row_id].append(cell)


    for k,row in rows.items():
        date = row[1].find('span').text
        date = date + ' %s 19:30' % datetime.now().year
        date = re.sub("[\d]{1,2}st|nd|rd|th", '', date).strip()
        try:
            date = datetime.strptime(date, "%d %b %Y %H:%M")
        except Exception, e:
            continue


        event = icalendar.Event()
        for i in range(2,6):
            try:
                row[i] = u"%s" % row[i].find('span').text
            except:
                row.append('')
        
        summary = """
%s
Supporters: %s
Members: %s
Non-Members: %s
        """ % (row[2],
            row[3],
            row[4],
            row[5],
            )
        
        
        
        event.add('summary', summary)
        event.add('dtstart', date)
        event.add('dtend', date + timedelta(hours=3))
        cal.add_component(event)
x = open('cal.ics', 'w')
x.write(cal.as_string())

    
    
    
    
    
    