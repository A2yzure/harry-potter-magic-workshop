"""
数据持久化模块
使用 JSON 文件存储用户数据
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

class Database:
    """JSON 文件数据库"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, 'users.json')
        self.wands_file = os.path.join(data_dir, 'wands.json')
        self.spells_file = os.path.join(data_dir, 'spells.json')
        self.dialogues_file = os.path.join(data_dir, 'dialogues.json')
        self.puzzles_file = os.path.join(data_dir, 'puzzles.json')
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 初始化数据文件
        self._init_file(self.users_file, {})
        self._init_file(self.wands_file, [])
        self._init_file(self.spells_file, [])
        self._init_file(self.dialogues_file, [])
        self._init_file(self.puzzles_file, {})
    
    def _init_file(self, filepath: str, default_data: Any):
        """初始化数据文件"""
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(default_data, f, ensure_ascii=False, indent=2)
    
    def _read_json(self, filepath: str) -> Any:
        """读取 JSON 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"读取文件错误 {filepath}: {e}")
            return {} if '.json' in filepath else []
    
    def _write_json(self, filepath: str, data: Any):
        """写入 JSON 文件"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"写入文件错误 {filepath}: {e}")
    
    # 用户数据操作
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取用户数据"""
        users = self._read_json(self.users_file)
        return users.get(user_id)
    
    def create_user(self, user_id: str, user_data: Dict[str, Any]) -> bool:
        """创建用户"""
        users = self._read_json(self.users_file)
        if user_id in users:
            return False
        
        user_data['created_at'] = datetime.now().isoformat()
        user_data['updated_at'] = datetime.now().isoformat()
        users[user_id] = user_data
        self._write_json(self.users_file, users)
        return True
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """更新用户数据"""
        users = self._read_json(self.users_file)
        if user_id not in users:
            return False
        
        users[user_id].update(updates)
        users[user_id]['updated_at'] = datetime.now().isoformat()
        self._write_json(self.users_file, users)
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """删除用户"""
        users = self._read_json(self.users_file)
        if user_id not in users:
            return False
        
        del users[user_id]
        self._write_json(self.users_file, users)
        return True
    
    def get_all_users(self) -> Dict[str, Any]:
        """获取所有用户"""
        return self._read_json(self.users_file)
    
    # 魔杖数据操作
    def save_wand(self, user_id: str, wand_data: Dict[str, Any]) -> bool:
        """保存魔杖数据"""
        wands = self._read_json(self.wands_file)
        
        wand_entry = {
            'user_id': user_id,
            'wand': wand_data,
            'created_at': datetime.now().isoformat()
        }
        
        wands.append(wand_entry)
        self._write_json(self.wands_file, wands)
        
        # 同时更新用户数据
        self.update_user(user_id, {'wand': wand_data})
        return True
    
    def get_user_wands(self, user_id: str) -> list:
        """获取用户的所有魔杖"""
        wands = self._read_json(self.wands_file)
        return [w['wand'] for w in wands if w['user_id'] == user_id]
    
    # 咒语数据操作
    def unlock_spell(self, user_id: str, spell_id: str) -> bool:
        """解锁咒语"""
        spells = self._read_json(self.spells_file)
        
        spell_entry = {
            'user_id': user_id,
            'spell_id': spell_id,
            'unlocked_at': datetime.now().isoformat()
        }
        
        spells.append(spell_entry)
        self._write_json(self.spells_file, spells)
        
        # 更新用户的解锁列表
        user = self.get_user(user_id) or {}
        unlocked_spells = user.get('unlockedSpells', [])
        if spell_id not in unlocked_spells:
            unlocked_spells.append(spell_id)
            self.update_user(user_id, {'unlockedSpells': unlocked_spells})
        
        return True
    
    def get_user_spells(self, user_id: str) -> list:
        """获取用户已解锁的咒语"""
        spells = self._read_json(self.spells_file)
        return [s['spell_id'] for s in spells if s['user_id'] == user_id]
    
    def save_spell_score(self, user_id: str, spell_id: str, score: int) -> bool:
        """保存咒语练习成绩"""
        user = self.get_user(user_id) or {}
        spell_scores = user.get('spellScores', {})
        spell_scores[spell_id] = score
        self.update_user(user_id, {'spellScores': spell_scores})
        return True
    
    # 对话记录操作
    def save_dialogue(self, user_id: str, character_id: str, messages: list) -> bool:
        """保存对话记录"""
        dialogues = self._read_json(self.dialogues_file)
        
        dialogue_entry = {
            'user_id': user_id,
            'character_id': character_id,
            'messages': messages,
            'created_at': datetime.now().isoformat()
        }
        
        dialogues.append(dialogue_entry)
        self._write_json(self.dialogues_file, dialogues)
        return True
    
    def get_user_dialogues(self, user_id: str) -> list:
        """获取用户的所有对话记录"""
        dialogues = self._read_json(self.dialogues_file)
        return [d for d in dialogues if d['user_id'] == user_id]
    
    # 谜题进度操作
    def update_puzzle_progress(self, user_id: str, level: int) -> bool:
        """更新谜题进度"""
        puzzles = self._read_json(self.puzzles_file)
        
        if user_id not in puzzles:
            puzzles[user_id] = {
                'completed_levels': [],
                'current_level': 1,
                'scores': {}
            }
        
        if level not in puzzles[user_id]['completed_levels']:
            puzzles[user_id]['completed_levels'].append(level)
        
        puzzles[user_id]['current_level'] = max(
            puzzles[user_id]['current_level'],
            level + 1
        )
        
        self._write_json(self.puzzles_file, puzzles)
        
        # 更新用户数据
        self.update_user(user_id, {
            'puzzleProgress': puzzles[user_id]['current_level']
        })
        
        return True
    
    def get_puzzle_progress(self, user_id: str) -> Dict[str, Any]:
        """获取谜题进度"""
        puzzles = self._read_json(self.puzzles_file)
        return puzzles.get(user_id, {
            'completed_levels': [],
            'current_level': 1,
            'scores': {}
        })
    
    # 统计数据
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计数据"""
        users = self._read_json(self.users_file)
        wands = self._read_json(self.wands_file)
        spells = self._read_json(self.spells_file)
        dialogues = self._read_json(self.dialogues_file)
        
        # 统计学院分布
        house_counts = {'格兰芬多': 0, '斯莱特林': 0, '拉文克劳': 0, '赫奇帕奇': 0, '': 0}
        for user in users.values():
            house = user.get('house', '')
            if house in house_counts:
                house_counts[house] += 1
            else:
                house_counts[''] += 1
        
        return {
            'total_users': len(users),
            'total_wands': len(wands),
            'total_spell_unlocks': len(spells),
            'total_dialogues': len(dialogues),
            'house_distribution': house_counts
        }


# 创建数据库实例
db = Database()
