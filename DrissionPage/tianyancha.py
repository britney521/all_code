from DrissionPage import ChromiumOptions, ChromiumPage,errors


co = ChromiumOptions()
page = ChromiumPage(co)
page.get('https://www.tianyancha.com/search?key=&sessionNo=1723599497.24069195')

page.wait.ele_displayed('.tyc-header-suggest-input input', timeout=3)
page.ele('登录/注册').click()
page.wait.ele_displayed('div.login-toggle.-scan', timeout=3)
page.ele('tag:div@class:login-toggle').click()
try:
    # 等待手机号输入框加载完成并变为可点击状态
    page.wait.ele_displayed('tag:input', timeout=10)

    # 输入手机号
    phone_input = page.ele('css:.phone input')
    phone_input.input('18166072280')
    print(phone_input.attr('value'))
    # 检查输入框的值是否正确
    assert phone_input.attr('value') == '181 6607 2280', "手机号输入不正确"

    # 等待“获取验证码”按钮加载完成并变为可点击状态
    page.wait.ele_displayed('获取验证码', timeout=10)

    # 点击“获取验证码”按钮
    verify_button = page.ele('获取验证码')
    verify_button.click()


except errors.ElementNotFoundError as e:
    print(f"元素未找到错误: {e}")
except AssertionError as e:
    print(f"断言失败: {e}")
except Exception as e:
    print(f"发生其他错误: {e}")
# page.ele('tag:input').input('京龙')
# page.ele('天眼一下').click()


