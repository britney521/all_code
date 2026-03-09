from bs4 import BeautifulSoup


def extract_from_html(html_content):
    """从 HTML 文本中提取用法用量（兼容 Table 和 Div 结构）"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # 关键词列表，防止网页有些写的是“用法与用量”
        keywords = ["用法用量", "用法与用量"]

        # --- 策略 1: 查找表格结构 (th -> td) ---
        # 查找包含关键词的 th 标签
        target_th = soup.find('th', string=lambda text: text and any(k in text for k in keywords))
        if target_th:
            # 表格结构通常内容在下一个 td
            next_td = target_th.find_next_sibling('td')
            if next_td:
                return next_td.get_text(strip=True)

        # --- 策略 2: 查找 DIV/段落结构 (div/h/p -> next_sibling) ---
        # 查找所有可能作为标题的标签，且文本包含关键词
        # 限制标签类型，避免匹配到正文里的文字
        potential_tags = ['div', 'p', 'span', 'h3', 'h4', 'strong', 'b']

        # 查找符合条件的标签
        targets = soup.find_all(potential_tags)

        for tag in targets:
            text = tag.get_text(strip=True)
            # 判断是否是标题：必须包含关键词，且字数不能太多（防止匹配到正文里的一长句话）
            # 例如 "【用法用量】" 长度很短，而正文 "本品用法用量为..." 长度较长
            if any(k in text for k in keywords) and len(text) < 20:

                # 找到标题后，获取下一个兄弟节点（可能是文本，也可能是标签）
                # find_next_sibling() 会跳过换行符等空白节点，直接找下一个 Tag
                next_node = tag.find_next_sibling()

                if next_node:
                    return next_node.get_text(strip=True)

                # 特殊情况：有时候内容不是兄弟节点，而是跟在标题后面的纯文本（不太常见，备用）
                # parent_text = tag.parent.get_text() ... 暂不处理，以免误判

    except Exception as e:
        print(f"HTML 解析出错: {e}")

    return None

print(extract_from_html('''<div class="content_paragraph_title"><a name="ph_3" id="ph_3"></a>【说明书修订日期】</div>
                                    <div>
                                        2007年04月06日
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_4" id="ph_4"></a>【特殊标记】</div>
                                    <div>
                                        OTC<br />乙类<br />外
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_6" id="ph_6"></a>【药品名称】</div>
                                    <div>
                                        双氯芬酸钠凝胶
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_7" id="ph_7"></a>【英文名】</div>
                                    <div>
                                        Diclofenac Sodium Gel
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_8" id="ph_8"></a>【汉语拼音】</div>
                                    <div>
                                        Shuanglü fensuanna Ningjiao
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_9" id="ph_9"></a>【成份】</div>
                                    <div>
                                        本品每克含主要成分双氯芬酸钠0.01克。辅料为卡波姆、聚乙二醇、三乙醇胺、丙二醇、羟苯丁酯。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_10" id="ph_10"></a>【性状】</div>
                                    <div>
                                        本品为水溶性凝胶。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_11" id="ph_11"></a>【作用类别】</div>
                                    <div>
                                        本品为镇痛类非处方药药品。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_12" id="ph_12"></a>【适应症】</div>
                                    <div>
                                        用于缓解肌肉、软组织和关节的轻至中度疼痛。如缓解肌肉、软组织的扭伤、拉伤、挫伤、劳损、腰背部损伤引起的疼痛以及关节疼痛等。也可用于骨关节炎的对症治疗。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_13" id="ph_13"></a>【规格】</div>
                                    <div>
                                        1%
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_14" id="ph_14"></a>【用法用量】</div>
                                    <div>
                                        外用。按照痛处面积大小，使用本品适量，轻轻揉搓，使本品渗透皮肤，一日3-4次。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_15" id="ph_15"></a>【不良反应】</div>
                                    <div>
                                        1.偶可出现局部不良反应：过敏性或非过敏性皮炎如丘疹、皮肤发红、水肿、瘙痒、小水泡、大水泡或鳞屑等。<br />2.局部使用本品而导致全身不良反应的情况少见，若将其用于较大范围皮肤长期使用，则可能出现：一般性皮疹、过敏性反应（如哮喘发作、血管神经性水肿、光敏反应等）。如发生这种情况，应咨询医师。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_16" id="ph_16"></a>【禁忌】</div>
                                    <div>
                                        1.对其他非甾体抗炎药过敏者禁用。<br />2.对丙二醇过敏者禁用。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_17" id="ph_17"></a>【注意事项】</div>
                                    <div>
                                        1.由于本品局部应用也可全身吸收，故应避免长期大面积使用。<br />2.肝、肾功能不全者以及孕妇、哺乳期妇女使用前请咨询医师或药师。<br />3.不得用于破损皮肤或感染性创口。<br />4.12岁以下儿童用量请咨询医师。<br />5.避免接触眼睛和其他黏膜（如口、鼻等）。<br />6.如使用本品7日，局部疼痛未缓解，请咨询医师或药师。<br />7.对本品过敏者禁用，过敏体质者慎用。<br />8.本品性状发生改变时禁止使用。<br />9.请将本品放在儿童不能接触的地方。<br />10.儿童必须在成人监护下使用。<br />11.如正在使用其他药品，使用本品前请咨询医师或药师。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_18" id="ph_18"></a>【药物相互作用】</div>
                                    <div>
                                        如与其他药物同时使用可能会发生药物相互作用，详情请咨询医师或药师。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_19" id="ph_19"></a>【药理作用】</div>
                                    <div>
                                        本品为前列腺素合成抑制剂，具有抗炎、镇痛作用。局部应用。其有效成份可穿透皮肤达到炎症区域，缓解急、慢性炎症反应，使炎性肿痛减轻、疼痛缓解。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_20" id="ph_20"></a>【贮藏】</div>
                                    <div>
                                        密封，在阴凉处（不超过20℃）保存。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_21" id="ph_21"></a>【包装】</div>
                                    <div>
                                        软膏铝管装，15克/支，20克/支。
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_22" id="ph_22"></a>【有效期】</div>
                                    <div>
                                        24个月
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_23" id="ph_23"></a>【执行标准】</div>
                                    <div>
                                        WS<sub>1</sub>-(X-360)-2004Z
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_24" id="ph_24"></a>【批准文号】</div>
                                    <div>
                                        国药准字H10950169
                                    </div>
                                    <div class="content_paragraph_title"><a name="ph_25" id="ph_25"></a>【生产企业】</div>
                                    <div>
                                        企业名称：南京长澳制药有限公司<br />生产地址：南京市六合区八百路2号<br />邮政编码：211500<br />电话号码：025-57759539<br />传真号码：025-57758296<br />网址：www.changao.com<br />如有问题可与生产企业联系
                                    </div>
                            '''))