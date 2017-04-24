#!/Users/samburrell/anaconda/bin/python
import requests
import json

url = '192.168.56.101:6800'
project = 'news_crawler'

spiders = json.loads(requests.get('http://%s/listspiders.json?project=%s' % (url,project)).text)['spiders']

for spider in spiders:
     job = requests.post('http://%s/schedule.json'%(url), data = {'project':project, 'spider':spider})
     print(job.text)
