# pip install pycryptodome   需要模块加密方面的模块

from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from urllib.parse import quote_plus
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from base64 import decodebytes, encodebytes

import json
import requests


class AliPay(object):
    """
    支付宝支付接口
    """

    def __init__(self) -> None:
        super().__init__()

    # def __init__(self, appid, app_notify_url, app_private_key_path,
    #              alipay_public_key_path, return_url, debug=False):
    #     self.appid = appid
    #     self.app_notify_url = app_notify_url
    #     self.app_private_key_path = app_private_key_path
    #     self.app_private_key = None
    #     self.return_url = return_url
    #     with open(self.app_private_key_path) as fp:
    #         self.app_private_key = RSA.importKey(fp.read())

    #     self.alipay_public_key_path = alipay_public_key_path
    #     with open(self.alipay_public_key_path) as fp:
    #         self.alipay_public_key = RSA.import_key(fp.read())

    #     if debug is True:
    #         self.__gateway = "https://openapi.alipaydev.com/gateway.do"
    #     else:
    #         self.__gateway = "https://openapi.alipay.com/gateway.do"

    def init_app(self, app) -> None:
        self.app = app

    def _rebuild_params(self):
        pstr = '-----BEGIN PRIVATE KEY-----\n{}\n-----END PRIVATE KEY-----'
        self.appid = self.app.config['ALIPAY_APPID']
        self.app_private_key = RSA.importKey(pstr.format(self.app.config['ALIPAY_PRIVATE_KEY']))
        self.alipay_public_key = RSA.importKey(pstr.format(self.app.config['ALIPAY_PUBLIC_KEY']))
        self.debug = self.app.config['ALIPAY_DEBUG']
        self.app_notify_url = self.app.config['ALIPAY_NOTIFY_URL']
        if self.debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def build_trade_precreate_url(self, subject, out_trade_no, total_amount, **kwargs):
        """
        当面付预创建订单url
        """
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            # "qr_code_timeout_express": '5m',
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.precreate", biz_content)
        qs = self.sign_data(data)
        url = self.__gateway + '?' + qs
        return url

    def trade_precreate_qrcode_str(self, subject, out_trade_no, total_amount, **kwargs) -> str:
        """
        获取当面付订单二维码内容
        """
        self._rebuild_params()
        url = self.build_trade_precreate_url(subject=subject, out_trade_no=out_trade_no, total_amount=total_amount)
        resp = requests.get(url, timeout=5)
        body_dict = json.loads(resp.text)
        ali_resp = body_dict['alipay_trade_precreate_response']
        if ali_resp['code'] == '10000':
            return ali_resp['qr_code']
        return ''

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY",
            # "qr_pay_mode":4
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, self.return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["return_url"] = self.return_url
        if self.app_notify_url is not None:
            data["notify_url"] = self.app_notify_url
        return data

    def _build_sign_params(self, params: dict) -> None:
        params.pop('sign', None)
        unsigned_items = self.ordered_data(params)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        params['sign'] = sign

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        unsigned_string = "&".join("{0}={1}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string.encode("utf-8"))
        ordered_items = self.ordered_data(data)
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in ordered_items)

        # 获得最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64 编码，转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def _verify(self, raw_content, signature):
        # 开始计算签名
        key = self.alipay_public_key
        signer = PKCS1_v1_5.new(key)
        digest = SHA256.new()
        digest.update(raw_content.encode("utf8"))
        if signer.verify(digest, decodebytes(signature.encode("utf8"))):
            return True
        return False

    def verify(self, data, signature):
        if "sign_type" in data:
            sign_type = data.pop("sign_type")
        # 排序后的字符串
        unsigned_items = self.ordered_data(data)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)


if __name__ == "__main__":
    """支付请求过程"""
    # 传递参数初始化支付类
    alipay = AliPay(
        appid="2021000117636514",  # 设置签约的appid
        app_notify_url="http://projectsedus.com/",  # 异步支付通知url
        app_private_key_path='应用私钥_RSA2_PKCS1.txt',  # 设置应用私钥
        alipay_public_key_path="支付宝公钥.txt",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        debug=True,  # 默认False,                                   # 设置是否是沙箱环境，True是沙箱环境
        return_url="http://47.92.87.172:8000/"  # 同步支付通知url
    )

    # 传递参数执行支付类里的direct_pay方法，返回签名后的支付参数，
    # url = alipay.direct_pay(
    #     subject="测试订单",                              # 订单名称
    #     # 订单号生成，一般是当前时间(精确到秒)+用户ID+随机数
    #     out_trade_no="201702021225",                    # 订单号
    #     total_amount=100,                               # 支付金额
    #     return_url="http://47.92.87.172:8000/"          # 支付成功后，跳转url
    # )

    # 将前面后的支付参数，拼接到支付网关
    # 注意：下面支付网关是沙箱环境，
    # re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    # print(re_url)
    # 最终进行签名后组合成支付宝的url请求
    url = alipay.build_trade_precreate_url(subject='测试', out_trade_no='20210414002', total_amount=0.01)
    print(url)
    resp = requests.get(url)
    body_dict = json.loads(resp.text)
    print(body_dict)
    ali_resp = body_dict['alipay_trade_precreate_response']
    if ali_resp['code'] == '10000':
        print(ali_resp['qr_code'])
