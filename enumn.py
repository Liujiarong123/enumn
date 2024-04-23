from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

# 加载 spaCy 的英文模型
nlp = spacy.load("en_core_web_sm")

# 对文本进行分析和语义理解
def analyze_text(text):
    doc = nlp(text)
    
    # 提取关键词
    keywords = [token.text for token in doc if not token.is_stop and token.is_alpha]
    
    # 提取命名实体
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    return keywords, entities

# 处理 POST 请求，用于接收用户消息并返回响应
@app.route('/webhook', methods=['POST'])
def webhook():
    # 解析接收到的 JSON 数据
    data = request.get_json()
    user_message = data['message']
    
    # 调用对话处理函数处理用户消息
    keywords, entities = analyze_text(user_message)
    
    # 构造机器人的响应
    bot_response = "我收到了你的消息：{}\n".format(user_message)
    bot_response += "关键词: {}\n".format(keywords)
    bot_response += "命名实体: {}\n".format(entities)
    
    # 返回机器人的响应
    return jsonify({'response': bot_response})

# 主函数
if __name__ == '__main__':
    app.run(debug=True)
