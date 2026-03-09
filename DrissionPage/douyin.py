import requests
from DrissionPage import ChromiumOptions, ChromiumPage,errors

url = input('请输入url链接：')

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': '__ac_nonce=06704ee9c00dc0896c1c4; __ac_signature=_02B4Z6wo00f01ZoYHyAAAIDAtJ.SCZhi3wmaOBuAAAGD41; ttwid=1%7CQOARiqe_5zZTIIVl277yMaXpLZ-f-nLI5q5UHh-c4aw%7C1728376476%7C33bada904b025c528adfa5205cba9dfa73c2d08db4ebe9cbab6baf78e0c5a5da; UIFID_TEMP=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457bcd52853fda0d2485ba4023d8a3f047d2cec3b4e60316bfa6dcaeef4acfa3b2382bb1d7050952e8edaeb2c91ffc6c99c4; s_v_web_id=verify_m206q8u5_8LjuJMZY_goOu_49fq_8dJX_gTAwdfDBSRP5; hevc_supported=true; dy_swidth=1536; dy_sheight=960; strategyABtestKey=%221728376478.007%22; fpk1=U2FsdGVkX1+i5pnWtTGgKmSikgsxKsPpfuvfMIiv8tPufGkxUhpOrUcd15cv++BXXamSv5HkpMFlzJlNgV9Y7w==; fpk2=16453d6e2683b8800ded2a27c7f595d9; passport_csrf_token=085360adee522242d5ead4bef31857ce; passport_csrf_token_default=085360adee522242d5ead4bef31857ce; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Atrue%2C%22volume%22%3A0.5%7D; FORCE_LOGIN=%7B%22videoConsumedRemainSeconds%22%3A180%7D; bd_ticket_guard_client_web_domain=2; UIFID=60b2ef133e5e740633c50bb923c1ddfcacd13dfeee1bbba287269d01840b457bcd52853fda0d2485ba4023d8a3f047d20d56a2feb0c0ec7e9cfd91d70a306fec7aba616b366245e73f065a77107c240515abecf9890030c14dc4ecf08a661171ba102a4aa0eea78070a493228e370f53cf9e5f3584bca380494151aca76a54b98df4bfaca760873cf6fbda5369dbe70ae2b2e452f33df255964fea625dccac55; passport_mfa_token=Cjez4dnHOdeZKTrakbH8sxRbHGniafubiWRdB2K7fZRS62KO5Pi2VWIn2KBhkT8%2Bu5QSd77iykZsGkoKPI5HKQeh4X7GW14F%2BOHuSSzqhVAcRaro11j4N9osKK2i%2BvJYljISh4t35yxt%2BIxx8%2FlQSTW%2B9OTklQORiBDBmN4NGPax0WwgAiIBAwvpTkE%3D; d_ticket=22e9100a87dce13445f582d9dc2f7f6d81224; passport_assist_user=CkDeW84iXwvKnQQ6FwQ12-f-0FRx6Rfo3J94NhIxGaIdGo2D05vtLtXTAo-rtQZr2stdKhv9XB7AYleB6Zy6Pp-SGkoKPCwdpAH4shD_rZKlXX-7wXEQssT55saCF0nmHUJNorQJQGtOowyPRoMBKz07Sl2SXr7GYA67F4rcgdlb4RC8lt4NGImv1lQgASIBA0STnAA%3D; n_mh=bRj9wnCvlvHfr9DpEUKfAcD0xW7we8zJIPyvFO-2KJs; sso_uid_tt=33d27f16e8ce22e008d67c83dfb25b5e; sso_uid_tt_ss=33d27f16e8ce22e008d67c83dfb25b5e; toutiao_sso_user=781a61728ceacec0ab7109074bfefa85; toutiao_sso_user_ss=781a61728ceacec0ab7109074bfefa85; sid_ucp_sso_v1=1.0.0-KGJmNmJkMWMzZTIwY2YyZmQwZWVjMjlhNmNlNWY1NTI2NjEzMzZlNGQKIQi-1pDW6PWhARCI3pO4BhjvMSAMMPvYovcFOAZA9AdIBhoCbHEiIDc4MWE2MTcyOGNlYWNlYzBhYjcxMDkwNzRiZmVmYTg1; ssid_ucp_sso_v1=1.0.0-KGJmNmJkMWMzZTIwY2YyZmQwZWVjMjlhNmNlNWY1NTI2NjEzMzZlNGQKIQi-1pDW6PWhARCI3pO4BhjvMSAMMPvYovcFOAZA9AdIBhoCbHEiIDc4MWE2MTcyOGNlYWNlYzBhYjcxMDkwNzRiZmVmYTg1; passport_auth_status=97eef15d6f51976d0d0f0de0b0774cdd%2C; passport_auth_status_ss=97eef15d6f51976d0d0f0de0b0774cdd%2C; uid_tt=42aa40aa9c9e88bc62b49f363ec52584; uid_tt_ss=42aa40aa9c9e88bc62b49f363ec52584; sid_tt=2bb8d99817b7780c1b073228d7a63963; sessionid=2bb8d99817b7780c1b073228d7a63963; sessionid_ss=2bb8d99817b7780c1b073228d7a63963; is_staff_user=false; SelfTabRedDotControl=%5B%5D; publish_badge_show_info=%220%2C0%2C0%2C1728376589025%22; _bd_ticket_crypt_doamin=2; _bd_ticket_crypt_cookie=068892eca62b130d62e3cc132aa9f19d; __security_server_data_status=1; sid_guard=2bb8d99817b7780c1b073228d7a63963%7C1728376590%7C5183997%7CSat%2C+07-Dec-2024+08%3A36%3A27+GMT; sid_ucp_v1=1.0.0-KDU1YTA0NTU2NDRlNTE1ZGQ5YWJjYjM3NjFmZTlmOGMxY2ZlODNlMDAKGwi-1pDW6PWhARCO3pO4BhjvMSAMOAZA9AdIBBoCbHEiIDJiYjhkOTk4MTdiNzc4MGMxYjA3MzIyOGQ3YTYzOTYz; ssid_ucp_v1=1.0.0-KDU1YTA0NTU2NDRlNTE1ZGQ5YWJjYjM3NjFmZTlmOGMxY2ZlODNlMDAKGwi-1pDW6PWhARCO3pO4BhjvMSAMOAZA9AdIBBoCbHEiIDJiYjhkOTk4MTdiNzc4MGMxYjA3MzIyOGQ3YTYzOTYz; csrf_session_id=4c090355bf90c3516c6c25f23831188b; download_guide=%223%2F20241008%2F0%22; FOLLOW_NUMBER_YELLOW_POINT_INFO=%22MS4wLjABAAAAQOTYFIrBBtsOSBKNGI6Jh90gdhL5OaDYrT_iXKfJ1XQ%2F1728403200000%2F0%2F1728377038204%2F0%22; pwa2=%220%7C0%7C1%7C0%22; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1536%2C%5C%22screen_height%5C%22%3A960%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A12%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A50%7D%22; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAAQOTYFIrBBtsOSBKNGI6Jh90gdhL5OaDYrT_iXKfJ1XQ%2F1728403200000%2F0%2F0%2F1728378051674%22; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWl0ZXJhdGlvbi12ZXJzaW9uIjoxLCJiZC10aWNrZXQtZ3VhcmQtcmVlLXB1YmxpYy1rZXkiOiJCR2dodmVReU9qbHdqZTY4SU5lNVdFREo5d3BoMTl2LzZYSTJJeEg1MlEvN2syd3FpdjU0TkhjRGpCd2ZMZUZrVlg2RUoxbUhOY0NlaDdjdHU5aGgwWTQ9IiwiYmQtdGlja2V0LWd1YXJkLXdlYi12ZXJzaW9uIjoyfQ%3D%3D; passport_fe_beating_status=true; odin_tt=86c97747c2e640970239b7576d4ff7aca48cb6d9215ac585c322db47323bf9f50073b582e54bdab0690b1d1c7648d01f; home_can_add_dy_2_desktop=%221%22; IsDouyinActive=false',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.douyin.com/video/7398484837599939877',
    'sec-ch-ua': '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}
co = ChromiumOptions()
page = ChromiumPage(co)
page.get(url)

page.listen.start('aweme/detail')
data_packet = page.listen.wait()  # 等待并获取一个数据包
print(data_packet)  # 打印数据包url
response = requests.get(data_packet.url, headers=headers)

# print(response.text)
data = response.json()
desc = data['aweme_detail']['desc'].replace("\n", "")
playurl = data['aweme_detail']['video']['play_addr_h264']['url_list'][0]
print('desc:', desc, 'playurl:', playurl)
response = requests.get(playurl, headers=headers)
f = open(f'video/{desc}.mp4','wb')
f.write(response.content)
page.quit()
