"""
AI 服务集成模块
集成 OpenAI、Whisper、语音合成等AI服务
"""

import os
from typing import List, Dict, Optional
import openai
import anthropic

from dotenv import load_dotenv

load_dotenv()

# 初始化 AI 客户端
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

if OPENAI_API_KEY:
    openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    openai_client = None
    print("警告: OPENAI_API_KEY 未设置，AI功能将使用模拟模式")

if ANTHROPIC_API_KEY:
    anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
else:
    anthropic_client = None


class OpenAIService:
    """OpenAI API 服务封装"""
    
    def __init__(self):
        self.client = openai_client
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o-mini",
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """聊天补全"""
        if not self.client:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API 错误: {e}")
            return None
    
    def speech_to_text(self, audio_file) -> Optional[Dict]:
        """语音转文字（Whisper）"""
        if not self.client:
            return None
        
        try:
            transcript = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            return {
                'text': transcript.text,
                'duration': getattr(transcript, 'duration', 0)
            }
        except Exception as e:
            print(f"Whisper API 错误: {e}")
            return None
    
    def text_to_speech(self, text: str, voice: str = "alloy") -> Optional[bytes]:
        """文字转语音"""
        if not self.client:
            return None
        
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            return response.content
        except Exception as e:
            print(f"TTS API 错误: {e}")
            return None
    
    def image_generation(
        self,
        prompt: str,
        style: str = "vivid",
        size: str = "1024x1024"
    ) -> Optional[str]:
        """图像生成（DALL-E）"""
        if not self.client:
            return None
        
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                style=style,
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"DALL-E API 错误: {e}")
            return None


class AnthropicService:
    """Anthropic Claude API 服务封装"""
    
    def __init__(self):
        self.client = anthropic_client
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20241022",
        max_tokens: int = 500
    ) -> Optional[str]:
        """聊天补全"""
        if not self.client:
            return None
        
        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=messages
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API 错误: {e}")
            return None


class SortingHatChatService:
    """分院帽对话服务"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
    
    def chat(self, messages: List[Dict[str, str]]) -> Dict:
        """分院帽对话"""
        system_prompt = """你是霍格沃茨的分院帽，已经服务了上千年。你的性格特征：
- 智慧、有洞察力、略带神秘
- 能看透人的内心深处
- 通过提问了解学生的性格
- 最终将学生分配到最适合的学院：格兰芬多（勇敢）、斯莱特林（野心）、拉文克劳（智慧）、赫奇帕奇（忠诚）
- 语气应该古老而慈祥，充满智慧

回答时要注意：
1. 一次只问一个问题
2. 问题要能帮助了解学生的性格和价值观
3. 大约3-5个问题后做出分院决定
4. 分院后给出理由和学院特点描述
5. 保持分院帽的神秘感和智慧形象

用户输入格式：{"role": "user", "content": "..."}
回答格式：普通对话文本，不要包含JSON格式"""

        # 添加系统提示
        messages_with_system = [{"role": "system", "content": system_prompt}] + messages
        
        response = self.openai_service.chat_completion(
            messages=messages_with_system,
            temperature=0.8
        )
        
        if response:
            # 简单判断是否完成分院
            user_messages = [m for m in messages if m['role'] == 'user']
            is_sorted = len(user_messages) >= 4 and any(
                house in response for house in ['格兰芬多', '斯莱特林', '拉文克劳', '赫奇帕奇']
            )
            
            return {
                'message': response,
                'sorted': is_sorted
            }
        
        # 模拟响应（当API不可用时）
        return self._simulate_response(messages)
    
    def _simulate_response(self, messages: List[Dict[str, str]]) -> Dict:
        """模拟响应（当API不可用时）"""
        user_messages = [m for m in messages if m['role'] == 'user']
        progress = len(user_messages)
        
        responses = [
            '嗯...又一个新生来到了霍格沃茨。让我好好看看你...告诉我，你觉得自己最大的优点是什么？',
            '嗯...很有趣。那么，面对危险，你会怎么做？',
            '我看到了...但还需要了解更多。你最珍视什么？',
            '分院帽的视野越来越清晰了。告诉我，你希望别人记住你什么？'
        ]
        
        if progress >= 4:
            houses = ['格兰芬多', '斯莱特林', '拉文克劳', '赫奇帕奇']
            selected_house = houses[progress % 4]
            return {
                'message': f'嗯...我决定了！{selected_house}！',
                'sorted': True,
                'result': {
                    'house': selected_house,
                    'description': f'{selected_house}是最适合你的学院！你的特质与这里的精神完美契合。',
                    'traits': [
                        {'icon': '⚔️', 'name': '勇敢'},
                        {'icon': '💪', 'name': '坚韧'},
                        {'icon': '🔥', 'name': '热情'},
                        {'icon': '⭐', 'name': '领导力'}
                    ]
                }
            }
        
        return {
            'message': responses[progress % len(responses)],
            'sorted': False
        }


class CharacterChatService:
    """角色对话服务（RAG架构）"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.character_profiles = {
            'dumbledore': {
                'name': '阿白思·邓布利多',
                'tone': '智慧、温和、深思熟虑',
                'keywords': ['选择', '爱', '勇气', '智慧', '死亡'],
                'personality': '霍格沃茨校长，最伟大的白巫师。他智慧、仁慈，对哈利关怀备至。说话温和而富有哲理，经常引用谚语。',
                'sample_dialogues': [
                    '决定我们成为什么样人的，不是我们的能力，而是我们的选择。',
                    '不要怜悯死者，哈利。怜悯活着的人，最重要的是，怜悯那些生活中没有爱的人。',
                    '对于那些等待死亡的人来说，死亡只是另一场伟大的冒险。'
                ]
            },
            'snape': {
                'name': '西弗勒斯·斯内普',
                'tone': '冷漠、严厉、复杂',
                'keywords': ['魔药学', '背叛', '忠诚', '莉莉', '黑魔法'],
                'personality': '斯莱特林学院院长，魔药课大师。外表冷漠严厉，内心却隐藏着对莉莉的深深爱意和对哈利的复杂情感。',
                'sample_dialogues': [
                    'Always。',
                    '你是个很傲慢的男孩，波特。',
                    '你的父亲也不是什么好东西。'
                ]
            },
            'hermione': {
                'name': '赫敏·格兰杰',
                'tone': '聪明、热情、好学',
                'keywords': ['学习', '书本', '知识', '朋友', '逻辑'],
                'personality': '最聪明的女巫，以超常的智慧和勤奋著称。对魔法知识有着近乎狂热的追求，是哈利最可靠的朋友。',
                'sample_dialogues': [
                    '书本！还有聪明！但还有更多重要的东西——友谊和勇气。',
                    '这连最笨的人也知道，海格！那是巨怪！',
                    '我可是花了几个星期在图书馆里查到的！'
                ]
            },
            'voldemort': {
                'name': '伏地魔',
                'tone': '傲慢、冷酷、无情',
                'keywords': ['永生', '权力', '死亡', '预言', '黑魔法'],
                'personality': '历史上最危险的黑巫师，追求永生和权力。他的名字被人们恐惧地称为"那个人"。极端自私，不懂得爱的力量。',
                'sample_dialogues': [
                    '世上没有善恶，只有权力，还有那些太软弱而无法追求它的人。',
                    '哈利·波特...那个大难不死的男孩。',
                    '只有一个能活下来。'
                ]
            }
        }
    
    def chat(self, character_id: str, messages: List[Dict[str, str]]) -> Dict:
        """角色对话"""
        profile = self.character_profiles.get(character_id)
        if not profile:
            profile = self.character_profiles['dumbledore']
        
        system_prompt = f"""你是哈利波特故事中的角色：{profile['name']}。

角色特征：
- 语气：{profile['tone']}
- 性格：{profile['personality']}
- 关键词：{', '.join(profile['keywords'])}

经典台词示例：
{chr(10).join(f"- {q}" for q in profile['sample_dialogues'])}

对话要求：
1. 完全保持角色的性格和说话方式
2. 回答要符合角色的世界观和价值观
3. 可以引用角色相关的剧情和设定
4. 不要出现不符合角色性格的言论
5. 语言风格要与角色一致（邓布利多温和哲理，斯内普冷漠尖刻，赫敏聪明热情，伏地魔傲慢冷酷）
6. 使用中文回答，保持角色的中文翻译风格

用户输入：{{user_message}}
请以角色的身份回答。"""

        messages_with_system = [{"role": "system", "content": system_prompt}] + messages
        
        response = self.openai_service.chat_completion(
            messages=messages_with_system,
            temperature=0.7
        )
        
        return {
            'message': response or self._simulate_response(character_id, messages)
        }
    
    def _simulate_response(self, character_id: str, messages: List[Dict[str, str]]) -> str:
        """模拟响应（当API不可用时）"""
        profile = self.character_profiles.get(character_id, self.character_profiles['dumbledore'])
        user_last_message = [m['content'] for m in messages if m['role'] == 'user'][-1] if messages else ''
        
        responses = {
            'dumbledore': f'这是一个很好的问题，年轻人。在魔法世界里，{profile["keywords"][0]}是非常重要的品质。记住，决定我们成为什么样人的，不是我们的能力，而是我们的选择。',
            'snape': f'哼...{profile["keywords"][2]}...你真的理解这个词的含义吗？在魔药学的世界里，精确和耐心是成功的关键。',
            'hermione': f'太好了！这也是我一直想知道的问题。{profile["keywords"][0]}是掌握魔法的基础。我可以推荐几本这方面的书给你！',
            'voldemort': f'只有弱者才问这样的问题。{profile["keywords"][0]}才是永恒的追求。你...还有资格与我对话吗？'
        }
        
        return responses.get(character_id, '我理解你的意思。')


class SpellRecognitionService:
    """咒语识别服务"""
    
    def __init__(self):
        self.openai_service = OpenAIService()
        self.spell_database = {
            'lumos': {
                'name': '荧光闪烁',
                'correct_pronunciation': 'LOO-mos',
                'common_mistakes': ['loo-mos', 'lu-mos', 'lumus']
            },
            'expelliarmus': {
                'name': '缴械咒',
                'correct_pronunciation': 'ex-pell-ee-AR-mus',
                'common_mistakes': ['ex-pelli-armus', 'expelliarmus', 'ex-pel-lee-armus']
            },
            'stupefy': {
                'name': '昏迷咒',
                'correct_pronunciation': 'STOO-puh-fy',
                'common_mistakes': ['stupid-fy', 'stu-pe-fy', 'stupy']
            },
            'protego': {
                'name': '护盾咒',
                'correct_pronunciation': 'pro-TAY-go',
                'common_mistakes': ['prot-go', 'pro-tego', 'pro-tay-go']
            },
            'wingardium': {
                'name': '漂浮咒',
                'correct_pronunciation': 'win-GAR-dee-um Lev-ee-O-sa',
                'common_mistakes': ['wingardium leviosa', 'win-gar-dium', 'wingardium leviosa']
            },
            'accio': {
                'name': '召唤咒',
                'correct_pronunciation': 'AK-ee-oh',
                'common_mistakes': ['acio', 'a-ki-oh', 'akio']
            }
        }
    
    def recognize(self, spell_id: str, audio_data: bytes) -> Dict:
        """识别咒语发音"""
        spell_info = self.spell_database.get(spell_id)
        if not spell_info:
            return {
                'success': False,
                'error': 'Unknown spell'
            }
        
        # 实际项目中，这里应该：
        # 1. 将音频数据保存为临时文件
        # 2. 调用 Whisper API 进行语音识别
        # 3. 对比识别结果和标准发音
        # 4. 计算相似度并给出评分
        
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
        
        return {
            'success': True,
            'score': score,
            'feedback': feedback,
            'transcript': spell_info['correct_pronunciation'],
            'improvements': self._get_improvements(spell_id, score)
        }
    
    def _get_improvements(self, spell_id: str, score: int) -> List[str]:
        """获取改进建议"""
        if score >= 90:
            return []
        
        improvements = [
            '注意元音的饱满度',
            '确保每个音节都清晰',
            '保持语速适中，不要太快',
            '注意重音位置'
        ]
        
        return improvements[:3]


# 导出服务实例
openai_service = OpenAIService()
anthropic_service = AnthropicService()
sorting_hat_service = SortingHatChatService()
character_chat_service = CharacterChatService()
spell_recognition_service = SpellRecognitionService()
