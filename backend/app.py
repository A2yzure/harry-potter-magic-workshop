from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')

# 模拟数据存储
users_db = {}
chat_history_db = {}

@app.route('/')
def home():
    return jsonify({
        'message': '哈利波特魔法工坊 API',
        'version': '1.0.0',
        'endpoints': [
            '/api/wand/generate',
            '/api/sorting/chat',
            '/api/characters/chat',
            '/api/spells/recognize',
            '/api/puzzles/check'
        ]
    })

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
        'description': generate_wand_description(answers)
    }
    
    return jsonify(wand)

def generate_wand_description(answers):
    """生成魔杖描述"""
    descriptions = [
        '这根魔杖与它的主人有着深厚的联系，善于施展复杂的变形术。',
        '这根魔杖选择了一个拥有强烈意志的巫师，它在对抗黑魔法时表现出色。',
        '这根魔杖适合施展守护咒和防护魔法，它的主人有着纯洁的心灵。',
        '这根魔杖在施法时会产生美丽的光效，展现出主人独特的魔法风格。'
    ]
    return descriptions[answers[0] % len(descriptions)]

@app.route('/api/sorting/chat', methods=['POST'])
def sorting_chat():
    """分院帽对话"""
    data = request.json
    messages = data.get('messages', [])
    
    # 模拟对话逻辑
    response = generate_sorting_response(messages)
    
    return jsonify(response)

def generate_sorting_response(messages):
    """生成分院帽回复"""
    # 这里应该调用LLM API
    # 演示模式：返回预设回复
    
    user_messages = [m for m in messages if m['role'] == 'user']
    
    responses = [
        '嗯...很有趣。告诉我，你最看重的品质是什么？',
        '我明白了...但还需要了解更多。面对危险，你会怎么做？',
        '分院帽的视野越来越清晰了。你希望别人记住你什么？',
        '这是一个艰难的选择...你更看重个人成就还是集体荣誉？',
        '嗯...我看到了你的内心深处。我决定了！'
    ]
    
    # 简单的进度判断
    progress = len(user_messages)
    
    response = {
        'message': responses[progress % len(responses)],
        'sorted': progress >= 4
    }
    
    if response['sorted']:
        # 简单的分院逻辑（实际应该基于对话内容分析）
        houses = ['格兰芬多', '斯莱特林', '拉文克劳', '赫奇帕奇']
        selected_house = houses[progress % 4]
        
        response['result'] = {
            'house': selected_house,
            'description': f'{selected_house}是最适合你的学院！你的特质与这里的精神完美契合。',
            'traits': [
                {'icon': '⚔️', 'name': '勇敢'},
                {'icon': '💪', 'name': '坚韧'},
                {'icon': '🔥', 'name': '热情'},
                {'icon': '⭐', 'name': '领导力'}
            ]
        }
    
    return response

@app.route('/api/characters/chat', methods=['POST'])
def character_chat():
    """角色对话"""
    data = request.json
    character_id = data.get('characterId')
    messages = data.get('messages', [])
    
    # 模拟RAG响应
    response = generate_character_response(character_id, messages)
    
    return jsonify(response)

def generate_character_response(character_id, messages):
    """生成角色回复（模拟RAG）"""
    # 这里应该：
    # 1. 从向量数据库检索相关台词和设定
    # 2. 将检索结果作为上下文输入LLM
    # 3. LLM生成符合角色性格的回复
    
    # 角色性格设定
    character_profiles = {
        'dumbledore': {
            'tone': '智慧、温和、深思熟虑',
            'keywords': ['选择', '爱', '勇气', '智慧']
        },
        'snape': {
            'tone': '冷漠、严厉、复杂',
            'keywords': ['魔药学', '背叛', '忠诚', '莉莉']
        },
        'hermione': {
            'tone': '聪明、热情、好学',
            'keywords': ['学习', '书本', '知识', '朋友']
        },
        'voldemort': {
            'tone': '傲慢、冷酷、无情',
            'keywords': ['永生', '权力', '死亡', '预言']
        }
    }
    
    profile = character_profiles.get(character_id, character_profiles['dumbledore'])
    
    # 演示模式：基于角色性格生成回复
    user_last_message = [m['content'] for m in messages if m['role'] == 'user'][-1]
    
    responses = {
        'dumbledore': f'这是一个很好的问题，年轻人。在魔法世界里，{profile.keywords[0]}是非常重要的品质。记住，决定我们成为什么样人的，不是我们的能力，而是我们的选择。',
        'snape': f'哼...{profile.keywords[1]}...你真的理解这个词的含义吗？在魔药学的世界里，精确和耐心是成功的关键。',
        'hermione': f'太好了！这也是我一直想知道的问题。{profile.keywords[0]}是掌握魔法的基础。我可以推荐几本这方面的书给你！',
        'voldemort': f'只有弱者才问这样的问题。{profile.keywords[1]}才是永恒的追求。你...还有资格与我对话吗？'
    }
    
    return {
        'message': responses.get(character_id, '我理解你的意思。')
    }

@app.route('/api/spells/recognize', methods=['POST'])
def recognize_spell():
    """语音识别咒语"""
    data = request.json
    
    # 这里应该：
    # 1. 接收音频文件
    # 2. 使用Whisper等API进行语音识别
    # 3. 对比标准发音，计算准确度
    
    spell_id = data.get('spellId')
    audio_data = data.get('audioData')
    
    # 演示模式：返回模拟评分
    import random
    score = random.randint(70, 95)
    
    feedbacks = {
        90: '完美！你的发音非常标准，堪比霍格沃茨教授！',
        80: '很好！注意尾音要更加饱满一些。',
        70: '还不错，多练习几次就会更好。'
    }
    
    feedback = '继续加油！注意每个音节都要清晰。'
    for threshold, msg in sorted(feedbacks.items(), reverse=True):
        if score >= threshold:
            feedback = msg
            break
    
    return jsonify({
        'score': score,
        'feedback': feedback,
        'transcript': 'Lumos'  # 识别出的文本
    })

@app.route('/api/puzzles/check', methods=['POST'])
def check_puzzle():
    """检查谜题答案"""
    data = request.json
    puzzle_id = data.get('puzzleId')
    user_answer = data.get('answer')
    
    # 正确答案库
    correct_answers = {
        1: ['风', 'wind', '微风'],
        2: ['独角兽', '飞马', 'unicorn', 'pegasus'],
        3: ['魔药', 'potion'],
        4: ['镜子', '魔镜', '厄里斯魔镜', 'mirror'],
        5: ['时间转换器', '时间器', 'time turner'],
        6: ['老三', '第三个兄弟'],
        7: ['爱', 'love']
    }
    
    correct = correct_answers.get(puzzle_id, [])
    is_correct = any(user_answer.lower().strip() == ans.lower() for ans in correct)
    
    return jsonify({
        'correct': is_correct,
        'explanation': get_puzzle_explanation(puzzle_id)
    })

def get_puzzle_explanation(puzzle_id):
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

# 用户数据管理
@app.route('/api/user/data', methods=['GET'])
def get_user_data():
    """获取用户数据"""
    user_id = request.args.get('userId', 'default')
    user_data = users_db.get(user_id, {
        'house': '',
        'wand': None,
        'unlockedSpells': [],
        'puzzleProgress': 0
    })
    return jsonify(user_data)

@app.route('/api/user/data', methods=['POST'])
def save_user_data():
    """保存用户数据"""
    user_id = request.args.get('userId', 'default')
    data = request.json
    
    if user_id not in users_db:
        users_db[user_id] = {}
    
    users_db[user_id].update(data)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
