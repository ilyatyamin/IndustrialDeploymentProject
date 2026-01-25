import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep
from venv import logger

import requests


def call(method, url, body):
    response = requests.request(
        method=method,
        url=url,
        json=body
    )
    print(f"Request: {method} {url} - Status: {response.status_code}")
    sleep(random.randint(1000, 1500) / 1000.0)


host = 'http://muffin-wallet.com'
types = [
    ('GET', '/v1/muffin-wallets?page=0&size=0', None),
    ('POST', '/v1/muffin-wallets', '''
        {
          "type": "CHOCOLATE",
          "owner_name": "string"
        }
    '''),
    ('GET', '/v1/muffin-wallet/be98f92a-310f-44ea-939c-d1536dd8f1a8', None),
    ('GET', '/v1/muffin-wallets/2a8f5b71-f67f-4b4b-a99c-cf4ffe291907DATAINCORRECT', None),
    ('GET', '/v1/muffin-wallets1111/2a8f5b71-f67f-4b4b-a99c-cf4ffe291907DATAINCORRECT', None),
]

executor = ThreadPoolExecutor(max_workers=60)

futures = []
num = 1500

for i in range(num):
    choice = random.choice(types)
    futures.append(
        executor.submit(call, choice[0], f'{host}{choice[1]}', choice[2])
    )

logger.info("Waiting for all requests to complete...")
completed = 0
failed = 0

for future in as_completed(futures):
    completed += 1
    if completed % 10 == 0:
        logger.info(f"Progress: {completed}/{len(futures)} requests completed")

    try:
        future.result()
    except Exception as e:
        failed += 1
        logger.error(f"Future failed: {str(e)}")