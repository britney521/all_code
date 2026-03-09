# import cloudscraper
# scraper = cloudscraper.create_scraper()
# url = 'https://steamdb.info/app/730/charts/#max'
# res = scraper.get(url)
# print("============scraper的方式", res.status_code, res.cookies, res.text)


from curl_cffi import requests as cffi_requests
res = cffi_requests.get("https://steamdb.info/app/730/charts/#max", impersonate='chrome110', timeout=10)
print("============cffi_requests的方式", res.status_code, res.cookies, res.text)