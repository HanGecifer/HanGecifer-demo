import streamlit as st
from zhipuai import ZhipuAI

# ⚠️⚠️⚠️ 把下面引号里的字换成你刚才在智谱网页上拿到的 API Key ⚠️⚠️⚠️
#保密
API_KEY = st.secrets["ZHIPU_KEY"]

#网络页标题与图标
st.set_page_config(page_title="极简医学循证助手", page_icon="🩺")
#网页标题
st.title("🩺 极简医学循证助手 ")
#免责声明
st.sidebar.warning("⚠️ 免责声明：本工具为工程练习，AI回答不能替代专业医生。")
#输入框，接受输入
user_input = st.text_area("请输入您的医学问题（例如：高血压吃什么药？）：", height=150)

if st.button("开始回答"):
    if not user_input:
        st.warning("请先输入问题！")
    else:
        with st.spinner("正在查阅文献..."): #表示加载图标，伴随着以下事情进行
            try:
                client = ZhipuAI(api_key=API_KEY)

                # 核心：引用与拒答约束
                system_prompt = """
                你是一个严谨的医学助手。请遵守以下规则：
                1. 结论必须带文献引用（模拟格式如：[1] NEJM, 2023）。
                2. 遇到荒谬或不懂的问题，直接回答：【拒答】当前医学证据不足。
                3. 结尾必须加：⚠️ 仅供医学参考，请遵医嘱。
                """

                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ]
                )
                st.success("回答如下：")
                st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"出错了：{e}")
st.caption("\n网站开发人：HanGecifer   指导老师：南昌航空大学 胡正老师")
