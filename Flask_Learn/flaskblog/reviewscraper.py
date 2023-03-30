# from selenium import webdriver
# from parsel import Selector

# chromedrive_path = "./C:\Program Files\Google\Chrome\Application\chrome.exe" # use the path to the driver you downloaded from previous steps
# driver = webdriver.Chrome(chromedrive_path)

# url = 'https://www.google.com/maps/place/Central+Park+Zoo/@40.7712318,-73.9674707,15z/data=!3m1!5s0x89c259a1e735d943:0xb63f84c661f84258!4m16!1m8!3m7!1s0x89c258faf553cfad:0x8e9cfc7444d8f876!2sTrump+Tower!8m2!3d40.7624284!4d-73.973794!9m1!1b1!3m6!1s0x89c258f1fcd66869:0x65d72e84d91a3f14!8m2!3d40.767778!4d-73.9718335!9m1!1b1?hl=en&hl=en'
# driver.get(url)

# page_content = driver.page_source

# response = Selector(page_content)

# results = []

# for el in response.xpath('//div/div[@data-review-id]/div[contains(@class, "content")]'):
#     results.append({
#         'title': el.xpath('.//div[contains(@class, "title")]/span/text()').extract_first(''),
#         'rating': el.xpath('.//span[contains(@aria-label, "stars")]/@aria-label').extract_first('').replace('stars' ,'').strip(),
#         'body': el.xpath('.//span[contains(@class, "text")]/text()').extract_first(''),
#     })

# print(results)

# driver.quit()

from outscraper import ApiClient


api_cliet = ApiClient(api_key='AIzaSyCs85_IULmdNSTUj21h_m7FK-15Z1F6V4U')
response = api_cliet.google_maps_reviews(
    'https://www.google.com/maps/place/Do+or+Dive+Bar/@40.6867831,-73.9570104,17z/data=!3m2!4b1!5s0x89c25b96a0b10eb9:0xfe4f81ff249e280d!4m5!3m4!1s0x89c25b96a0b30001:0x643d0464b3138078!8m2!3d40.6867791!4d-73.9548217',
    language='en',
    limit=100
)