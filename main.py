#test 01
import os
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *
import requests
import websocket
import json
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

app = Flask(__name__)
# Channel Access Token    '''需要修改成自己的'''
line_bot_api = LineBotApi(
    '1CPlEAnl0ofyWrpLbLvfZlparn3AzIfrSxvG0Zkrkhfu9YWaEprCdAki1UzDXBtSEJwIrQpIt5bH+CW4s8f+bXsmTfbDzRGtzjaxpgb6RzCwh7iW46LrKCMMjymEjP/4qtcbjgTTQBs4AJCbGPZPrgdB04t89/1O/w1cDnyilFU='
)  #回傳Json資料使用的

# Channel Secret  '''需要修改成自己的'''
handler = WebhookHandler('96858ee049f70b4757ee556058306d10')  #接收到資料解碼

cities = ["臺北", "新北", "桃園", "臺中", "臺南", "高雄", "基隆", "新竹", "嘉義"]  # 市
counties = [
    "苗栗", "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江"
]  # 縣


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print(event.message.text)
    user_id = event.source.user_id  # 取得使用者uid
    '''import random
    flag = random.randint(0, 9)
    if flag == 1:
      print("中獎")
      line_bot_api.push_message(user_id, TextSendMessage(text='Page changed!\n'+str('推播測試')))
    else:
      pass'''

    city = event.message.text[:2]
    city = city.replace('台', '臺')  # 氣象局資料使用「臺」
    if city in cities:  # 加上「市」
        city += '市'
        message = TextSendMessage(str("正在為您查詢「" + str(city) + "」的資料請稍候..."))
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif city in counties:  # 加上「縣」
        city += '縣'
        message = TextSendMessage(str("正在為您查詢「" + str(city) + "」的資料請稍候..."))
        line_bot_api.reply_message(event.reply_token, message)
        return 0

    if event.message.text == "天氣狀況":
        contents = {
            "type": "bubble",
            "direction": "ltr",
            "hero": {
                "type": "image",
                "url":
                "https://img-fnc.ebc.net.tw/EbcFnc/news/2018/08/01/1533127075_45838.jpg",
                "size": "full",
                "aspectRatio": "16:9",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "label": "Action",
                    "uri": "https://www.greenadvocates.org.tw/sky/index/"
                }
            },
            "body": {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "md",
                "backgroundColor":
                "#FFFFFFFF",
                "contents": [{
                    "type": "text",
                    "text": "你想要查詢哪個縣市",
                    "weight": "bold",
                    "size": "lg",
                    "align": "start",
                    "contents": []
                }, {
                    "type": "separator",
                    "color": "#413939"
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "基隆市",
                            "text": "基隆市",
                            "data": "基隆市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "臺北市",
                            "text": "臺北市",
                            "data": "臺北市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "新北市",
                            "text": "新北市",
                            "data": "新北市"
                        },
                        "style": "primary"
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "桃園市",
                            "text": "桃園市",
                            "data": "桃園市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "新竹市",
                            "text": "新竹市",
                            "data": "新竹市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "苗栗縣",
                            "text": "苗栗縣",
                            "data": "苗栗縣"
                        },
                        "style": "primary"
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "臺中市",
                            "text": "臺中市",
                            "data": "臺中市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "彰化縣",
                            "text": "彰化縣",
                            "data": "彰化縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "南投縣",
                            "text": "南投縣",
                            "data": "南投縣"
                        },
                        "style": "primary"
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "雲林縣",
                            "text": "雲林縣",
                            "data": "雲林縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "嘉義縣",
                            "text": "嘉義縣",
                            "data": "嘉義縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "台南市",
                            "text": "台南市",
                            "data": "台南市"
                        },
                        "style": "primary"
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "高雄市",
                            "text": "高雄市",
                            "data": "高雄市"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "屏東縣",
                            "text": "屏東縣",
                            "data": "屏東縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "澎湖縣",
                            "text": "澎湖縣",
                            "data": "澎湖縣"
                        },
                        "style": "primary"
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "spacing":
                    "md",
                    "contents": [{
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "金門縣",
                            "text": "金門縣",
                            "data": "金門縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "連江縣",
                            "text": "連江縣",
                            "data": "連江縣"
                        },
                        "style": "primary"
                    }, {
                        "type": "button",
                        "action": {
                            "type": "postback",
                            "label": "綠島鄉",
                            "text": "綠島鄉",
                            "data": "綠島鄉"
                        },
                        "style": "primary"
                    }]
                }]
            },
            "styles": {
                "body": {
                    "backgroundColor": "#F8F2A6"
                }
            }
        }
        alt_text = '天氣查詢🔍'
        message = FlexSendMessage(alt_text, contents)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif event.message.text == "冷笑話":
        import random
        number = random.randint(0, joke(0, "數量") - 1)
        contents = {
            "type": "bubble",
            "header": {
                "type":
                "box",
                "layout":
                "vertical",
                "flex":
                0,
                "contents": [{
                    "type": "text",
                    "text": "冷笑話",
                    "weight": "bold",
                    "size": "xl",
                    "align": "center",
                    "contents": []
                }]
            },
            "body": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "text",
                    "text": str(joke(number, "q")),
                    "size": "lg",
                    "align": "start",
                    "wrap": True,
                    "contents": []
                }]
            },
            "footer": {
                "type":
                "box",
                "layout":
                "vertical",
                "contents": [{
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "查看答案",
                        "data": str('#' + joke(number, "a"))
                    },
                    "style": "primary"
                }]
            }
        }
        alt_text = '冷笑話'
        message = FlexSendMessage(alt_text, contents)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif event.message.text == "範例圖片":
        import random
        圖片 = [
            'https://i.imgur.com/ZGhZkzS.png',
            'https://i.imgur.com/p219U7j.png',
            'https://i.imgur.com/3CkAhLj.png'
        ]
        number = random.randint(0, len(圖片) - 1)
        message = ImageSendMessage(original_content_url=圖片[number],
                                   preview_image_url=圖片[number])
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif event.message.text == "空汙":
        '''data = air('pm2.5',20)
      data = data.split('@')
      溫度 = 27
      濕度 = 75
      data1 = air('溫度',溫度)
      data2 = air('濕度',濕度)'''
        data = air('pm2.5', int(mcs('pm2.5')))
        data = data.split('@')
        溫度 = mcs('溫度')
        濕度 = mcs('濕度')
        data1 = air('溫度', 溫度)
        data2 = air('濕度', 濕度)
        contents = {
            "type": "bubble",
            "body": {
                "type":
                "box",
                "layout":
                "vertical",
                "spacing":
                "md",
                "contents": [{
                    "type":
                    "box",
                    "layout":
                    "horizontal",
                    "contents": [{
                        "type": "image",
                        "url": "https://i.imgur.com/uR6h9R1.png",
                        "align": "start"
                    }, {
                        "type": "text",
                        "text": "空氣品質",
                        "weight": "bold",
                        "size": "xxl",
                        "flex": 6,
                        "align": "start",
                        "gravity": "center",
                        "margin": "md",
                        "contents": []
                    }]
                }, {
                    "type":
                    "box",
                    "layout":
                    "vertical",
                    "spacing":
                    "sm",
                    "contents": [{
                        "type":
                        "box",
                        "layout":
                        "vertical",
                        "contents": [{
                            "type":
                            "box",
                            "layout":
                            "horizontal",
                            "contents": [{
                                "type": "text",
                                "text": "目前: " + str(data[0]) + " ug/m3",
                                "weight": "bold",
                                "size": "lg",
                                "flex": 1,
                                "align": "start",
                                "gravity": "center",
                                "contents": []
                            }, {
                                "type": "text",
                                "text": str(data[2]),
                                "size": "md",
                                "flex": 0,
                                "align": "end",
                                "contents": []
                            }]
                        }, {
                            "type":
                            "box",
                            "layout":
                            "vertical",
                            "margin":
                            "sm",
                            "height":
                            "6px",
                            "backgroundColor":
                            "#9FD8E36E",
                            "contents": [{
                                "type": "box",
                                "layout": "vertical",
                                "width": data[1] + "%",
                                "height": "6px",
                                "backgroundColor": data[3],
                                "contents": [{
                                    "type": "filler"
                                }]
                            }]
                        }]
                    }, {
                        "type":
                        "box",
                        "layout":
                        "baseline",
                        "margin":
                        "lg",
                        "contents": [{
                            "type": "icon",
                            "url": "https://i.imgur.com/ZGhZkzS.png"
                        }, {
                            "type": "text",
                            "text": "溫度: " + str(溫度) + " 度",
                            "weight": "bold",
                            "margin": "sm",
                            "contents": []
                        }, {
                            "type": "text",
                            "text": data1,
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                            "contents": []
                        }]
                    }, {
                        "type":
                        "box",
                        "layout":
                        "baseline",
                        "contents": [{
                            "type": "icon",
                            "url": "https://i.imgur.com/p219U7j.png"
                        }, {
                            "type": "text",
                            "text": "濕度: " + str(濕度) + " %",
                            "weight": "bold",
                            "flex": 0,
                            "margin": "sm",
                            "contents": []
                        }, {
                            "type": "text",
                            "text": data2,
                            "size": "sm",
                            "color": "#AAAAAA",
                            "align": "end",
                            "contents": []
                        }]
                    }]
                }]
            }
        }
        alt_text = '空汙'
        message = FlexSendMessage(alt_text, contents)
        line_bot_api.reply_message(event.reply_token, message)
        return 0
    elif event.message.text == "好手氣":
        message = TextSendMessage(str(google()))
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "目前溫濕度":
        message = TextSendMessage(str(mcs('GET', 0)))
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "電燈開關":
        message = ImageSendMessage(
            original_content_url=
            'https://images.clipartlogo.com/files/istock/previews/7705/77059375-electric-bulb-colored-vector-icon.jpg',
            preview_image_url=
            'https://images.clipartlogo.com/files/istock/previews/7705/77059375-electric-bulb-colored-vector-icon.jpg',
            quick_reply=QuickReply(items=[
                QuickReplyButton(
                    action=MessageAction(label="開燈請按我", text="燈已經幫妳打開了"),
                    image_url=
                    'https://images.clipartlogo.com/files/istock/previews/1005/100579801-light-bulb-icon-lamp-illumination-sign.jpg'
                ),
                QuickReplyButton(
                    action=MessageAction(label="關燈請按我", text="燈已經幫你關上了"),
                    image_url=
                    'https://images.clipartlogo.com/files/istock/previews/1005/100579801-light-bulb-icon-lamp-illumination-sign.jpg'
                )
            ]))
        line_bot_api.reply_message(event.reply_token, message)
    elif event.message.text == "燈已經幫妳打開了":
        mcs('POST', 1)
        return 0
    elif event.message.text == "燈已經幫你關上了":
        mcs('POST', 0)
        return 0
    elif event.message.text == "圖片":
        message = ImageSendMessage(
            original_content_url='https://example.com/original.jpg',
            preview_image_url='https://example.com/preview.jpg')
        line_bot_api.reply_message(event.reply_token, message)
    else:
        message = TextSendMessage(text=event.message.text)
        line_bot_api.reply_message(event.reply_token, message)


@handler.add(PostbackEvent)
def handle_post_message(event):
    # can not get event text
    #print("event =", event)
    #print(event.postback.data)
    data = event.postback.data
    print(data)
    if '#' in data:
        text = data[1:]
        print(text)
        line_bot_api.reply_message(event.reply_token,
                                   TextMessage(text=str(text)))
        return 0
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=str(the_weather(str(event.postback.data)))))
        return 0


@handler.add(BeaconEvent)
def handle_beacon_event(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)  # 取得個人檔案
    print("使用者uid：" + user_id + "中文名稱：" + profile.display_name)  # 記錄使用者名稱
    print(event)
    if event.beacon.hwid == "016546759c" and event.beacon.type == "enter":
        line_bot_api.push_message(
            event.source.user_id,
            TextMessage(text='ESP32測試' + '\n\n' + '你的id=' + user_id + '\n\n' +
                        "歡迎來到MIAT319-1:" + profile.display_name))
    elif event.beacon.hwid == "016546759c" and event.beacon.type == "leave":
        line_bot_api.push_message(
            event.source.user_id,
            TextMessage(text='ESP32測試' + '\n\n' + '你的id=' + user_id + '\n\n' +
                        "希望下次還可以來MIAT319-1:" + profile.display_name))
    if event.beacon.hwid == "014a7d5087" and event.beacon.type == "enter":
        line_bot_api.push_message(
            event.source.user_id,
            TextMessage(text='LinkIt 7697測試' + '\n\n' + '你的id=' + user_id +
                        '\n\n' + "歡迎來到MIAT319-1:" + profile.display_name))
    elif event.beacon.hwid == "014a7d5087" and event.beacon.type == "leave":
        line_bot_api.push_message(
            event.source.user_id,
            TextMessage(text='LinkIt 7697測試' + '\n\n' + '你的id=' + user_id +
                        '\n\n' + "希望下次還可以來MIAT319-1:" + profile.display_name))


@app.route('/')
def index():
    return 'Hello World'


def google():
    import requests
    from bs4 import BeautifulSoup
    response = requests.get("https://www.google.com/doodles?hl=zh-TW")
    response.encoding = 'utf-8'
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    soup.encoding = 'utf-8'
    # print(soup.prettify())  # 輸出排版後的HTML內容
    result = soup.find_all("div", class_="title", limit=10)
    titles = soup.select(".title", limit=6)
    print(titles)
    # print(result)
    print("==================================")
    data = "資料來源於google好手氣：" + "\n"
    for title in result:
        s = title.select_one("a").getText()
        s = s.replace(' ', '')
        s = s.strip()
        #print("標題：", s)
        #print("網址：", "https://www.google.com/"+title.select_one("a").get("href"))
        data += "\n"+"標題："+s+"\n\n"+"網址："+"https://www.google.com/" + \
            title.select_one("a").get("href")
    return data


def joke(data, mode):
    #參考網站 https://w199584.pixnet.net/blog/post/16756643
    q = [
        "小孩子跌倒，猜一成語？", "一顆心值多少錢？", "愛是什麼？", "饅頭假裝是肉包，猜一人名？", "誰家沒有電話？",
        "孔子有3位徒弟：子貢、子路和子游，哪一位不是人？", "哪種動物最怕冷？", "老鼠姓什麼？", "一口井，旁邊有兩杯茶猜一種職業？",
        "鯊魚不小心吞了一顆綠豆，牠變成了什麼？", "少了一本書，猜一成語？", "第11本書，猜一成語？", "很多離婚的女人，猜一成語？",
        "希爾頓、香格里拉、凱悅，哪一家服務生最沒禮貌？", "小明爬樓梯，才爬到2樓，為什麼覺得腳很酸？", "夕陽西下，斷腸人在哪裡？",
        "五月花和百合花哪一個沒有生小孩？", "為什麼阿里巴巴只帶36名海盜過來？", "老師:為啥要來上學?",
        "猩猩跟猴子很怕一種線，請問那是什麼線？", "大象的媽媽為什麼是猩猩??", "有個人住在雨傘上面，猜猜他是誰..？",
        "為什麼上帝不用租A片?", "地震是公的還母的?", "人體哪個東西貴的可賣到兆？", "有一把隱形的劍，是什麼劍？",
        "李哪吒、唐三奘、牛魔王，哪一個患有不孕症呢？", "誰的大便最濃？"
    ]
    a = [
        "馬馬虎虎（媽媽撫撫）", "一億（一心一意）", "基摩人（愛斯基摩人）", "吳宗憲（無中陷）", "天衣，因為天衣無縫（PHONE）",
        "子路，因為指鹿為馬（子路為馬）", "鴨子（〝呱呱〞台語：冷冷）", "米（米老鼠）", "警察伯伯。", "綠豆沙（綠豆鯊）",
        "缺一不可（缺一Book）", "不可思議（Book11）", "前功盡棄（前公盡棄）", "香格里拉（台語：誰叫你來）",
        "因為他踩到檸檬", "醫院", "五月花。五月花〝衛生紙〞（未生子）", "因為台灣已經有市民大道（4名大盜）了",
        "學生:不讓老師失業!", "平行線，因為沒有相交（沒有香蕉)", "因為象由猩生阿...（相由心生） <---這就簡單一點了...",
        "黑狗兄啦!", "是因為人在看天在看", "答案是公的….因為地震有ㄐㄐ....", "膽...好膽麥跑(兆).(台語)",
        "看不見(劍)", "唐三奘【唐三奘要去西方取經(精)】", "席維斯【屎特濃】"
    ]
    if mode == "數量":
        return len(q)
    elif mode == "q":
        return q[data]
    elif mode == "a":
        return a[data]


def the_weather(data):
    cities = ["臺北", "新北", "桃園", "臺中", "臺南", "高雄", "基隆", "新竹", "嘉義"]  # 市
    counties = [
        "苗栗", "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江"
    ]  # 縣
    city = data[:2]
    user_key = "CWB-2F5F4D0B-DDEE-4832-80F0-30DA4E6EC13B"
    doc_name = "F-C0032-001"
    if not city == '':  # 天氣類地點存在
        flagcity = False  # 檢查是否為縣市名稱
        city = city.replace('台', '臺')  # 氣象局資料使用「臺」
        if city in cities:  # 加上「市」
            city += '市'
            flagcity = True
        elif city in counties:  # 加上「縣」
            city += '縣'
            flagcity = True
        if flagcity:  # 是縣市名稱
            token = 'CWB-2F5F4D0B-DDEE-4832-80F0-30DA4E6EC13B'
            url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=' + token + '&format=JSON&locationName=' + str(
                city)
            Data = requests.get(url)
            print(Data.text)
            Data = (json.loads(
                Data.text,
                encoding='utf-8'))['records']['location'][0]['weatherElement']
            res = [[], [], []]
            for j in range(3):
                for i in Data:
                    res[j].append(i['time'][j])
            for data in res:
                print('{} ~ {}'.format(data[0]['startTime'][5:-3],
                                       data[0]['endTime'][5:-3]))
                print(city + '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {} %'.format(
                    data[0]['parameter']['parameterName'], data[2]['parameter']
                    ['parameterName'], data[4]['parameter']['parameterName'],
                    data[1]['parameter']['parameterName']))
                return city + '天氣狀況 {}\n溫度 {} ~ {} °C\n降雨機率 {} %'.format(
                    data[0]['parameter']['parameterName'],
                    data[2]['parameter']['parameterName'],
                    data[4]['parameter']['parameterName'],
                    data[1]['parameter']['parameterName'])
        else:
            text = '無此地點天氣資料！'
        return text


def mcs(mode, data):
    if mode == 'POST':
        headers = {
            'deviceKey':
            '907825d55de2ef8b6620ba8da7613d57e2cf1a132770d942f17ebbc457bc2d9e',
            'Content-Type': 'text/csv'
        }
        data_channel = "led" + ",," + str(data)
        res = requests.post(
            "http://211.20.253.250:3000/api/devices/SyMdGDI__/datapoints.csv",
            headers=headers,
            data=data_channel)
        print(res)
    elif mode == 'GET':
        headers = {
            "deviceKey":
            "ef6c180568e36a8ac6e42a8262091683db295f614fe91bec51cfa96115fda707",
            "contentType": "application/json"
        }

        res = requests.get(
            "http://120.125.96.212:3000/api/devices/r1QY1Kzfu/datachannels/alarm2/datapoints?limit=1",
            headers=headers)
        resp = res.json()
        h = resp['data'][0]['values']['value']
        print(h)

        res = requests.get(
            "http://120.125.96.212:3000/api/devices/r1QY1Kzfu/datachannels/alarm1/datapoints?limit=1",
            headers=headers)
        resp = res.json()
        t = resp['data'][0]['values']['value']
        print(t)
        text = "溫度：" + str(t) + "度" + " 濕度：" + str(h) + "%"
        print("溫度：", t, "度", " 濕度：", h, "%")
        return text


def get_two_float(f_str, n):
    f_str = str(f_str)  # f_str = '{}'.format(f_str) 也可以轉換為字符串
    a, b, c = f_str.partition('.')
    c = (c + "0" * n)[:n]  # 如論傳入的函數有幾位小數，在字符串後面都添加n為小數0
    return ".".join([a, c])


def air(mode, data):
    if mode == 'pm2.5':
        data1 = (data / 71) * 100
        if data1 >= 100.00:
            data1 = 100.00
        print(data1)
        data1 = get_two_float(data1, 1)  #判斷幾%
        print(data1)
        if data <= 35:
            data2 = '優良'
            data3 = '#4bb900'
        elif data <= 53:
            data2 = '中等'
            data3 = '#ffe200'
        elif data <= 70:
            data2 = '高危害'
            data3 = '#fe0201'
        else:
            data2 = '超高危害'
            data3 = '#b101b3'
        print(data2)
        print(data3)
        return str(data) + '@' + str(data1) + '@' + str(data2) + '@' + str(
            data3)
    elif mode == '溫度':
        if data <= -5:
            data1 = '防凍傷'
        elif data <= 5:
            data1 = '大寒'
        elif data <= 15:
            data1 = '寒冷'
        elif data <= 27:
            data1 = '舒適'
        elif data <= 38:
            data1 = '炎熱'
        else:
            data1 = '防中暑'
        return data1
    elif mode == '濕度':
        if data <= 40:
            data1 = '乾燥'
        elif data <= 70:
            data1 = '舒適'
        else:
            data1 = '潮濕'
        return data1


def mcs_pm(modo):
    if modo == '溫度':
        headers = {
            "deviceKey":
            "d627e3a02fd6187f5483c436232abbd4aa89d4bf949de314e4efe5c5712b6a38",
            "contentType": "application/json"
        }
        res = requests.get(
            "http://211.20.253.250:3000/api/devices/S1qsHmEPO/datachannels/temp/datapoints?limit=1",
            headers=headers)
        #print(res.text)
        res = res.json()
        data = res['data'][0]['values']['value']
        print('溫度: ', data, ' 度')
        return data
    elif modo == '濕度':
        headers = {
            "deviceKey":
            "d627e3a02fd6187f5483c436232abbd4aa89d4bf949de314e4efe5c5712b6a38",
            "contentType": "application/json"
        }
        res = requests.get(
            "http://211.20.253.250:3000/api/devices/S1qsHmEPO/datachannels/humid/datapoints?limit=1",
            headers=headers)
        #print(res.text)
        res = res.json()
        data = res['data'][0]['values']['value']
        print('濕度: ', data, ' %')
        return data
    elif modo == 'pm2.5':
        headers = {
            "deviceKey":
            "d627e3a02fd6187f5483c436232abbd4aa89d4bf949de314e4efe5c5712b6a38",
            "contentType": "application/json"
        }
        res = requests.get(
            "http://211.20.253.250:3000/api/devices/S1qsHmEPO/datachannels/PM25/datapoints?limit=1",
            headers=headers)
        #print(res.text)
        res = res.json()
        data = res['data'][0]['values']['value']
        print('PM2.5數值: ', data, ' ug/m3')
        return data


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
