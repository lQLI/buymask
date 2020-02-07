# -*- coding=utf-8 -*-
'''
京东抢购口罩程序
'''
import requests
import time
import json
import sys
import random
from bs4 import BeautifulSoup
from log.jdlogger import logger
from jdemail.jdEmail import sendMail
'''
需要修改
'''
# cookie 网页获取
cookies_String = 'unpl=V2_ZzNtbUVSREB9ChVceB9fVWJWG1xKUkVAdAkTVikaXQxgBBUOclRCFnQUR1RnGlQUZwUZXkBcRhFFCEdkeB5fA2AFEFlBZxVLK14bADlNDEY1WnwHBAJfFXYPR1Z6EVgBVzMRXXJXQiV9DERXfBtYBmQzIlpyZ3MTdQhFUEsYbARXQUYBR19DFXJFTlB5GlsHYwARbUNnQA%3d%3d; __jdv=76161171|google-search|t_262767352_googlesearch|cpc|kwd-126030955_0_646d93b9272a4d80947d00d3c208666b|1580289825978; areaId=1; shshshfpa=cab4d538-1df8-8449-975c-7e0f4731f855-1580289828; shshshfpb=yrPAVZoFu%20QdOp3DXNHjAMA%3D%3D; __jdu=953263522; PCSYCityID=CN_110000_110100_110115; pinId=DY-HvY35UiVpKJ-Air2rGbV9-x-f3wj7; pin=503352477-283496; unick=z_binks; _tp=U4v4jO%2BOa72eEyELUQ8FA%2BM%2BfEwNfylRzKirGX8j0E0%3D; _pst=503352477-283496; user-key=fa9abec0-c642-4f82-9821-be44364e7838; ipLoc-djd=1-2810-6501-0.137925768; ipLocation=%u5317%u4eac; cn=6; TrackID=1fXRzG_TcKhQvObWBtVMCzScDugm7rWknVHzHhsTA3jDB_GS0qLQsPh5IcBKlEY4nUGGsKjl1yR5Hv2wDXLkiLc68xJEDT6jxxFKRqlqzf04; ceshi3.com=201; shshshfp=641dd281fbd9ac6cca28336768b100f6; shshshsID=afed28a6042596a7f256be806a2ce60b_17_1581059473604; __jda=122270672.953263522.1580289825.1580289826.1581053720.2; __jdc=122270672; 3AB9D23F7A4B3C9B=YQBXU3IDIGOFVE5I6PFGVAZ4WQX4FYTHPKAE24JMIPAAO3K73XWKCYBPGHNQ27P7MX6RRXQSJESZL6MXM7EJFPTQKQ; __jdb=122270672.68.953263522|2.1581053720; thor=F02DCBE38B3B3E82405687F829D9F8C2CC732DE05395E742D82CE94CC9E66A5D9633FCF68873A15CBEB8160DDBC6AB204EC1D586381026877CCBE2DECB7725CE52D44039939D4C22E271B6CF532D5D2F3BD2D916413A9C023FE0E07B55230DBCE8EA86AB7E505DD61C2222D4427FA73FF175F9D581955D9110EF1E707A74B0F88ADB4C992C319F506F324C1DAC12492B48093D93F4A5D9A1237F3666398A74C6'

# 有货通知 收件邮箱
mail = 'zbinks@126.com'
# 商品的url
url = [
    'https://c0.3.cn/stock?skuId=1835967&area=16_1362_44319_51500&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery1535213',
    'https://c0.3.cn/stock?skuId=1835968&area=16_1362_44319_51500&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery366840',
    'https://c0.3.cn/stock?skuId=1336984&area=16_1362_44319_51500&venderId=1000078145&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery94700',
    'https://c0.3.cn/stock?skuId=65466451629&area=16_1362_44319_51500&venderId=127922&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery8432226',
    'https://c0.3.cn/stock?skuId=7498169&area=16_1362_44319_51500&venderId=1000128491&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery7323892',
    'https://c0.3.cn/stock?skuId=7263128&area=16_1362_44319_51500&venderId=1000128491&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery9621467',
    'https://c0.3.cn/stock?skuId=4061438&area=16_1362_44319_51500&venderId=1000005584&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery620656',
    'https://c0.3.cn/stock?skuId=65421329578&area=16_1362_44319_51500&venderId=593210&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery4952468',
    'https://c0.3.cn/stock?skuId=100005678825&area=16_1362_44319_51500&venderId=1000090691&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery2192795',
    'https://c0.3.cn/stock?skuId=100005294853&area=16_1362_44319_51500&venderId=1000090691&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery8766944',
    'https://c0.3.cn/stock?skuId=45923412989&area=16_1362_44319_51500&venderId=10066244&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery8072251',
    'https://c0.3.cn/stock?skuId=62830056100&area=16_1362_44319_51500&venderId=10066244&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery599501',
    'https://c0.3.cn/stock?skuId=45006657879&area=16_1362_44319_51500&venderId=10066244&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_77a8935fb872d&pduid=526700225&ch=1&callback=jQuery6257903',
    'https://c0.3.cn/stock?skuId=1336984&area=1_72_2799_0&venderId=1000078145&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=1035427354&ch=1&callback=jQuery530569',
    'https://c0.3.cn/stock?skuId=1306182&area=1_72_2799_0&venderId=1000078145&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery6572795',
    'https://c0.3.cn/stock?skuId=2582352&area=1_72_2799_0&venderId=1000078145&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery7637686',
    'https://c0.3.cn/stock?skuId=1835968&area=1_72_2799_0&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery6965677',
    'https://c0.3.cn/stock?skuId=1835967&area=1_72_2799_0&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery3911758',
    'https://c0.3.cn/stock?skuId=3649920&area=1_72_2799_0&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery3239457',
    'https://c0.3.cn/stock?skuId=100011303188&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery6431712',
    'https://c0.3.cn/stock?skuId=4954677&area=1_72_2799_0&venderId=1000084390&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=1615272479_m&pduid=1035427354&ch=1&callback=jQuery9906168',
    'https://c0.3.cn/stock?skuId=65421329578&area=1_72_2799_0&venderId=593210&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery587338',
    'https://c0.3.cn/stock?skuId=100009443324&area=1_72_2799_0&venderId=1000084542&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery1225480',
    'https://c0.3.cn/stock?skuId=100011303176&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery7895873',
    'https://c0.3.cn/stock?skuId=100011303220&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery2336685',
    'https://c0.3.cn/stock?skuId=100011303174&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery4887760',
    'https://c0.3.cn/stock?skuId=100011303172&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery4305892',
    'https://c0.3.cn/stock?skuId=100011303180&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery6552283',
    'https://c0.3.cn/stock?skuId=100011303188&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery6431712',
    'https://c0.3.cn/stock?skuId=100011303190&area=1_72_2799_0&venderId=1000135921&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=&pduid=2102363655&ch=1&callback=jQuery6063461',
    # 'https://c0.3.cn/stock?skuId=1336984&area=19_1607_4773_0&venderId=1000078145&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery6715489',
    # 'https://c0.3.cn/stock?skuId=4642656&area=19_1607_4773_0&venderId=1000006724&buyNum=1&choseSuitSkuIds=&cat=9192,12190,1517&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery4552086',
    # 'https://c0.3.cn/stock?skuId=65466451629&area=19_1607_4773_0&venderId=127922&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery2790674',
    # 'https://c0.3.cn/stock?skuId=65437208345&area=19_1607_4773_0&venderId=127922&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery1749958',
    # 'https://c0.3.cn/stock?skuId=7498169&area=19_1607_4773_0&venderId=1000128491&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=15631231857651045904648&ch=1&callback=jQuery4102801',
    # 'https://c0.3.cn/stock?skuId=7498165&area=19_1607_4773_0&venderId=1000128491&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=15631231857651045904648&ch=1&callback=jQuery9614479',
    'https://c0.3.cn/stock?skuId=7263128&area=19_1607_4773_0&venderId=1000128491&buyNum=1&choseSuitSkuIds=&cat=9855,9858,9924&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=15631231857651045904648&ch=1&callback=jQuery8872960',
    # 'https://c0.3.cn/stock?skuId=1739089&area=19_1607_4773_0&venderId=1000017287&buyNum=1&choseSuitSkuIds=&cat=15248,15250,15278&extraParam={%22originid%22:%221%22}&fqsp=0&pdpin=jd_7c3992aa27d1a&pduid=1580535906442142991701&ch=1&callback=jQuery4479703'
]
'''
备用
'''
timesleep = random.randint(3, 8)

# eid
eid = ''
fp = ''
# 支付密码
payment_pwd = ''

session = requests.session()
session.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Connection": "keep-alive"
}
manual_cookies = {}


def get_tag_value(tag, key='', index=0):
    if key:
        value = tag[index].get(key)
    else:
        value = tag[index].text
    return value.strip(' \t\r\n')


def response_status(resp):
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


for item in cookies_String.split(';'):
    name, value = item.strip().split('=', 1)
    # 用=号分割，分割1次
    manual_cookies[name] = value
    # 为字典cookies添加内容

cookiesJar = requests.utils.cookiejar_from_dict(manual_cookies, cookiejar=None, overwrite=True)
session.cookies = cookiesJar


def validate_cookies():
    for flag in range(1, 3):
        try:
            targetURL = 'https://order.jd.com/center/list.action'
            payload = {
                'rid': str(int(time.time() * 1000)),
            }
            resp = session.get(url=targetURL, params=payload, allow_redirects=False)
            if resp.status_code == requests.codes.OK:
                logger.info('登录成功')
                return True
            else:
                logger.info('第【%s】次请重新获取cookie', flag)
                sendMail(mail,'需要重新登录', True)
                time.sleep(5)
                continue
        except Exception as e:
            logger.info('第【%s】次请重新获取cookie', flag)
            time.sleep(5)
            continue


def getUsername():
    userName_Url = 'https://passport.jd.com/new/helloService.ashx?callback=jQuery339448&_=' + str(
        int(time.time() * 1000))
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://order.jd.com/center/list.action",
        "Connection": "keep-alive"
    }
    resp = session.get(url=userName_Url, allow_redirects=True)
    resultText = resp.text
    resultText = resultText.replace('jQuery339448(', '')
    resultText = resultText.replace(')', '')
    usernameJson = json.loads(resultText)
    logger.info('登录账号名称' + usernameJson['nick'])


'''
检查是否有货
'''


def check_item_stock(itemUrl):
    response = session.get(itemUrl)
    if (response.text.find('无货') > 0):
        return True
    else:
        return False


'''
取消勾选购物车中的所有商品
'''


def cancel_select_all_cart_item():
    url = "https://cart.jd.com/cancelAllItem.action"
    data = {
        't': 0,
        'outSkus': '',
        'random': random.random()
    }
    resp = session.post(url, data=data)
    if resp.status_code != requests.codes.OK:
        print('Status: %u, Url: %s' % (resp.status_code, resp.url))
        return False
    return True


'''
购物车详情
'''


def cart_detail():
    url = 'https://cart.jd.com/cart.action'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://order.jd.com/center/list.action",
        "Host": "cart.jd.com",
        "Connection": "keep-alive"
    }
    resp = session.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    cart_detail = dict()
    for item in soup.find_all(class_='item-item'):
        try:
            sku_id = item['skuid']  # 商品id
        except Exception as e:
            logger.info('购物车中有套装商品，跳过')
            continue
        try:
            # 例如：['increment', '8888', '100001071956', '1', '13', '0', '50067652554']
            # ['increment', '8888', '100002404322', '2', '1', '0']
            item_attr_list = item.find(class_='increment')['id'].split('_')
            p_type = item_attr_list[4]
            promo_id = target_id = item_attr_list[-1] if len(item_attr_list) == 7 else 0

            cart_detail[sku_id] = {
                'name': get_tag_value(item.select('div.p-name a')),  # 商品名称
                'verder_id': item['venderid'],  # 商家id
                'count': int(item['num']),  # 数量
                'unit_price': get_tag_value(item.select('div.p-price strong'))[1:],  # 单价
                'total_price': get_tag_value(item.select('div.p-sum strong'))[1:],  # 总价
                'is_selected': 'item-selected' in item['class'],  # 商品是否被勾选
                'p_type': p_type,
                'target_id': target_id,
                'promo_id': promo_id
            }
        except Exception as e:
            logger.error("商品%s在购物车中的信息无法解析，报错信息: %s，该商品自动忽略", sku_id, e)

    logger.info('购物车信息：%s', cart_detail)
    return cart_detail


'''
修改购物车商品的数量
'''


def change_item_num_in_cart(sku_id, vender_id, num, p_type, target_id, promo_id):
    url = "https://cart.jd.com/changeNum.action"
    data = {
        't': 0,
        'venderId': vender_id,
        'pid': sku_id,
        'pcount': num,
        'ptype': p_type,
        'targetId': target_id,
        'promoID': promo_id,
        'outSkus': '',
        'random': random.random(),
        # 'locationId'
    }
    session.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://cart.jd.com/cart",
        "Connection": "keep-alive"
    }
    resp = session.post(url, data=data)
    return json.loads(resp.text)['sortedWebCartResult']['achieveSevenState'] == 2


'''
添加商品到购物车
'''


def add_item_to_cart(sku_id):
    url = 'https://cart.jd.com/gate.action'
    payload = {
        'pid': sku_id,
        'pcount': 1,
        'ptype': 1,
    }
    resp = session.get(url=url, params=payload)
    if 'https://cart.jd.com/cart.action' in resp.url:  # 套装商品加入购物车后直接跳转到购物车页面
        result = True
    else:  # 普通商品成功加入购物车后会跳转到提示 "商品已成功加入购物车！" 页面
        soup = BeautifulSoup(resp.text, "html.parser")
        result = bool(soup.select('h3.ftx-02'))  # [<h3 class="ftx-02">商品已成功加入购物车！</h3>]

    if result:
        logger.info('%s  已成功加入购物车', sku_id)
    else:
        logger.error('%s 添加到购物车失败', sku_id)


def get_checkout_page_detail():
    """获取订单结算页面信息

    该方法会返回订单结算页面的详细信息：商品名称、价格、数量、库存状态等。

    :return: 结算信息 dict
    """
    url = 'http://trade.jd.com/shopping/order/getOrderInfo.action'
    # url = 'https://cart.jd.com/gotoOrder.action'
    payload = {
        'rid': str(int(time.time() * 1000)),
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "https://cart.jd.com/cart.action",
        "Connection": "keep-alive",
        'Host': 'trade.jd.com',
    }
    try:
        resp = session.get(url=url, params=payload, headers=headers)
        if not response_status(resp):
            logger.error('获取订单结算页信息失败')
            return ''

        soup = BeautifulSoup(resp.text, "html.parser")
        risk_control = get_tag_value(soup.select('input#riskControl'), 'value')

        order_detail = {
            'address': soup.find('span', id='sendAddr').text[5:],  # remove '寄送至： ' from the begin
            'receiver': soup.find('span', id='sendMobile').text[4:],  # remove '收件人:' from the begin
            'total_price': soup.find('span', id='sumPayPriceId').text[1:],  # remove '￥' from the begin
            'items': []
        }

        logger.info("下单信息：%s", order_detail)
        return order_detail
    except requests.exceptions.RequestException as e:
        logger.error('订单结算页面获取异常：%s' % e)
    except Exception as e:
        logger.error('下单页面数据解析异常：%s', e)
    return risk_control


def submit_order(risk_control):
    """提交订单

    重要：
    1.该方法只适用于普通商品的提交订单（即可以加入购物车，然后结算提交订单的商品）
    2.提交订单时，会对购物车中勾选✓的商品进行结算（如果勾选了多个商品，将会提交成一个订单）

    :return: True/False 订单提交结果
    """
    url = 'https://trade.jd.com/shopping/order/submitOrder.action'
    # js function of submit order is included in https://trade.jd.com/shopping/misc/js/order.js?r=2018070403091

    # overseaPurchaseCookies:
    # vendorRemarks: []
    # submitOrderParam.sopNotPutInvoice: false
    # submitOrderParam.trackID: TestTrackId
    # submitOrderParam.ignorePriceChange: 0
    # submitOrderParam.btSupport: 0
    # riskControl:
    # submitOrderParam.isBestCoupon: 1
    # submitOrderParam.jxj: 1
    # submitOrderParam.trackId:

    data = {
        'overseaPurchaseCookies': '',
        'vendorRemarks': '[]',
        'submitOrderParam.sopNotPutInvoice': 'false',
        'submitOrderParam.trackID': 'TestTrackId',
        'submitOrderParam.ignorePriceChange': '0',
        'submitOrderParam.btSupport': '0',
        'riskControl': risk_control,
        'submitOrderParam.isBestCoupon': 1,
        'submitOrderParam.jxj': 1,
        'submitOrderParam.trackId': '9643cbd55bbbe103eef18a213e069eb0',  # Todo: need to get trackId
        # 'submitOrderParam.eid': eid,
        # 'submitOrderParam.fp': fp,
        'submitOrderParam.needCheck': 1,
    }

    def encrypt_payment_pwd(payment_pwd):
        return ''.join(['u3' + x for x in payment_pwd])

    if len(payment_pwd) > 0:
        data['submitOrderParam.payPassword'] = encrypt_payment_pwd(payment_pwd)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
        "Connection": "keep-alive",
        'Host': 'trade.jd.com',
    }

    try:
        resp = session.post(url=url, data=data, headers=headers)
        resp_json = json.loads(resp.text)

        # 返回信息示例：
        # 下单失败
        # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60123, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '请输入支付密码！'}
        # {'overSea': False, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'orderXml': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60017, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '您多次提交过快，请稍后再试'}
        # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 60077, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': '获取用户订单信息失败'}
        # {"cartXml":null,"noStockSkuIds":"xxx","reqInfo":null,"hasJxj":false,"addedServiceList":null,"overSea":false,"orderXml":null,"sign":null,"pin":"xxx","needCheckCode":false,"success":false,"resultCode":600157,"orderId":0,"submitSkuNum":0,"deductMoneyFlag":0,"goJumpOrderCenter":false,"payInfo":null,"scaleSkuInfoListVO":null,"purchaseSkuInfoListVO":null,"noSupportHomeServiceSkuList":null,"msgMobile":null,"addressVO":{"pin":"xxx","areaName":"","provinceId":xx,"cityId":xx,"countyId":xx,"townId":xx,"paymentId":0,"selected":false,"addressDetail":"xx","mobile":"xx","idCard":"","phone":null,"email":null,"selfPickMobile":null,"selfPickPhone":null,"provinceName":null,"cityName":null,"countyName":null,"townName":null,"giftSenderConsigneeName":null,"giftSenderConsigneeMobile":null,"gcLat":0.0,"gcLng":0.0,"coord_type":0,"longitude":0.0,"latitude":0.0,"selfPickOptimize":0,"consigneeId":0,"selectedAddressType":0,"siteType":0,"helpMessage":null,"tipInfo":null,"cabinetAvailable":true,"limitKeyword":0,"specialRemark":null,"siteProvinceId":0,"siteCityId":0,"siteCountyId":0,"siteTownId":0,"skuSupported":false,"addressSupported":0,"isCod":0,"consigneeName":null,"pickVOname":null,"shipmentType":0,"retTag":0,"tagSource":0,"userDefinedTag":null,"newProvinceId":0,"newCityId":0,"newCountyId":0,"newTownId":0,"newProvinceName":null,"newCityName":null,"newCountyName":null,"newTownName":null,"checkLevel":0,"optimizePickID":0,"pickType":0,"dataSign":0,"overseas":0,"areaCode":null,"nameCode":null,"appSelfPickAddress":0,"associatePickId":0,"associateAddressId":0,"appId":null,"encryptText":null,"certNum":null,"used":false,"oldAddress":false,"mapping":false,"addressType":0,"fullAddress":"xxxx","postCode":null,"addressDefault":false,"addressName":null,"selfPickAddressShuntFlag":0,"pickId":0,"pickName":null,"pickVOselected":false,"mapUrl":null,"branchId":0,"canSelected":false,"address":null,"name":"xxx","message":null,"id":0},"msgUuid":null,"message":"xxxxxx商品无货"}
        # {'orderXml': None, 'overSea': False, 'noStockSkuIds': 'xxx', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'cartXml': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': False, 'resultCode': 600158, 'orderId': 0, 'submitSkuNum': 0, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': {'oldAddress': False, 'mapping': False, 'pin': 'xxx', 'areaName': '', 'provinceId': xx, 'cityId': xx, 'countyId': xx, 'townId': xx, 'paymentId': 0, 'selected': False, 'addressDetail': 'xxxx', 'mobile': 'xxxx', 'idCard': '', 'phone': None, 'email': None, 'selfPickMobile': None, 'selfPickPhone': None, 'provinceName': None, 'cityName': None, 'countyName': None, 'townName': None, 'giftSenderConsigneeName': None, 'giftSenderConsigneeMobile': None, 'gcLat': 0.0, 'gcLng': 0.0, 'coord_type': 0, 'longitude': 0.0, 'latitude': 0.0, 'selfPickOptimize': 0, 'consigneeId': 0, 'selectedAddressType': 0, 'newCityName': None, 'newCountyName': None, 'newTownName': None, 'checkLevel': 0, 'optimizePickID': 0, 'pickType': 0, 'dataSign': 0, 'overseas': 0, 'areaCode': None, 'nameCode': None, 'appSelfPickAddress': 0, 'associatePickId': 0, 'associateAddressId': 0, 'appId': None, 'encryptText': None, 'certNum': None, 'addressType': 0, 'fullAddress': 'xxxx', 'postCode': None, 'addressDefault': False, 'addressName': None, 'selfPickAddressShuntFlag': 0, 'pickId': 0, 'pickName': None, 'pickVOselected': False, 'mapUrl': None, 'branchId': 0, 'canSelected': False, 'siteType': 0, 'helpMessage': None, 'tipInfo': None, 'cabinetAvailable': True, 'limitKeyword': 0, 'specialRemark': None, 'siteProvinceId': 0, 'siteCityId': 0, 'siteCountyId': 0, 'siteTownId': 0, 'skuSupported': False, 'addressSupported': 0, 'isCod': 0, 'consigneeName': None, 'pickVOname': None, 'shipmentType': 0, 'retTag': 0, 'tagSource': 0, 'userDefinedTag': None, 'newProvinceId': 0, 'newCityId': 0, 'newCountyId': 0, 'newTownId': 0, 'newProvinceName': None, 'used': False, 'address': None, 'name': 'xx', 'message': None, 'id': 0}, 'msgUuid': None, 'message': 'xxxxxx商品无货'}
        # 下单成功
        # {'overSea': False, 'orderXml': None, 'cartXml': None, 'noStockSkuIds': '', 'reqInfo': None, 'hasJxj': False, 'addedServiceList': None, 'sign': None, 'pin': 'xxx', 'needCheckCode': False, 'success': True, 'resultCode': 0, 'orderId': 8740xxxxx, 'submitSkuNum': 1, 'deductMoneyFlag': 0, 'goJumpOrderCenter': False, 'payInfo': None, 'scaleSkuInfoListVO': None, 'purchaseSkuInfoListVO': None, 'noSupportHomeServiceSkuList': None, 'msgMobile': None, 'addressVO': None, 'msgUuid': None, 'message': None}

        if resp_json.get('success'):
            logger.info('订单提交成功! 订单号：%s', resp_json.get('orderId'))
            return True
        else:
            message, result_code = resp_json.get('message'), resp_json.get('resultCode')
            if result_code == 0:
                # self._save_invoice()
                message = message + '(下单商品可能为第三方商品，将切换为普通发票进行尝试)'
            elif result_code == 60077:
                message = message + '(可能是购物车为空 或 未勾选购物车中商品)'
            elif result_code == 60123:
                message = message + '(需要在payment_pwd参数配置支付密码)'
            logger.info('订单提交失败, 错误码：%s, 返回信息：%s', result_code, message)
            logger.info(resp_json)
            return False
    except Exception as e:
        logger.error(e)
        return False


'''

'''


def item_removed(sku_id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Referer": "http://trade.jd.com/shopping/order/getOrderInfo.action",
        "Connection": "keep-alive",
        'Host': 'item.jd.com',
    }
    url = 'https://item.jd.com/{}.html'.format(sku_id)
    page = requests.get(url=url, headers=headers)
    return '该商品已下柜' not in page.text


'''
购买环节
测试三次
'''


def buyMask(sku_id):
    for count in range(1, 2):
        logger.info('第[%s/%s]次尝试提交订单', count, 3)
        cancel_select_all_cart_item()
        cart = cart_detail()
        if sku_id in cart:
            logger.info('%s 已在购物车中，调整数量为 %s', sku_id, 1)
            cart_item = cart.get(sku_id)
            change_item_num_in_cart(
                sku_id=sku_id,
                vender_id=cart_item.get('vender_id'),
                num=1,
                p_type=cart_item.get('p_type'),
                target_id=cart_item.get('target_id'),
                promo_id=cart_item.get('promo_id')
            )
        else:
            add_item_to_cart(sku_id)
        risk_control = get_checkout_page_detail()
        if len(risk_control) > 0:
            if submit_order(risk_control):
                return True
        logger.info('休息%ss', 3)
        time.sleep(3)
    else:
        logger.info('执行结束，提交订单失败！')
        return False


flag = 1
while (1):
    try:
        if flag == 1:
            validate_cookies()
            getUsername()
        checkSession = requests.Session()
        checkSession.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/531.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Connection": "keep-alive"
        }
        logger.info('第' + str(flag) + '次 ')
        flag += 1
        for i in url:
            # 商品url
            skuId = i.split('skuId=')[1].split('&')[0]
            skuidUrl = 'https://item.jd.com/' + skuId + '.html'
            response = checkSession.get(i)
            if (response.text.find('无货') > 0):
                logger.info('[%s]类型口罩无货', skuId)
            else:
                if item_removed(skuId):
                    logger.info('[%s]类型口罩有货啦!马上下单', skuId)
                    if buyMask(skuId):
                        sendMail(mail,skuidUrl, True)
                    else:
                        sendMail(mail,skuidUrl, False)
                else:
                    logger.info('[%s]类型口罩有货，但已下柜商品', skuId)
        time.sleep(timesleep)
        if flag % 20 == 0:
            logger.info('校验是否还在登录')
            validate_cookies()
    except Exception as e:
        import traceback

        print(traceback.format_exc())
        time.sleep(10)
