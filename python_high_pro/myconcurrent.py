import asyncio
import time
import random
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# *定义协程
async def async_hello():
    print("hello world!")

# **运行
# loop = asyncio.get_event_loop()
# loop.run_until_complete(async_hello())
# loop.close()


# *定义协程
async def print_number(number):
    print(number)

# **异步执行
def test1():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([print_number(number) for number in range(10)]))
    loop.close()


async def waiter(name):
    for _ in range(4):
        time_to_sleep = random.randint(1, 3) / 4
        asyncio.sleep(time_to_sleep)
        print("{} waited {} seconeds".format(name, time_to_sleep))

async def main():
    await asyncio.wait([waiter("foo"), waiter("bar")])

def test2():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


# **异步http请求(pip install aiohttp)
# session = aiohttp.ClientSession()

# async def get(question):
#     url = "http://192.168.1.123:8000/mgbase/split_knowledge"
#     params = {"question": question}
#     async with session.get(url, params=params) as response:
#         result = await response.text()
#         return result

# QUESTIONS = ("纳税人缴纳增值税", "如何缴纳车辆购置税", 
#              "如何缴纳车辆购置税", "如何缴纳个人所得税")

# async def get_word(question):
#     return await get(question)

# async def present_result(result):
#     word = await result
#     print(word)

# async def main2():
#     await asyncio.wait(
#         [present_result(get_word(q)) for q in QUESTIONS]
#     )

# def test3():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main2())

#     # **关闭clientsession
#     loop.run_until_complete(session.close())
#     loop.close()


# **Executors
# QUESTIONS = ("纳税人缴纳增值税", "如何缴纳车辆购置税", 
#              "如何缴纳车辆购置税", "如何缴纳个人所得税")

# def get_word2(question):
#     url = "http://192.168.1.123:8000/mgbase/split_knowledge"
#     params = {"question": question}
#     return requests.get(url, params).text

# def present_result2(result):
#     print(result)

# def test4():
#     with ThreadPoolExecutor(2) as pool:
#         results = pool.map(get_word2, QUESTIONS)
    
#     for result in results:
#         present_result2(result)


QUESTIONS = ("纳税人缴纳增值税", "如何缴纳车辆购置税", 
             "如何缴纳车辆购置税", "如何缴纳个人所得税")

def get3(question):
    url = "http://192.168.1.123:8000/mgbase/split_knowledge"
    params = {"question": question}
    return requests.get(url, params).text

async def get_word3(question):
    #import BaseEventLoop as loop
    #rst = loop.
    return await get3(question)

def present_result3(result):
    print(result)

def test5():
    with ThreadPoolExecutor(2) as pool:
        results = pool.map(get_word3, QUESTIONS)
    
    for result in results:
        present_result3(result)

def test(sentence):
        
        url = "http://192.168.1.123:8000/mgbase/validate_knowledge_repeat?question="

        # 调用的接口，其中的ip应该需要根据实际的来修改
        input_url = url+sentence
        answer = requests.get(input_url).json()
        token = answer['token']
        print('sentence:', sentence) # 表示输入的问题在excel表格的第二列

        # print(requests.get(input_url).json()['content'])
        if token == 0:
            # ws.write(line, 3, 'false')            # 保存到同一excel表格的第三列处
            rst = sentence + "：" + 'false'
        else:
            # get_sen = requests.get(input_url).json()['content']['relativeQuestionList'][0]['question']
            get_sen = answer['content']['relativeQuestionList']
            # print(get_sen)
            if get_sen == []:
                # ws.write(line, 3, 'strange')    # 保存到同一excel表格的第三列处
                rst = sentence + "：" + 'strange'
            elif sentence == get_sen[0]['question']:
                # ws.write(line, 3, 'ture')
                rst = sentence + "：" + 'ture'
            else:
                # ws.write(line, 3, 'false')         # 保存到同一excel表格的第三列处
                rst = sentence + "：" + 'false'

        return rst


if __name__ == "__main__":
    # test1()
    # test2()
    # test3()
    # test4()
    test5()

    

    # questions = tuple(["纳税人缴纳", 
    # "受票方丢失未认证增值税专用发票抵扣联要怎么办？",
    # '金融商品转让可以开具增值税专用发票吗？'
    # ])
    # with ProcessPoolExecutor(6) as pool:
    #     results = pool.map(test, questions)

    # for result in results:
    #     if not result.endswith("ture"):
    #         print(result)