"""
哈利波特魔法工坊 - 后端API服务
整合数据库和AI服务
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from database import db
from ai_services import (
    sorting_hat_service,
    character_chat_service,
    spell_recognition_service
)

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 配置
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# ============================================================================
# 基础路由
# ============================================================================

@app.route('/')
def home():
    """首页"""
    stats = db.get_statistics()
    return jsonify({
        'message': '哈利波特魔法工坊 API',
        'version': '1.0.0',
        'statistics': stats,
        'endpoints': {
            '用户': {
                'GET /api/user': '获取用户数据',
                'POST /api/user': '创建用户',
                'PUT /api/user': '更新用户数据'
            },
            '魔杖': {
                'POST /api/wand/generate': '生成魔杖',
                'POST /api/wand/save': '保存魔杖'
            },
            '分院': {
                'POST /api/sorting/chat': '分院帽对话'
            },
            '咒语': {
                'POST /api/spells/unlock': '解锁咒语',
                'POST /api/spells/recognize': '识别咒语发音'
            },
            '角色': {
                'POST /api/characters/chat': '角色对话'
            },
            '谜题': {
                'POST /api/puzzles/check': '检查谜题答案',
                'POST /api/puzzles/progress': '更新谜题进度'
            }
        }
    })

# ============================================================================
# 用户数据API
# ============================================================================

@app.route('/api/user', methods=['GET'])
def get_user():
    """获取用户数据"""
    user_id = request.args.get('userId', 'default')
    user_data = db.get_user(user_id)
    
    if user_data:
        return jsonify(user_data)
    else:
        return jsonify({
            'house': '',
            'wand': None,
            'unlockedSpells': [],
            'puzzleProgress': 0,
            'spellScores': {}
        })

@app.route('/api/user', methods=['POST'])
def create_user():
    """创建用户"""
    user_id = request.args.get('userId')
    if not user_id:
        user_id = request.json.get('userId', 'default')
    
    if db.get_user(user_id):
        return jsonify({'success': False, 'message': '用户已存在'}), 400
    
    user_data = request.json
    success = db.create_user(user_id, user_data)
    
    if success:
        return jsonify({'success': True, 'userId': user_id})
    else:
        return jsonify({'success': False, 'message': '创建用户失败'}), 500

@app.route('/api/user', methods=['PUT'])
def update_user():
    """更新用户数据"""
    user_id = request.args.get('userId', 'default')
    updates = request.json
    
    if not db.get_user(user_id):
        return jsonify({'success': False, 'message': '用户不存在'}), 404
    
    success = db.update_user(user_id, updates)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': '更新失败'}), 500

# ============================================================================
# 魔杖API
# ============================================================================

@app.route('/api/wand/generate', methods=['POST'])
def generate_wand():
    """生成专属魔杖"""
    data = request.json
    answers = data.get('answers', [])
    
    # 基于答案生成魔杖属性
    wood_types = ['冬青木', '山毛榉木', '橡木', '紫杉木', '葡萄藤木', '花楸木']
    core_types = ['凤凰羽毛', '龙神经', '独角兽毛', '雷鸟尾羽']
    flexibilities = ['柔韧', '坚固', '弹性', '坚硬']
    
    wand = {
        'wood': wood_types[answers[0] % len(wood_types)],
        'core': core_types[answers[1] % len(core_types)],
        'length': 10 + answers[2],
        'flexibility': flexibilities[answers[3] % len(flexibilities)],
        'description': _generate_wand_description(answers)
    }
    
    return jsonify(wand)

def _generate_wand_description(answers):
    """生成魔杖描述"""
    descriptions = [
        '这根魔杖与它的主人有着深厚的联系，善于施展复杂的变形术。',
        '这根魔杖选择了一个拥有强烈意志的巫师，它在对抗黑魔法时表现出色。',
        '这根魔杖适合施展守护咒和防护魔法，它的主人有着纯洁的心灵。',
        '这根魔杖在施法时会产生美丽的光效，展现出主人独特的魔法风格。'
    ]
    return descriptions[answers[0] % len(descriptions)]

@app.route('/api/wand/save', methods=['POST'])
def save_wand():
    """保存魔杖"""
    data = request.json
    user_id = data.get('userId', 'default')
    wand_data = data.get('wand')
    
    success = db.save_wand(user_id, wand_data)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': '保存失败'}), 500

# ============================================================================
# 分院帽API
# ============================================================================

@app.route('/api/sorting/chat', methods=['POST'])
def sorting_chat():
    """分院帽对话"""
    data = request.json
    messages = data.get('messages', [])
    
    response = sorting_hat_service.chat(messages)
    
    # 如果完成分院，保存用户数据
    if response.get('sorted'):
        user_id = data.get('userId', 'default')
        result = response.get('result', {})
        house = result.get('house', '')
        
        if not db.get_user(user_id):
            db.create_user(user_id, {})
        
        db.update_user(user_id, {'house': house})
    
    return jsonify(response)

# ============================================================================
# 咒语API
# ============================================================================

@app.route('/api/spells/unlock', methods=['POST'])
def unlock_spell():
    """解锁咒语"""
    data = request.json
    user_id = data.get('userId', 'default')
    spell_id = data.get('spellId')
    
    success = db.unlock_spell(user_id, spell_id)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': '解锁失败'}), 500

@app.route('/api/spells/recognize', methods=['POST'])
def recognize_spell():
    """识别咒语发音"""
    data = request.json
    spell_id = data.get('spellId')
    audio_data = data.get('audioData')
    
    # 调用AI服务进行识别
    result = spell_recognition_service.recognize(spell_id, audio_data)
    
    if result.get('success'):
        # 保存成绩
        user_id = data.get('userId', 'default')
        score = result.get('score', 0)
        db.save_spell_score(user_id, spell_id, score)
    
    return jsonify(result)

# ============================================================================
# 角色对话API
# ============================================================================

@app.route('/api/characters/chat', methods=['POST'])
def character_chat():
    """角色对话"""
    data = request.json
    character_id = data.get('characterId')
    messages = data.get('messages', [])
    
    response = character_chat_service.chat(character_id, messages)
    
    # 保存对话记录
    user_id = data.get('userId', 'default')
    if len(messages) > 1:
        db.save_dialogue(user_id, character_id, messages)
    
    return jsonify(response)

# ============================================================================
# 谜题API
# ============================================================================

@app.route('/api/puzzles/check', methods=['POST'])
def check_puzzle():
    """检查谜题答案"""
    data = request.json
    puzzle_id = data.get('puzzleId')
    user_answer = data.get('answer')
    
    correct_answers = _get_correct_answers(puzzle_id)
    is_correct = any(
        user_answer.lower().strip() == ans.lower() 
        for ans in correct_answers
    )
    
    response = {
        'correct': is_correct,
        'explanation': _get_puzzle_explanation(puzzle_id)
    }
    
    return jsonify(response)

@app.route('/api/puzzles/progress', methods=['POST'])
def update_puzzle_progress():
    """更新谜题进度"""
    data = request.json
    user_id = data.get('userId', 'default')
    level = data.get('level')
    
    success = db.update_puzzle_progress(user_id, level)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': '更新失败'}), 500

def _get_correct_answers(puzzle_id):
    """获取正确答案"""
    correct_answers = {
        1: ['风', 'wind', '微风'],
        2: ['独角兽', '飞马', 'unicorn', 'pegasus'],
        3: ['魔药', 'potion'],
        4: ['镜子', '魔镜', '厄里斯魔镜', 'mirror'],
        5: ['时间转换器', '时间器', 'time turner'],
        6: ['老三', '第三个兄弟'],
        7: ['爱', 'love']
    }
    return correct_answers.get(puzzle_id, [])

def _get_puzzle_explanation(puzzle_id):
    """获取谜题解析"""
    explanations = {
        1: '风！风看不见却能吹动万物，没有翅膀却能远行，无形却能传递声音。',
        2: '独角兽或飞马！在魔法生物中，它们是温和无害的神奇生物。',
        3: '魔药本身！魔药既可以用来伤害也可以用来拯救，关键在于用途和剂量。',
        4: '镜子/厄里斯魔镜！镜子反射现实，但厄里斯魔镜展示的是人内心深处的渴望。',
        5: '时间转换器！它可以让人回到过去，但不能改变已经发生的事情。',
        6: '老三！他明智地使用了隐身衣，最终接受了自己的命运。',
        7: '爱！爱是伏地魔无法理解也无法击败的力量。'
    }
    return explanations.get(puzzle_id, '答对了！')

# ============================================================================
# 错误处理
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    print(f"哈利波特魔法工坊 API 启动中...")
    print(f"端口: {PORT}")
    print(f"调试模式: {DEBUG}")
    print(f"访问地址: http://localhost:{PORT}")
    
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
