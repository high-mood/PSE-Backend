import json
import time
import requests
import random
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

class JenkinsCollector(object):
  def collect(self):
    

    with open('test.json') as json_file:
      result = json.load(json_file)

    metric = GaugeMetricFamily(
          'test_job',
          'Python custom exporter test',
          labels=["jobname"])

    for item in result['menu']['items']:
      if item:
        # print(item['id'])
        metric.add_metric([item['id']], random.randint(0, 10), time.time())
        metric.add_metric(['poop'], 1, time.time())
    yield metric

    metric = GaugeMetricFamily(
          'test_job2',
          'Python custom exporter test',
          labels=["jobname"])

    for item in result['menu']['items']:
      if item:
        # print(item['id'])
        metric.add_metric([item['id']+'asdasd'], random.randint(-10, 0), time.time())
        metric.add_metric(['lorem ipsum2'], 5, time.time())
    yield metric



if __name__ == "__main__":
  REGISTRY.register(JenkinsCollector())
  start_http_server(9118)
  i = 0
  while True: 
    i+=1
    print(i)
    # response = requests.get("http://127.0.0.1:9118/api/v1/query", params={'query': 'test_job2'})
    # # results  = response.json()
    # print(response.text)

    time.sleep(1)