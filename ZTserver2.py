from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# 读取允许的账户列表
def load_allowed_accounts():
    try:
        # 使用当前工作目录（用户运行exe的目录）
        current_dir = os.getcwd()
        # 构建JSON文件路径
        json_path = os.path.join(current_dir, 'allowed_accounts.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('allowed_accounts', {})
    except Exception as e:
        print(f"Error loading allowed accounts: {str(e)}")
        return {}

@app.route('/')
def home():
    return "Hello, this is the MT5 server!"

@app.route('/validate', methods=['POST'])
def validate_account():
    try:
        # 解析 JSON 数据
        data = request.get_json()
        if not data:
            return jsonify({"status": "fail", "message": "Invalid JSON format"}), 400
        
        # 获取 broker 和 account
        broker = data.get('broker')
        account = data.get('account')

        # 加载允许的账户列表
        allowed_accounts = load_allowed_accounts()
        
        # 检查账户是否被允许
        if broker in allowed_accounts and account in allowed_accounts[broker]:
            return jsonify({"status": "success", "message": "Account verified!"}), 200
        else:
            return jsonify({"status": "fail", "message": "Account not authorized!"}), 403
    except Exception as e:
        return jsonify({"status": "fail", "message": f"Error parsing request: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))
