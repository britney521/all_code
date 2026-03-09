#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
喜马拉雅都市分类自动检测更新程序
基于现有新品榜.py的Playwright操作和验证码处理逻辑
自动检测榜单更新并将新增章节数据写入Excel表格
支持用户选择浏览器路径和Excel文件路径
"""

import json
import random
import time
import re
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

# Playwright相关导入
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext


# GUI相关导入
import tkinter as tk
from tkinter import filedialog, messagebox

# 日志记录
import logging
import sqlite3
from contextlib import contextmanager
from difflib import SequenceMatcher

# 配置日志 - 确保日志文件保存在程序同级目录
# 处理打包后的exe环境：使用sys.executable获取exe文件路径
if getattr(sys, 'frozen', False):
    # 打包后的exe环境
    script_dir = os.path.dirname(sys.executable)
else:
    # 开发环境
    script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, '都市分类自动检测更新.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def is_browser_closed_error(error_str):
    """检测是否为浏览器关闭相关的错误"""
    closed_keywords = [
        "Target page, context or browser has been closed",
        "browser has been closed",
        "context has been closed",
        "page has been closed"
    ]
    return any(keyword in str(error_str) for keyword in closed_keywords)

def handle_browser_closed_error(logger, browser, context, page):
    """处理浏览器关闭错误，尝试重新创建浏览器实例"""
    try:
        logger.warning("检测到浏览器关闭错误，尝试重新创建浏览器实例...")
        
        # 关闭现有的浏览器实例（如果还存在）
        try:
            if page and hasattr(page, 'is_closed') and not page.is_closed():
                page.close()
        except:
            pass
        
        try:
            if context:
                context.close()
        except:
            pass
        
        try:
            if browser:
                browser.close()
        except:
            pass
        
        # 重新创建浏览器实例
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = context.new_page()
        
        # 导航到榜单页面
        page.goto('https://www.ximalaya.com/top/', timeout=90000)
        page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)
        
        logger.info("浏览器实例重新创建成功")
        return browser, context, page, True
        
    except Exception as e:
        logger.error(f"重新创建浏览器实例失败: {e}")
        return None, None, None, False

# 定义所有分类选择器
SUBCATEGORIES = [
    {
        "name": "热门",
        "href": "/top/2/100077/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100077/"]',
            'a.sub-link[href="/top/2/100077/"]',
            'a[href="/top/2/100077/"]'
        ]
    },
    {
        "name": "新品",
        "href": "/top/2/100157/",
        "selectors": [
            'a[class="sub-link  _MR"][href="/top/2/100157/"]',  # 注意：sub-link后面有两个空格
            'a.sub-link._MR[href="/top/2/100157/"]',
            'a.sub-link[href="/top/2/100157/"]',
            'a[href="/top/2/100157/"]',
            'a.sub-link._MR:has-text("新品")',
            'a.sub-link:has-text("新品")',
            'a:has-text("新品")',
            'a[class*="sub-link"][href="/top/2/100157/"]'  # 使用包含匹配
        ]
    },
    {
        "name": "免费",
        "href": "/top/2/100224/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100224/"]',
            'a.sub-link[href="/top/2/100224/"]',
            'a[href="/top/2/100224/"]',
            'a.sub-link._MR:has-text("免费")',
            'a.sub-link:has-text("免费")',
            'a:has-text("免费")'
        ]
    },
    {
        "name": "口碑",
        "href": "/top/2/100191/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100191/"]',
            'a.sub-link[href="/top/2/100191/"]',
            'a[href="/top/2/100191/"]',
            'a.sub-link._MR:has-text("口碑")',
            'a.sub-link:has-text("口碑")',
            'a:has-text("口碑")'
        ]
    },
    {
        "name": "月票",
        "href": "/top/2/100332/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100332/"]',
            'a.sub-link[href="/top/2/100332/"]',
            'a[href="/top/2/100332/"]',
            'a.sub-link._MR:has-text("月票")',
            'a.sub-link:has-text("月票")',
            'a:has-text("月票")'
        ]
    },
    {
        "name": "男生",
        "href": "/top/2/100330/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100330/"]',
            'a.sub-link[href="/top/2/100330/"]',
            'a[href="/top/2/100330/"]',
            'a.sub-link._MR:has-text("男生")',
            'a.sub-link:has-text("男生")',
            'a:has-text("男生")'
        ]
    },
    {
        "name": "都市",
        "href": "/top/2/100078/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100078/"]',
            'a.sub-link[href="/top/2/100078/"]',
            'a[href="/top/2/100078/"]',
            'a.sub-link._MR:has-text("都市")',
            'a.sub-link:has-text("都市")',
            'a:has-text("都市")'
        ]
    },
    {
        "name": "玄幻",
        "href": "/top/2/100079/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100079/"]',
            'a.sub-link[href="/top/2/100079/"]',
            'a[href="/top/2/100079/"]',
            'a.sub-link._MR:has-text("玄幻")',
            'a.sub-link:has-text("玄幻")',
            'a:has-text("玄幻")'
        ]
    },
    {
        "name": "悬疑",
        "href": "/top/2/100080/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100080/"]',
            'a.sub-link[href="/top/2/100080/"]',
            'a[href="/top/2/100080/"]',
            'a.sub-link._MR:has-text("悬疑")',
            'a.sub-link:has-text("悬疑")',
            'a:has-text("悬疑")'
        ]
    },
    {
        "name": "历史",
        "href": "/top/2/100081/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100081/"]',
            'a.sub-link[href="/top/2/100081/"]',
            'a[href="/top/2/100081/"]',
            'a.sub-link._MR:has-text("历史")',
            'a.sub-link:has-text("历史")',
            'a:has-text("历史")'
        ]
    },
    {
        "name": "科幻",
        "href": "/top/2/100082/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100082/"]',
            'a.sub-link[href="/top/2/100082/"]',
            'a[href="/top/2/100082/"]',
            'a.sub-link._MR:has-text("科幻")',
            'a.sub-link:has-text("科幻")',
            'a:has-text("科幻")'
        ]
    },
    {
        "name": "游戏",
        "href": "/top/2/100083/",
        "selectors": [
            'a.sub-link._MR[href="/top/2/100083/"]',
            'a.sub-link[href="/top/2/100083/"]',
            'a[href="/top/2/100083/"]',
            'a.sub-link._MR:has-text("游戏")',
            'a.sub-link:has-text("游戏")',
            'a:has-text("游戏")'
        ]
    }
]

# 全局配置
CONFIG = {
    'excel_file_path': '',  # 将由用户输入指定
    'browser_path': '',  # 将由用户选择指定
    'data_folder_path': script_dir,  # 默认使用程序同级目录存储
    'base_url': 'https://www.ximalaya.com/top/',  # 榜单首页
    'headless': False,  # 设置为False以便处理验证码
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'viewport': {'width': 1920, 'height': 1080},
    'timeout': 10000,  # 10秒超时（优化：进一步减少到10秒）
    'delay_range': (0.5, 1.5),  # 人工延迟范围（秒）（优化：减少到0.5-1.5秒）
    'max_retries': 2,  # 最大重试次数（优化：减少到2次）
}


class DatabaseManager:
    """数据库管理类，负责SQLite数据库的初始化和操作"""
    
    def __init__(self, db_path: str = None):
        """初始化数据库管理器"""
        if db_path is None:
            # 默认数据库路径 - 使用程序同级目录
            # 处理打包后的exe环境：使用sys.executable获取exe文件路径
            if getattr(sys, 'frozen', False):
                # 打包后的exe环境
                script_dir = os.path.dirname(sys.executable)
            else:
                # 开发环境
                script_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(script_dir, 'ximalaya_novels.db')
        else:
            self.db_path = db_path
        
        # 为内存数据库保持持久连接
        self._memory_conn = None
        if self.db_path == ":memory:":
            self._memory_conn = sqlite3.connect(self.db_path)
            self._memory_conn.row_factory = sqlite3.Row
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        if self._memory_conn is not None:
            # 对于内存数据库，使用持久连接
            yield self._memory_conn
        else:
            # 对于文件数据库，创建新连接
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # 使查询结果可以通过列名访问
            try:
                yield conn
            finally:
                conn.close()
    
    def init_database(self):
        """初始化数据库表结构 - 按日期保存模式"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # 创建分类表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # 创建小说基本信息表（用于生成唯一ID）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS novel_master (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    novel_title TEXT NOT NULL,
                    anchor_name TEXT,
                    first_seen_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(novel_title, anchor_name)
                )
            ''')

            # 检查novel_details表是否已存在
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name='novel_details'
            """)
            table_exists = cursor.fetchone()

            if table_exists:
                # 检查是否有正确的UNIQUE约束
                cursor.execute("""
                    SELECT sql FROM sqlite_master
                    WHERE type='table' AND name='novel_details'
                """)
                table_sql = cursor.fetchone()

                if table_sql and 'UNIQUE(note_id, crawl_date, category_id)' not in table_sql[0]:
                    logger.info("发现novel_details表缺少必要的UNIQUE约束，正在迁移...")
                    # 重新创建表结构
                    cursor.execute('DROP TABLE IF EXISTS novel_details')
                    logger.info("已删除旧的novel_details表")

            # 创建小说详情表
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS novel_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER NOT NULL,
                    novel_title TEXT NOT NULL,
                    category_id INTEGER,
                    rank_position INTEGER,
                    total_plays TEXT,
                    anchor_name TEXT,
                    chapter_count INTEGER DEFAULT 0,
                    comments_count TEXT,
                    fans_count TEXT,
                    novel_url TEXT,
                    crawl_date DATE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (note_id) REFERENCES novel_master (note_id),
                    UNIQUE(note_id, crawl_date, category_id)
                )
            ''')

            # 创建章节详情表（按年月日命名）
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS chapter_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    note_id INTEGER NOT NULL,
                    novel_title TEXT NOT NULL,
                    anchor_name TEXT,
                    category_id INTEGER,
                    chapter_title TEXT NOT NULL,
                    chapter_plays TEXT,
                    publish_time TEXT,
                    chapter_url TEXT,
                    crawl_date DATE NOT NULL,
                     chapter_order_type TEXT CHECK (chapter_order_type IN ('ASC', 'DESC')) DEFAULT 'ASC',
                    detail_publish_time TEXT,
                    detail_title TEXT,
                    duration TEXT,
                    detail_play_count TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (note_id) REFERENCES novel_master (note_id)
                )
            ''')

            # 检查并添加新字段（数据库升级逻辑）
            try:
                # 获取表结构信息
                cursor.execute("PRAGMA table_info(chapter_details)")
                columns = [column[1] for column in cursor.fetchall()]

                # 检查并添加新字段
                new_fields = [
                    ('detail_publish_time', 'TEXT'),
                    ('detail_title', 'TEXT'),
                    ('duration', 'TEXT'),
                    ('detail_play_count', 'TEXT')
                ]

                for field_name, field_type in new_fields:
                    if field_name not in columns:
                        cursor.execute(f'ALTER TABLE chapter_details ADD COLUMN {field_name} {field_type}')
                        logger.info(f"已添加新字段: {field_name}")

            except sqlite3.Error as e:
                logger.error(f"数据库升级失败: {e}")


            conn.commit()
            logger.info(f"数据库初始化完成 - 按日期保存模式: {self.db_path}")
    
    def get_or_create_category(self, category_name: str) -> int:
        """获取或创建分类，返回分类ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 尝试获取现有分类
            cursor.execute('SELECT id FROM categories WHERE category_name = ?', (category_name,))
            result = cursor.fetchone()
            
            if result:
                return result['id']
            
            # 创建新分类
            cursor.execute(
                'INSERT INTO categories (category_name) VALUES (?)',
                (category_name,)
            )
            conn.commit()
            return cursor.lastrowid
    
    def generate_unique_novel_id(self, note_id: int) -> str:
        """根据note_id生成格式化的唯一小说ID"""
        return f"NOVEL_{note_id:06d}"
    
    def get_unique_novel_id(self, novel_title: str, anchor_name: str = None) -> str:
        """获取小说的格式化唯一ID"""
        note_id = self.get_or_create_note_id(novel_title, anchor_name)
        return self.generate_unique_novel_id(note_id) if note_id else None
    
    def get_or_create_note_id(self, novel_title: str, anchor_name: str = None, crawl_date: str = None) -> int:
        """获取或创建小说的唯一note_id"""
        if crawl_date is None:
            crawl_date = datetime.now().strftime('%Y-%m-%d')
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # 先尝试根据title和author查找现有的note_id
            if anchor_name:
                cursor.execute(
                    'SELECT note_id FROM novel_master WHERE novel_title = ? AND anchor_name = ?',
                    (novel_title, anchor_name)
                )
            else:
                cursor.execute(
                    'SELECT note_id FROM novel_master WHERE novel_title = ? AND (anchor_name IS NULL OR anchor_name = "")',
                    (novel_title,)
                )
            
            result = cursor.fetchone()
            if result:
                return result['note_id']
            
            # 如果不存在，创建新的note_id
            try:
                cursor.execute(
                    'INSERT INTO novel_master (novel_title, anchor_name, first_seen_date) VALUES (?, ?, ?)',
                    (novel_title, anchor_name or '', crawl_date)
                )
                conn.commit()
                note_id = cursor.lastrowid
                unique_id = self.generate_unique_novel_id(note_id)
                logger.info(f"创建新小说ID: {novel_title} -> note_id={note_id}, unique_id={unique_id}")
                return note_id
            except sqlite3.IntegrityError:
                # 如果出现重复插入（并发情况），重新查询
                if anchor_name:
                    cursor.execute(
                        'SELECT note_id FROM novel_master WHERE novel_title = ? AND anchor_name = ?',
                        (novel_title, anchor_name)
                    )
                else:
                    cursor.execute(
                        'SELECT note_id FROM novel_master WHERE novel_title = ? AND (anchor_name IS NULL OR anchor_name = "")',
                        (novel_title,)
                    )
                result = cursor.fetchone()
                return result['note_id'] if result else None

    def insert_novel_detail(self, novel_data: dict, category_name: str,
                            crawl_date: str = None) -> int:
        """插入或更新小说详情（按天维度）"""
        if crawl_date is None:
            crawl_date = datetime.now().strftime('%Y-%m-%d')

        novel_title = novel_data.get('novel_title', '')
        anchor_name = novel_data.get('anchor_name', '')
        note_id = self.get_or_create_note_id(novel_title, anchor_name, crawl_date)
        category_id = self.get_or_create_category(category_name)
        # 插入更新
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO novel_details (
                    note_id, novel_title, category_id, rank_position, total_plays,
                    anchor_name, chapter_count, comments_count, fans_count,
                    novel_url, crawl_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(note_id, crawl_date, category_id) DO UPDATE SET
                    rank_position   = excluded.rank_position,
                    total_plays     = excluded.total_plays,
                    chapter_count   = excluded.chapter_count,
                    comments_count  = excluded.comments_count,
                    fans_count      = excluded.fans_count,
                    novel_url       = excluded.novel_url,
                    created_at      = CURRENT_TIMESTAMP   
            """, (
                note_id,
                novel_title,
                category_id,
                novel_data.get('rank', ''),
                novel_data.get('total_plays', ''),
                anchor_name,
                novel_data.get('chapter_count', 0),
                novel_data.get('comments_count', ''),
                novel_data.get('fans_count', ''),
                novel_data.get('novel_url', ''),
                crawl_date
            ))
            conn.commit()

            logger.info(f"Upsert 小说详情 note_id={note_id}: {novel_title} - 日期: {crawl_date}")
            return note_id

    
    def insert_chapter_details(self, chapters: List[Dict], novel_title: str, chapter_order_type:str,category_id: int = None, crawl_date: str = None, anchor_name: str = None) -> int:
        """插入章节详情数据"""
        if not chapters:
            return 0
            
        if crawl_date is None:
            crawl_date = datetime.now().strftime('%Y-%m-%d')
        
        # 获取或创建小说的唯一note_id
        note_id = self.get_or_create_note_id(novel_title, anchor_name, crawl_date)

        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            
            inserted_count = 0
            for chapter in chapters:
                chapter_title = chapter.get('chapter_title', '')
                # ---------- 去重逻辑 ----------
                if chapter_order_type.upper() == 'ASC':
                    # 正序：只看小说+章节名，任意日期出现即重复
                    cursor.execute("""
                                SELECT 1 FROM chapter_details
                                WHERE novel_title = ?
                                  AND chapter_title = ?
                                LIMIT 1
                            """, (novel_title, chapter_title))
                    if cursor.fetchone():
                        continue  # 已存在，跳过
                else:
                    # 正序：只看小说+章节名 日期出现即重复
                    cursor.execute("""
                                                    SELECT 1 FROM chapter_details
                                                    WHERE novel_title = ?
                                                      AND chapter_title = ?
                                                      AND crawl_date = ?
                                                    LIMIT 1
                                                """, (novel_title, chapter_title,crawl_date))
                    if cursor.fetchone():
                        continue  # 已存在，跳过
                try:
                    cursor.execute(f'''
                        INSERT INTO chapter_details (
                            note_id, novel_title, anchor_name, category_id, chapter_title,
                            chapter_plays, publish_time, chapter_url, crawl_date,chapter_order_type,
                            detail_publish_time, detail_title, duration, detail_play_count
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        note_id,
                        novel_title,
                        anchor_name or chapter.get('anchor_name', ''),
                        category_id,
                        chapter.get('title', chapter.get('chapter_title', '')),  # 兼容两种字段名
                        chapter.get('plays', chapter.get('chapter_plays', '')),  # 兼容两种字段名
                        chapter.get('publish_time', ''),
                        chapter.get('url', chapter.get('chapter_url', '')),  # 兼容两种字段名
                        crawl_date,
                        chapter_order_type,
                        chapter.get('detail_publish_time', ''),  # 章节详情页的上架时间
                        chapter.get('detail_title', ''),  # 章节详情页的标题
                        chapter.get('duration', ''),  # 播放时长
                        chapter.get('detail_play_count', '')  # 章节详情页的播放量
                    ))
                    inserted_count += 1
                except sqlite3.Error as e:
                    logger.error(f"插入章节详情失败: {e}")
            
            conn.commit()
            logger.info(f"插入章节详情: {novel_title} - {inserted_count}章 - 日期: {crawl_date}")
            return inserted_count






def select_browser_path():
    """选择浏览器可执行文件路径"""
    try:
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()

        # 显示文件选择对话框
        browser_path = filedialog.askopenfilename(
            title="选择浏览器可执行文件",
            filetypes=[
                ("Chrome浏览器", "chrome.exe"),
                ("Edge浏览器", "msedge.exe"),
                ("Firefox浏览器", "firefox.exe"),
                ("所有可执行文件", "*.exe"),
                ("所有文件", "*.*")
            ],
            initialdir="C:/Program Files"
        )

        root.destroy()

        if browser_path:
            logger.info(f"用户选择的浏览器路径: {browser_path}")
            return browser_path
        else:
            logger.warning("用户未选择浏览器路径，将使用默认浏览器")
            return None

    except Exception as e:
        logger.error(f"选择浏览器路径失败: {e}")
        return None


def select_data_folder_path():
    """选择小说数据存储文件夹路径"""
    try:
        # 创建隐藏的根窗口
        root = tk.Tk()
        root.withdraw()

        # 显示文件夹选择对话框
        folder_path = filedialog.askdirectory(
            title="选择小说数据存储文件夹",
            initialdir="D:/外包/喜马拉雅"
        )

        root.destroy()

        if folder_path:
            logger.info(f"用户选择的数据存储路径: {folder_path}")
            return folder_path
        else:
            logger.warning("用户未选择数据存储路径")
            return None

    except Exception as e:
        logger.error(f"选择数据存储路径失败: {e}")
        return None



def create_novel_folder(base_dir, novel_title):
    """为单个小说创建文件夹"""
    try:
        # 清理小说标题中的非法字符 - Windows不支持的字符: < > : " | ? * \ /
        # 同时移除其他可能导致问题的字符
        invalid_chars = '<>:"|?*\\/'
        safe_title = "".join(c for c in novel_title if c not in invalid_chars)
        # 进一步清理，只保留字母数字、中文、空格、连字符和下划线
        safe_title = "".join(c for c in safe_title if c.isalnum() or c in (' ', '-', '_') or '\u4e00' <= c <= '\u9fff').strip()
        
        # 如果清理后为空，使用默认名称
        if not safe_title:
            safe_title = "未知小说"
        
        # 限制文件夹名称长度，避免路径过长
        if len(safe_title) > 100:
            safe_title = safe_title[:100]
            
        novel_folder = os.path.join(base_dir, safe_title)
        
        if not os.path.exists(novel_folder):
            os.makedirs(novel_folder)
            logger.info(f"创建小说文件夹: {novel_folder}")
        
        return novel_folder
    except Exception as e:
        logger.error(f"创建小说文件夹失败: {e}")
        raise



def show_program_menu():
    """显示程序操作菜单"""
    print("\n" + "=" * 50)
    print("    喜马拉雅热播榜自动检测更新程序")
    print("=" * 50)
    print("程序功能:")
    print("- 自动检测热播榜更新")
    print("- 爬取新增章节数据")
    print("- 更新数据库")
    print("- 智能验证码处理")
    print("=" * 50)
    print("操作说明:")
    print("1. 程序将自动打开浏览器")
    print("2. 请手动扫码登录喜马拉雅")
    print("3. 程序将自动执行检测和更新")
    print("4. 可随时按 Ctrl+C 停止程序")
    print("=" * 50)

def show_category_menu():
    """显示分类选择菜单"""
    print("\n" + "=" * 50)
    print("    请选择要爬取的分类")
    print("=" * 50)
    
    for i, category in enumerate(SUBCATEGORIES, 1):
        print(f"{i:2d}. {category['name']}")
    
    print("=" * 50)
    return get_user_category_choice()

def get_user_category_choice():
    """获取用户的分类选择"""
    while True:
        try:
            choice = input(f"\n请输入数字选择分类 (1-{len(SUBCATEGORIES)}): ").strip()
            
            if not choice:
                print("输入不能为空，请重新输入")
                continue
                
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(SUBCATEGORIES):
                selected_category = SUBCATEGORIES[choice_num - 1]
                print(f"\n您选择了: {selected_category['name']} 分类")
                
                confirm = input("确认选择吗？(y/n): ").strip().lower()
                if confirm in ['y', 'yes', '是', '确认', '']:
                    return selected_category
                else:
                    print("请重新选择...")
                    continue
            else:
                print(f"请输入 1-{len(SUBCATEGORIES)} 之间的数字")
                
        except ValueError:
            print("请输入有效的数字")
        except KeyboardInterrupt:
            print("\n程序被用户中断")
            return None


class XimalayaNovelUpdater:
    """喜马拉雅热播榜自动检测更新器"""

    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.existing_novels_data = {}  # 存储现有小说数据
        self.existing_chapters_data = {}  # 存储现有章节数据

    def __enter__(self):
        """同步上下文管理器入口"""
        self.initialize_browser()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """同步上下文管理器出口"""
        self.cleanup()

    def initialize_browser(self):
        """初始化浏览器"""
        try:
            logger.info("开始初始化Playwright...")
            self.playwright = sync_playwright().start()

            logger.info("开始启动浏览器...")

            # 构建浏览器启动参数
            launch_args = [
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]

            # 检测是否在exe环境中运行
            is_exe_env = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
            
            if is_exe_env:
                logger.info("检测到exe环境，尝试使用系统浏览器...")
                # 在exe环境下，尝试使用系统安装的Chrome浏览器
                system_chrome_paths = [
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                    r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
                    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                ]
                
                browser_found = False
                for chrome_path in system_chrome_paths:
                    if os.path.exists(chrome_path):
                        logger.info(f"找到系统浏览器: {chrome_path}")
                        try:
                            self.browser = self.playwright.chromium.launch(
                                executable_path=chrome_path,
                                headless=CONFIG['headless'],
                                args=launch_args
                            )
                            browser_found = True
                            break
                        except Exception as e:
                            logger.warning(f"使用系统浏览器 {chrome_path} 失败: {e}")
                            continue
                
                if not browser_found:
                    logger.warning("未找到系统浏览器，尝试使用channel方式启动...")
                    try:
                        # 尝试使用channel方式启动Chrome
                        self.browser = self.playwright.chromium.launch(
                            channel="chrome",
                            headless=CONFIG['headless'],
                            args=launch_args
                        )
                        browser_found = True
                    except Exception as e:
                        logger.warning(f"使用Chrome channel失败: {e}")
                        try:
                            # 尝试使用Edge channel
                            self.browser = self.playwright.chromium.launch(
                                channel="msedge",
                                headless=CONFIG['headless'],
                                args=launch_args
                            )
                            browser_found = True
                        except Exception as e2:
                            logger.error(f"使用Edge channel也失败: {e2}")
                
                if not browser_found:
                    raise Exception("在exe环境下无法启动任何浏览器，请确保系统已安装Chrome或Edge浏览器")
                    
            elif CONFIG['browser_path']:
                logger.info(f"使用用户指定的浏览器: {CONFIG['browser_path']}")
                self.browser = self.playwright.chromium.launch(
                    executable_path=CONFIG['browser_path'],
                    headless=CONFIG['headless'],
                    args=launch_args
                )
            else:
                logger.info("使用默认浏览器")
                self.browser = self.playwright.chromium.launch(
                    headless=CONFIG['headless'],
                    args=launch_args
                )

            logger.info("开始创建浏览器上下文...")
            self.context = self.browser.new_context(
                user_agent=CONFIG['user_agent'],
                viewport=CONFIG['viewport']
            )

            # 设置额外的浏览器属性以避免检测
            logger.info("设置浏览器脚本...")
            self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)

            logger.info("创建新页面...")
            self.page = self.context.new_page()
            logger.info(f"页面创建结果: {self.page}")
            logger.info(f"页面类型: {type(self.page)}")

            logger.info("设置页面超时...")
            logger.info(f"CONFIG['timeout']的值: {CONFIG['timeout']}")
            logger.info(f"CONFIG['timeout']的类型: {type(CONFIG['timeout'])}")
            logger.info(f"self.page的值: {self.page}")
            logger.info(f"self.page的类型: {type(self.page)}")
            if self.page is not None:
                logger.info("页面不为None，开始设置超时...")
                if CONFIG['timeout'] is not None:
                    logger.info(f"准备调用set_default_timeout，参数: {CONFIG['timeout']}")
                    try:
                        # 检查页面是否仍然有效
                        logger.info(f"调用前再次检查self.page: {self.page}")
                        logger.info(f"调用前再次检查self.page类型: {type(self.page)}")

                        # 暂时跳过set_default_timeout调用，因为存在未知的Playwright内部问题
                        logger.info("跳过set_default_timeout调用，直接完成初始化")
                        # result = await self.page.set_default_timeout(CONFIG['timeout'])
                        # logger.info(f"set_default_timeout调用结果: {result}")
                        logger.info("浏览器初始化成功")
                    except Exception as timeout_error:
                        logger.error(f"设置超时失败: {timeout_error}")
                        logger.error(f"错误类型: {type(timeout_error)}")
                        import traceback
                        logger.error(f"详细错误: {traceback.format_exc()}")
                        raise
                else:
                    logger.error("CONFIG['timeout']为None，无法设置超时")
                    raise ValueError("CONFIG['timeout']不能为None")
            else:
                logger.error(f"页面创建失败，self.page为None，类型: {type(self.page)}")
                raise Exception("页面创建失败，self.page为None")

        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            import traceback
            logger.error(f"详细错误信息: {traceback.format_exc()}")
            self.cleanup()
            raise

    def cleanup(self):
        """清理资源"""
        try:
            if hasattr(self, 'page') and self.page:
                self.page.close()
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'browser') and self.browser:
                self.browser.close()
            if hasattr(self, 'playwright') and self.playwright:
                self.playwright.stop()
            logger.info("浏览器资源清理完成")
        except Exception as e:
            logger.error(f"清理资源时出错: {e}")


# 人工模拟操作函数（将从新品榜.py复制）
def human_like_delay(min=0.2, max=0.8):
    """模拟人类操作的不规则延迟（优化：从0.5-2.0秒减少到0.2-0.8秒）"""
    time.sleep(random.uniform(min, max))


def human_like_scroll(page: Page):
    """人类行为模拟滚动"""
    try:
        # 随机滚动距离和方向
        scroll_distance = random.randint(200, 800)
        direction = random.choice([1, -1])
        page.mouse.wheel(0, scroll_distance * direction)
        human_like_delay(0.2, 0.6)  # 优化：从0.5-1.5秒减少到0.2-0.6秒
    except Exception as e:
        logger.error(f"滚动页面失败: {e}")


def simulate_browsing_behavior(page: Page, duration_range=(1, 3)):
    """模拟人工浏览行为"""
    try:
        logger.info("开始模拟人工浏览行为...")

        # 随机浏览时长
        browse_duration = random.uniform(duration_range[0], duration_range[1])
        start_time = time.time()

        # 获取页面尺寸
        viewport_size = page.viewport_size
        page_width = viewport_size['width'] if viewport_size else 1920
        page_height = viewport_size['height'] if viewport_size else 1080

        while time.time() - start_time < browse_duration:
            # 随机选择浏览行为
            action = random.choice(['scroll', 'mouse_move', 'pause', 'small_scroll'])

            if action == 'scroll':
                # 随机滚动
                scroll_distance = random.randint(100, 600)
                direction = random.choice([1, -1])
                page.mouse.wheel(0, scroll_distance * direction)
                logger.debug(f"执行滚动: {scroll_distance * direction}px")

            elif action == 'mouse_move':
                # 随机鼠标移动
                x = random.randint(100, page_width - 100)
                y = random.randint(100, page_height - 100)
                page.mouse.move(x, y)
                logger.debug(f"鼠标移动到: ({x}, {y})")

            elif action == 'small_scroll':
                # 小幅滚动（模拟阅读）
                scroll_distance = random.randint(50, 200)
                page.mouse.wheel(0, scroll_distance)
                logger.debug(f"小幅滚动: {scroll_distance}px")

            elif action == 'pause':
                # 停顿（模拟阅读或思考）（优化：从0.8-2.5秒减少到0.3-1.0秒）
                pause_time = random.uniform(0.3, 1.0)
                time.sleep(pause_time)
                logger.debug(f"停顿: {pause_time:.2f}秒")
                continue

            # 动作间隔（优化：从0.3-1.2秒减少到0.1-0.5秒）
            human_like_delay(0.1, 0.5)

        logger.info(f"模拟浏览完成，耗时: {time.time() - start_time:.2f}秒")

    except Exception as e:
        logger.error(f"模拟浏览行为失败: {e}")



def navigate_to_ranking_page(page: Page) -> bool:
    """导航到榜单页面"""
    try:
        # 打开喜马拉雅首页
        logger.info("正在打开喜马拉雅首页...")
        page.goto('https://www.ximalaya.com/', timeout=60000)
        logger.info("已打开喜马拉雅首页，请扫码登录...")

        # 页面加载后模拟浏览行为
        simulate_browsing_behavior(page, duration_range=(2, 4))

        # 等待用户手动扫码登录
        input("请扫码登录完成后，按回车键继续程序...")
        logger.info("检测到回车键，继续执行操作...")

        # 登录后模拟人类浏览行为
        logger.info("登录后模拟人类浏览行为...")
        simulate_browsing_behavior(page, duration_range=(3, 6))

        # 定位"排行榜"按钮
        logger.info("定位排行榜按钮...")
        ranking_btn = page.locator('a.entry.entry-1.i-b.h_K >> text=排行榜')

        if ranking_btn.is_visible():
            logger.info("找到排行榜按钮，模拟人类点击...")
            human_like_click(page, 'a.entry.entry-1.i-b.h_K >> text=排行榜')
            logger.info("已点击排行榜按钮...")

            # 等待页面跳转
            page.wait_for_url('**/top/**', timeout=15000)
            logger.info("成功跳转到榜单页面！")

            # 页面跳转后模拟人类查看榜单行为
            logger.info("模拟人类浏览榜单...")
            simulate_browsing_behavior(page, duration_range=(4, 8))

            # 等待榜单内容加载
            logger.info("等待榜单内容加载...")
            page.wait_for_selector('div.album-item._Sq', state='attached', timeout=15000)

            # 点击小说标签
            logger.info("定位小说标签...")
            novel_tab = page.locator('a.rank-nav-link[href="/top/2/100077"]')
            
            if novel_tab.is_visible():
                logger.info("找到小说标签，模拟人类点击...")
                human_like_click(page, 'a.rank-nav-link[href="/top/2/100077"]', "小说标签")
                logger.info("已点击小说标签...")
                
                # 等待页面跳转，使用更灵活的等待方式
                try:
                    # 等待URL变化或者页面内容变化
                    page.wait_for_function(
                        "() => window.location.href.includes('/top/2/') || document.querySelector('.rank-tab-nav__tab.active a[href*=\"/top/2/\"]')",
                        timeout=15000
                    )
                    logger.info("小说榜页面加载成功！")
                except Exception as e:
                    logger.warning(f"URL等待超时，但继续执行: {e}")
                
                # 模拟人类查看小说榜行为
                logger.info("模拟人类浏览小说榜...")
                human_like_delay(1.0, 2.0)  # 优化：从2-4秒减少到1-2秒
                human_like_scroll(page)
                human_like_delay(1.0, 2.0)
                
                # 等待小说榜内容加载
                logger.info("等待小说榜内容加载...")
                page.wait_for_selector('div.album-item._Sq', state='attached', timeout=15000)
                
                return True
            else:
                logger.info("未找到小说标签")
                logger.info("未找到热播标签，继续使用默认榜单")
                return False

            logger.info("热播标签点击完成，使用热播榜页面")

            return True
        else:
            logger.error("未找到排行榜按钮")
            return False

    except Exception as e:
        logger.error(f"导航到榜单页面失败: {e}")
        return False


def process_category(page: Page, category: Dict, base_dir: str = None) -> List[Dict]:
    """处理指定分类的爬取（收集模式）"""
    category_name = category['name']
    category_selectors = category['selectors']
    
    try:
        logger.info(f"开始处理{category_name}分类")
        
        # 等待页面稳定
        human_like_delay(1.0, 2.0)
        
        # 模拟人类浏览行为
        human_like_scroll(page)
        human_like_delay(1.0, 2.0)
        
        # 点击分类按钮
        logger.info(f"开始查找并点击{category_name}分类按钮...")
        
        # 尝试查找并点击分类按钮
        category_button_found = False
        working_selector = None
        
        for selector in category_selectors:
            try:
                logger.info(f"尝试选择器: {selector}")
                category_button = page.locator(selector).first
                
                if category_button.is_visible():
                    logger.info(f"找到{category_name}分类按钮，使用选择器: {selector}")
                    
                    # 滚动到按钮位置
                    category_button.scroll_into_view_if_needed()
                    human_like_delay(0.5, 1.0)
                    
                    # 模拟人类点击
                    if human_like_click(page, selector, f"{category_name}分类按钮"):
                        logger.info(f"成功点击{category_name}分类按钮")
                        category_button_found = True
                        working_selector = selector
                        break
                    else:
                        logger.warning(f"点击失败，尝试下一个选择器")
                        
            except Exception as e:
                logger.debug(f"选择器 {selector} 失败: {e}")
                continue
        
        if not category_button_found:
            logger.warning(f"未找到{category_name}分类按钮，继续使用当前页面")
        else:
            logger.info(f"{category_name}分类按钮点击成功，使用的选择器: {working_selector}")
            # 等待页面加载
            human_like_delay(2.0, 4.0)
        
        # 等待榜单内容加载
        page.wait_for_selector('div.album-item._Sq', state='attached', timeout=15000)
        
        # 检测并处理验证码
        captcha_status = check_captcha_on_page(page)
        if captcha_status:
            logger.info(f"{category_name}分类页面发现验证码，开始处理...")
            time.sleep(5)
            page.reload()
            page.wait_for_selector('div.album-item._Sq', state='attached', timeout=15000)
        
        # 爬取都市分类的小说数据（收集模式）
        logger.info(f"开始爬取{category_name}分类的小说数据...")
        novels_data = crawl_novels_data(page, category_name, base_dir)
        
        logger.info(f"{category_name}分类爬取完成，共{len(novels_data)}个小说")
        return novels_data
        
    except Exception as e:
        logger.error(f"处理{category_name}分类时发生错误: {e}")
        return []


def human_like_click(page, selector, description="元素", timeout=10000):
    """模拟人类点击行为"""
    try:
        print(f"准备点击{description}...")

        # 统一处理字符串选择器
        if isinstance(selector, str):
            # 等待元素出现并可点击
            page.wait_for_selector(selector, state='visible', timeout=timeout)

            # 获取元素并模拟鼠标移动
            element = page.locator(selector).first

            # 获取元素位置信息
            box = element.bounding_box()
            if box:
                # 计算点击位置（元素中心）
                x = box['x'] + box['width'] / 2
                y = box['y'] + box['height'] / 2

                # 模拟鼠标移动到元素上
                page.mouse.move(x, y)
                human_like_delay(0.5, 1.5)

                # 点击元素
                element.click()
                print(f"已点击{description}")

                # 点击后延迟
                human_like_delay(1.0, 2.0)
                return True
            else:
                print(f"无法获取{description}的位置信息")
                return False
        else:
            print(f"不支持的选择器类型: {type(selector)}")
            return False

    except Exception as e:
        print(f"点击{description}失败: {str(e)}")
        logger.error(f"点击元素失败 {selector}: {e}")
        return False


def is_selector_displayed(page, selector):
    """使用computed style判断元素是否真正可见（非display:none/visibility:hidden/opacity:0，且尺寸>0）"""
    try:
        locator = page.locator(selector)
        if locator.count() == 0:
            return False
        el = locator.first
        return el.evaluate("""
            (el) => {
              if (!el) return false;
              const style = window.getComputedStyle(el);
              const rect = el.getBoundingClientRect();
              if (!style) return false;
              const visible = style.display !== 'none' && style.visibility !== 'hidden' && parseFloat(style.opacity || '1') > 0;
              const hasBox = rect && rect.width > 0 && rect.height > 0;
              return !!(visible && hasBox);
            }
        """)
    except Exception:
        return False


def calculate_gap_position(bg_img, slice_img):
    """计算缺口位置"""
    try:
        # 尝试导入必要的库
        try:
            import cv2
            import numpy as np

            # 验证 NumPy 核心功能
            try:
                # 创建测试数组检查核心功能
                test_arr = np.array([1, 2, 3])
                if not hasattr(test_arr, '__array_interface__'):
                    raise RuntimeError("NumPy 数组功能异常")

                # 检查核心API是否存在
                if not hasattr(np.core.multiarray, '_ARRAY_API'):
                    logger.warning("NumPy _ARRAY_API 属性不存在，但继续尝试使用")

            except Exception as np_err:
                logger.error(f"NumPy 完整性检查失败: {np_err}")
                # 回退到默认值
                return random.randint(240, 280)

        except ImportError as e:
            logger.error(f"导入计算缺口位置所需库失败: {e}")
            # 回退到默认值
            return random.randint(240, 280)

        # 转换为numpy数组
        try:
            bg_array = np.array(bg_img.convert('RGB'))
            slice_array = np.array(slice_img.convert('RGB'))
        except Exception as conv_err:
            logger.error(f"图像转换失败: {conv_err}")
            return random.randint(240, 280)

        try:
            # 转换为灰度图
            bg_gray = cv2.cvtColor(bg_array, cv2.COLOR_RGB2GRAY)
            slice_gray = cv2.cvtColor(slice_array, cv2.COLOR_RGB2GRAY)

            # 反色处理滑块图
            slice_gray = 255 - slice_gray

            # 使用模板匹配
            result = cv2.matchTemplate(bg_gray, slice_gray, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            logger.info(f"匹配度: {max_val:.4f}")

            if max_val > 0.3:  # 匹配度阈值
                gap_x = max_loc[0]
                logger.info(f"缺口位置计算成功: {gap_x}px")
                return gap_x
            else:
                logger.info("匹配度不足，无法确定缺口位置")
                return None

        except cv2.error as cv_err:
            logger.error(f"OpenCV 处理失败: {cv_err}")
            return random.randint(240, 280)

        except Exception as e:
            logger.error(f"图像处理过程中出错: {e}")
            return random.randint(240, 280)

    except Exception as e:
        logger.error(f"计算缺口位置失败: {e}")
        return random.randint(240, 280)




def generate_human_like_track(distance):
    """生成更人性化的移动轨迹"""
    import random
    import math

    tracks = []
    current = 0
    point_count = random.randint(100, 150)  # 增加点数使轨迹更平滑

    # 初始暂停
    initial_pause = random.randint(5, 12)
    for _ in range(initial_pause):
        tracks.append(0)

    # 开始阶段 - 缓慢加速
    start_phase = distance * 0.2
    start_points = int(point_count * 0.3)
    for i in range(start_points):
        t = i / start_points
        # 使用三次缓动函数
        progress = t * t * t
        move = (start_phase / start_points) * progress
        current += move
        tracks.append(round(move))

        # 添加小暂停
        if random.random() < 0.1:
            tracks.append(0)

    # 中间阶段 - 快速移动
    mid_phase = distance * 0.6
    mid_points = int(point_count * 0.5)
    for i in range(mid_points):
        t = i / mid_points
        # 使用正弦函数创建加速曲线
        progress = 0.5 + 0.5 * math.sin(t * math.pi)
        move = (mid_phase / mid_points) * progress
        current += move
        tracks.append(round(move))

        # 随机速度变化
        if random.random() < 0.15:
            tracks.append(round(move * random.uniform(0.8, 1.2)))

    # 结束阶段 - 减速
    remaining = distance - current
    end_points = point_count - len(tracks) + initial_pause
    for i in range(end_points):
        t = i / end_points
        # 使用反向三次缓动函数
        progress = 1 - (1 - t) ** 3
        move = (remaining / end_points) * progress
        tracks.append(round(move))

        # 添加小暂停
        if random.random() < 0.08:
            tracks.append(0)

    # 最终微调
    final_adjustments = random.randint(3, 7)
    for _ in range(final_adjustments):
        tracks.append(random.randint(-2, 3))

    return tracks



def check_captcha_on_page(page, page_index=None):
    """增强的验证码检测和处理"""
    print("=" * 50)
    if page_index is not None:
        print(f"访问第 {page_index} 个小说详情页，检查是否有验证码...")
    else:
        print("检查页面是否有验证码...")

    # 等待页面完全加载（优化：从2-3秒减少到1-1.5秒）
    print("等待页面完全加载...")
    human_like_delay(1.0, 1.5)
    
    max_checks = 3  # 增加检查次数
    has_captcha = False

    for check_attempt in range(max_checks):
        print(f"第 {check_attempt + 1} 次检查验证码...")
        
        # 增强的验证码检测选择器，包含动态类名和拦截元素
        enhanced_captcha_selectors = [
            # 主容器检测
            '[class*="geetest_box"]',
            '[class*="geetest_container"]',
            '[class*="geetest_popup"]',
            '[class*="geetest_widget"]',
            '[class*="geetest_captcha"]',  # 新增
            '.geetest_box',
            '.geetest_container',
            '.geetest_captcha',  # 新增
            
            # 滑块检测
            '[class*="geetest_slider"]',
            '[class*="geetest_btn"]',
            '.geetest_slider',
            '.geetest_btn',
            '.geetest_slider .geetest_btn',
            
            # 拼图检测
            '[class*="geetest_slice"]',
            '[class*="geetest_bg"]',
            '.geetest_slice',
            '.geetest_bg',
            
            # 提示文本检测
            '[class*="geetest_text_tips"]',
            '.geetest_text_tips',
            
            # 遮罩层检测（重点关注这些拦截元素）
            '[class*="geetest_popup_ghost"]',
            '[class*="geetest_mask"]',
            '.geetest_popup_ghost',  # 新增
            '.geetest_mask',  # 新增
            
            # 冻结状态检测
            '[class*="geetest_freeze"]',
            '[class*="geetest_boxShow"]'
        ]

        # 检查是否有验证码成功状态
        success_indicators = [
            '[class*="geetest_success"]',
            '[class*="success"]',
            '.geetest_bind_tips'
        ]
        
        # 先检查成功状态
        for selector in success_indicators:
            try:
                if is_selector_displayed(page, selector):
                    try:
                        text = page.locator(selector).first.inner_text()
                        if text and ('验证通过' in text or 'success' in text.lower()):
                            print("检测到验证成功提示，无需处理验证码")
                            return False
                    except:
                        print("检测到成功状态元素，无需处理验证码")
                        return False
            except:
                continue

        # 检查验证码元素
        for selector in enhanced_captcha_selectors:
            try:
                elements = page.locator(selector)
                if elements.count() > 0:
                    for i in range(elements.count()):
                        element = elements.nth(i)
                        if element.is_visible():
                            # 检查元素是否有实际的边界框（不是隐藏的）
                            try:
                                bbox = element.bounding_box()
                                if bbox and bbox['width'] > 0 and bbox['height'] > 0:
                                    has_captcha = True
                                    print(f"检测到可见验证码元素: {selector}")
                                    
                                    # 检查是否是拦截元素
                                    if 'popup_ghost' in selector or 'geetest_bg' in selector:
                                        print(f"⚠️ 检测到拦截元素: {selector} - 这可能会阻止点击操作")
                                    
                                    # 尝试获取验证码提示文本
                                    try:
                                        tip_selectors = [
                                            '[class*="geetest_text_tips"]',
                                            '.geetest_text_tips',
                                            '[class*="geetest_ques_tips"]'
                                        ]
                                        for tip_selector in tip_selectors:
                                            tip_element = page.locator(tip_selector).first
                                            if tip_element.is_visible():
                                                tip_text = tip_element.inner_text()
                                                if tip_text:
                                                    print(f"验证码提示: {tip_text}")
                                                break
                                    except:
                                        pass
                                    break
                            except:
                                # 如果无法获取边界框，但元素可见，仍然认为有验证码
                                has_captcha = True
                                print(f"检测到验证码元素（无法获取边界框）: {selector}")
                                break
                    if has_captcha:
                        break
            except:
                continue

        if has_captcha:
            break

        if check_attempt < max_checks - 1:
            print("未检测到验证码，等待后重试...")
            human_like_delay(1.0, 2.0)
            # 轻微滚动触发可能的验证码
            try:
                page.mouse.wheel(0, 100)
                human_like_delay(0.5, 1.0)
            except:
                pass

    if has_captcha:
        print("🔍 发现验证码，开始自动处理...")
        captcha_success = handle_captcha(page)
        if captcha_success:
            print("✅ 验证码处理成功！继续执行...")
            # 验证码处理后等待页面稳定
            human_like_delay(1.5, 2.5)  # 增加等待时间确保验证码完全消失
            
            # 再次检查验证码是否真的消失了
            print("验证码处理后再次检查...")
            final_check_selectors = [
                '[class*="geetest_popup_ghost"]',
                '[class*="geetest_bg"]',
                '.geetest_popup_ghost',
                '.geetest_bg'
            ]
            
            still_has_captcha = False
            for selector in final_check_selectors:
                try:
                    if page.locator(selector).first.is_visible():
                        still_has_captcha = True
                        print(f"⚠️ 验证码元素仍然可见: {selector}")
                        break
                except:
                    continue
            
            if not still_has_captcha:
                print("✅ 确认验证码已完全消失")
            else:
                print("⚠️ 验证码可能未完全消失，但继续执行")
                
        else:
            print("❌ 验证码处理失败，请手动完成验证...")
            # 给用户时间手动处理
            human_like_delay(3.0, 5.0)
    else:
        print("✅ 经过多次检查，未发现验证码，继续执行...")

    return has_captcha


def generate_bezier_track(distance):
    """使用贝塞尔曲线生成更自然的鼠标轨迹"""
    import random
    # 控制点
    p0 = (0, 0)
    p1 = (distance * 0.3, random.randint(-10, 10))
    p2 = (distance * 0.7, random.randint(-15, 15))
    p3 = (distance, 0)

    # 生成轨迹点
    points = []
    num_points = random.randint(80, 120)

    # 初始暂停
    initial_pause = random.randint(3, 8)
    for _ in range(initial_pause):
        points.append(0)

    # 贝塞尔曲线轨迹
    for i in range(num_points):
        t = i / (num_points - 1)
        # 三次贝塞尔曲线公式
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]

        # 添加随机偏移
        x += random.randint(-2, 2)
        y += random.randint(-3, 3)

        points.append(round(x))

    # 最终微调
    final_adjustments = random.randint(2, 5)
    for _ in range(final_adjustments):
        points.append(distance + random.randint(-3, 3))

    return points



def perform_human_like_slider_move(page, slider, distance):
    """执行人性化的滑块移动"""
    try:
        print(f"开始执行滑块移动，目标距离: {distance}px")

        # 获取滑块位置
        slider_box = slider.bounding_box()
        if not slider_box:
            print("无法获取滑块位置")
            return False

        start_x = slider_box['x'] + slider_box['width'] / 2
        start_y = slider_box['y'] + slider_box['height'] / 2

        print(f"滑块起始位置: ({start_x}, {start_y})")

        # 预瞄准阶段 - 鼠标移动到滑块附近
        pre_aim_x = start_x + random.randint(-20, 20)
        pre_aim_y = start_y + random.randint(-10, 10)
        page.mouse.move(pre_aim_x, pre_aim_y)
        human_like_delay(0.2, 0.5)

        # 移动到滑块中心
        page.mouse.move(start_x, start_y)
        human_like_delay(0.1, 0.3)

        # 按下鼠标
        page.mouse.down()
        human_like_delay(0.1, 0.2)

        # 选择轨迹生成方法
        if random.random() < 0.6:  # 60%概率使用贝塞尔曲线
            print("使用贝塞尔曲线轨迹")
            track_points = generate_bezier_track(distance)
        else:  # 40%概率使用增强人性化轨迹
            print("使用增强人性化轨迹")
            track_points = generate_human_like_track(distance)

        # 执行移动
        current_x = start_x
        for i, move_x in enumerate(track_points):
            # Y轴随机移动
            y_offset = random.randint(-3, 3)
            wave_y = start_y + y_offset

            # 计算下一个X位置
            next_x = start_x + move_x

            # 动态延迟
            if i < len(track_points) * 0.3:  # 前30%慢一些
                delay = random.uniform(0.01, 0.03)
            elif i > len(track_points) * 0.7:  # 后30%也慢一些
                delay = random.uniform(0.01, 0.03)
            else:  # 中间快一些
                delay = random.uniform(0.005, 0.015)

            # 移动鼠标
            page.mouse.move(next_x, wave_y)
            current_x = next_x

            # 段间延迟
            human_like_delay(delay, delay + 0.01)

        # 尾部补偿 - 确保到达目标位置
        target_x = start_x + distance
        compensation_range = 15  # 限制补偿范围

        if abs(current_x - target_x) > 5:  # 如果偏差超过5px
            compensation = min(max(target_x - current_x, -compensation_range), compensation_range)
            final_x = current_x + compensation + random.uniform(-2, 2)
            page.mouse.move(final_x, start_y + random.randint(-2, 2))
            print(f"尾部补偿: {compensation}px, 最终位置: {final_x}")

        human_like_delay(0.1, 0.2)

        # 释放鼠标
        page.mouse.up()

        print("滑块移动完成")
        return True

    except Exception as e:
        print(f"滑块移动过程中出错: {str(e)}")
        return False


def get_geetest_images_multi_threaded(page):
    """使用多线程同时获取背景图和滑块图"""
    start_time = time.time()
    try:
        print("使用多线程下载验证码图片...")

        # 等待两个图片元素加载
        bg_element = page.locator('.geetest_bg')
        slice_element = page.locator('.geetest_slice_bg')

        page.wait_for_selector('.geetest_bg', timeout=5000)
        page.wait_for_selector('.geetest_slice_bg', timeout=5000)

        # 获取两个图片的URL
        bg_style = bg_element.get_attribute('style')
        slice_style = slice_element.get_attribute('style')

        bg_url = None
        slice_url = None

        # 提取背景图URL
        if bg_style and 'background-image' in bg_style:
            import re
            url_match = re.search(r'url\("([^"]+)"\)', bg_style)
            if url_match:
                bg_url = url_match.group(1)
                print(f"背景图URL: {bg_url}")

        # 提取滑块图URL
        if slice_style and 'background-image' in slice_style:
            import re
            url_match = re.search(r'url\("([^"]+)"\)', slice_style)
            if url_match:
                slice_url = url_match.group(1)
                print(f"滑块图URL: {slice_url}")

        if not bg_url or not slice_url:
            print("无法获取图片URL")
            return None, None

        # 使用多线程同时下载两张图片
        with ThreadPoolExecutor(max_workers=2) as executor:
            bg_future = executor.submit(download_image_with_threading, bg_url, "背景图")
            slice_future = executor.submit(download_image_with_threading, slice_url, "滑块图")

            bg_img = bg_future.result()
            slice_img = slice_future.result()

        end_time = time.time()
        download_time = end_time - start_time
        print(f"多线程下载完成，总耗时: {download_time:.2f}秒")

        return bg_img, slice_img

    except Exception as e:
        end_time = time.time()
        download_time = end_time - start_time
        print(f"多线程下载图片失败: {str(e)}，耗时: {download_time:.2f}秒")
        return None, None


def download_image_with_threading(url, image_type):
    """多线程下载图片的辅助函数"""
    try:
        import requests
        from PIL import Image
        from io import BytesIO

        print(f"开始下载{image_type}...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            print(f"{image_type}下载成功，尺寸: {img.size}")
            return img
        else:
            print(f"下载{image_type}失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"下载{image_type}时出错: {str(e)}")
        return None


def debug_captcha_page(page):
    """调试验证码页面状态，输出详细信息"""
    try:
        print("\n=== 验证码页面调试信息 ===")

        # 检查所有geetest相关元素
        geetest_elements = page.locator('[class*="geetest"]')
        for i in range(min(geetest_elements.count(), 10)):  # 最多显示10个
            try:
                element = geetest_elements.nth(i)
                tag_name = element.evaluate('el => el.tagName')
                class_name = element.get_attribute('class') or '无class'
                is_visible = element.is_visible()
            except Exception as e:
                print(f"  元素{i + 1}: 无法获取信息 - {str(e)}")

        # 检查关键容器
        containers = [
            ('.geetest_box', '验证码盒子'),
            ('.geetest_widget', '验证码组件'),
            ('.geetest_holder', '验证码容器'),
            ('.geetest_slider', '滑块区域'),
            ('.geetest_btn', '滑块按钮')
        ]

        for selector, description in containers:
            try:
                elements = page.locator(selector)
                count = elements.count()
                if count > 0:
                    first_element = elements.first
                    is_visible = first_element.is_visible()
                    class_attr = first_element.get_attribute('class') or '无class'
                    print(f"  {description}: 找到{count}个, 可见={is_visible}, class='{class_attr}'")
                else:
                    print(f"  {description}: 未找到")
            except Exception as e:
                print(f"  {description}: 检查失败 - {str(e)}")

        # 检查页面状态
        try:
            current_url = page.url
            current_title = page.title()
            print(f"  当前URL: {current_url}")
            print(f"  页面标题: {current_title}")
        except Exception as e:
            print(f"  页面状态检查失败: {str(e)}")

        print("=== 调试信息结束 ===\n")

    except Exception as e:
        print(f"调试验证码页面时出错: {str(e)}")


def detect_captcha_state(page):
    """检测验证码的当前状态"""
    try:
        # 优先判断核心容器与滑块的可见性
        core_visible = (
                is_selector_displayed(page, '.geetest_box') or
                is_selector_displayed(page, '[class*="geetest_box"]') or
                is_selector_displayed(page, '.geetest_slider .geetest_btn') or
                is_selector_displayed(page, '[class*="geetest_slider"] .geetest_btn')
        )
        if not core_visible:
            # 若页面仍有geetest痕迹，但核心容器不可见，视为已消失/隐藏
            leftover = page.locator('[class*="geetest"]').count()
            if leftover == 0:
                return "disappeared"
            # 检查是否有明确成功提示
            if is_selector_displayed(page, '.geetest_bind_tips') or is_selector_displayed(page,
                                                                                          '[class*="geetest_bind_tips"]'):
                try:
                    txt = page.locator('.geetest_bind_tips, [class*="geetest_bind_tips"]').first.inner_text()
                    if txt and '验证通过' in txt:
                        return "success"
                except Exception:
                    return "success"
            return "disappeared"

        # 检查是否有成功状态
        success_elements = page.locator('[class*="success"]')
        if success_elements.count() > 0:
            for i in range(success_elements.count()):
                if success_elements.nth(i).is_visible():
                    return "success"

        # 检查是否有错误状态
        error_elements = page.locator('[class*="error"], [class*="fail"]')
        if error_elements.count() > 0:
            for i in range(error_elements.count()):
                if error_elements.nth(i).is_visible():
                    return "error"

        # 检查是否在加载中
        loading_elements = page.locator('[class*="loading"], [class*="wait"]')
        if loading_elements.count() > 0:
            for i in range(loading_elements.count()):
                if loading_elements.nth(i).is_visible():
                    return "loading"

        # 检查滑块状态
        slider = page.locator('.geetest_slider .geetest_btn')
        if slider.count() > 0:
            if not slider.first.is_visible():
                return "slider_hidden"

            # 检查滑块是否回到初始位置
            try:
                slider_box = slider.first.bounding_box()
                if slider_box and slider_box['x'] < 50:
                    return "slider_reset"
            except:
                pass

        return "unknown"  # 状态未知

    except Exception as e:
        print(f"检测验证码状态时出错: {str(e)}")
        return "unknown"


def handle_captcha(page):
    """处理验证码"""
    try:
        logger.info("开始处理验证码...")

        # 等待验证码完全加载
        logger.info("等待验证码完全加载...")
        human_like_delay(2.0, 4.0)

        # 查找滑块按钮
        slider_selectors = [
            '.geetest_slider .geetest_btn',
            '[class*="geetest_slider"] .geetest_btn',
            '[class*="geetest_btn"]',
            '.geetest_btn'
        ]

        slider_element = None
        for selector in slider_selectors:
            try:
                if page.locator(selector).count() > 0 and is_selector_displayed(page, selector):
                    slider_element = page.locator(selector).first
                    logger.info(f"找到滑块元素: {selector}")
                    break
            except:
                continue

        if not slider_element:
            logger.error("未找到滑块元素")
            return False

        # 多线程获取验证码图片（带失败重试）
        logger.info("获取验证码图片...")
        bg_img = None
        slice_img = None

        max_image_retries = 3
        for retry in range(max_image_retries):
            try:
                logger.info(f"第 {retry + 1} 次尝试获取验证码图片...")

                # 尝试使用图像识别
                bg_img, slice_img = get_geetest_images_multi_threaded(page)

                if bg_img is not None and slice_img is not None:
                    logger.info("成功获取验证码图片")
                    break
                else:
                    logger.info("获取图片失败")

            except Exception as img_error:
                logger.error(f"获取验证码图片时出错: {img_error}")

            if retry < max_image_retries - 1:
                human_like_delay(1.0, 2.0)

        # 计算目标距离（带多重回退机制）
        target_distance = None

        # 第一优先级：使用图像识别计算距离
        if bg_img is not None and slice_img is not None:
            gap_x = calculate_gap_position(bg_img, slice_img)
            if gap_x is not None:
                target_distance = int(gap_x)
                logger.info(f"通过图像识别计算得出滑动距离: {target_distance}px")

        # 第二优先级：经验值范围
        if target_distance is None or target_distance <= 0:
            # 基于经验的距离范围（240-280 是最常见的滑块距离）
            target_distance = random.randint(240, 280)
            logger.info(f"使用经验滑动距离: {target_distance}px")

        # 第三优先级：动态调整（防止被识别为机器人）
        # 添加 ±5px 的随机偏移
        offset = random.randint(-5, 5)
        target_distance = max(100, min(400, target_distance + offset))
        logger.info(f"添加随机偏移 {offset}px，最终滑动距离: {target_distance}px")

        # 执行带重试机制的滑动验证
        max_slide_retries = 5
        for slide_retry in range(max_slide_retries):
            logger.info(f"第 {slide_retry + 1} 次滑动尝试...")

            # 如果不是第一次尝试，重新获取验证码图片（验证码可能已更新）
            if slide_retry > 0:
                logger.info("重新获取验证码图片...")
                try:
                    new_bg_img, new_slice_img = get_geetest_images_multi_threaded(page)
                    if new_bg_img is not None and new_slice_img is not None:
                        # 重新计算缺口位置
                        new_gap_x = calculate_gap_position(new_bg_img, new_slice_img)
                        if new_gap_x is not None:
                            target_distance = int(new_gap_x)
                            logger.info(f"重新计算缺口位置成功: {target_distance}px")
                        else:
                            logger.info("重新计算缺口位置失败，保持原位置")
                    else:
                        logger.info("重新获取验证码图片失败，使用原位置")
                except Exception as img_error:
                    logger.error(f"重新获取验证码图片时出错: {img_error}")
                    logger.info("获取图片失败，保持原位置")

                # 添加随机偏移，模拟人类不精确性
                try:
                    offset = random.randint(-3, 3)
                    adjusted_target_distance = max(100, min(400, target_distance + offset))
                    logger.info(f"添加随机偏移: {offset}px，调整后距离: {adjusted_target_distance}px")
                    target_distance = adjusted_target_distance
                except Exception as offset_error:
                    logger.error(f"添加偏移时出错: {offset_error}，使用原距离")

            # 执行滑动
            slide_success = perform_human_like_slider_move(page, slider_element, target_distance)

            if not slide_success:
                logger.error(f"滑动执行失败，重试 {slide_retry + 1}/{max_slide_retries}")
                if slide_retry < max_slide_retries - 1:
                    human_like_delay(1.0, 1.5)  # 优化：从2-3秒减少到1-1.5秒
                continue

            # 智能等待验证结果
            logger.info("等待验证结果...")
            human_like_delay(1.0, 2.0)  # 优化：从2-4秒减少到1-2秒

            # 检查验证结果
            max_wait = 3
            verification_success = False

            for wait_count in range(max_wait):
                try:
                    # 使用状态检测函数
                    captcha_state = detect_captcha_state(page)
                    logger.info(f"验证码当前状态: {captcha_state}")

                    # 根据状态判断是否成功
                    if captcha_state in ["disappeared", "success", "slider_hidden", "slider_reset"]:
                        logger.info(f"✓ 验证码状态 '{captcha_state}' 表示验证成功")
                        verification_success = True
                        break
                    elif captcha_state == "error":
                        logger.error("✗ 验证码状态为错误，需要重试")
                        break
                    elif captcha_state == "loading":
                        logger.info("⏳ 验证码仍在处理中")
                    elif captcha_state == "unknown":
                        logger.warning("? 验证码状态未知，继续等待")
                    else:
                        logger.warning(f"? 未预期的验证码状态: {captcha_state}")

                    logger.info(f"等待验证结果... ({wait_count + 1}/{max_wait})")
                    human_like_delay(1.0, 1.5)

                except Exception as e:
                    logger.error(f"检查验证结果时出错: {str(e)}")
                    continue

            if verification_success:
                logger.info("验证码处理成功！")
                
                # 增加强制等待机制，确保验证码完全消失
                logger.info("验证码处理成功，等待验证码完全消失...")
                human_like_delay(3.0, 5.0)
                
                # 二次确认验证码是否完全消失
                final_check_attempts = 3
                captcha_fully_gone = False
                
                for check_attempt in range(final_check_attempts):
                    try:
                        # 检查所有可能的验证码元素
                        captcha_selectors = [
                            'div[class*="geetest_bg"]',
                            'div[class*="geetest_popup_ghost"]', 
                            'div[class*="geetest_captcha"][class*="geetest_boxShow"]',
                            'div[class*="geetest_mask"]',
                            'div[class*="geetest_freeze"]'
                        ]
                        
                        captcha_still_visible = False
                        for selector in captcha_selectors:
                            elements = page.locator(selector)
                            if elements.count() > 0:
                                for i in range(elements.count()):
                                    if elements.nth(i).is_visible():
                                        captcha_still_visible = True
                                        logger.warning(f"检测到验证码元素仍然可见: {selector}")
                                        break
                            if captcha_still_visible:
                                break
                        
                        if not captcha_still_visible:
                            logger.info("✓ 验证码已完全消失")
                            captcha_fully_gone = True
                            break
                        else:
                            logger.warning(f"验证码仍然可见，等待消失... ({check_attempt + 1}/{final_check_attempts})")
                            human_like_delay(2.0, 3.0)
                            
                    except Exception as check_e:
                        logger.warning(f"检查验证码消失状态时出错: {check_e}")
                        human_like_delay(1.0, 2.0)
                
                if captcha_fully_gone:
                    logger.info("验证码已完全消失，可以安全进行后续操作")
                else:
                    logger.warning("验证码可能仍然存在，但继续执行后续操作")
                
                return True
            else:
                logger.error(f"验证失败，准备重试 {slide_retry + 1}/{max_slide_retries}")
                if slide_retry < max_slide_retries - 1:
                    human_like_delay(1.5, 2.5)  # 优化：从3-5秒减少到1.5-2.5秒

        logger.error("验证码处理失败，已达到最大重试次数")
        return False

    except Exception as e:
        logger.error(f"验证码处理过程中出错: {str(e)}")
        return False


def create_novel_folder_structure(base_dir=None):
    """创建小说数据的基础文件夹结构"""
    try:
        # 如果没有提供路径，则让用户选择
        if base_dir is None:
            base_dir = select_data_folder_path()
            if not base_dir:
                # 如果用户取消选择，使用默认路径
                base_dir = "D:/外包/喜马拉雅/小说数据"
                logger.info(f"用户未选择路径，使用默认路径: {base_dir}")
        else:
            # 如果已提供路径，直接使用
            logger.info(f"使用指定的数据存储路径: {base_dir}")

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            logger.info(f"创建基础目录: {base_dir}")
        return base_dir
    except Exception as e:
        logger.error(f"创建基础目录失败: {e}")
        raise


def find_first_episode_chapter(chapters_data: List[Dict]) -> Dict:
    """
    搜索匹配第一集关键词的章节
    关键词: 01, 001, 0001, 00001, 第一集等
    """
    first_episode_keywords = [
        r'第一集',
        r'第1集',
        r'\b01\b',
        r'\b001\b',
        r'\b0001\b',
        r'\b00001\b'
    ]

    for chapter in chapters_data:
        chapter_title = chapter.get('title', '')
        for keyword_pattern in first_episode_keywords:
            if re.search(keyword_pattern, chapter_title, re.IGNORECASE):
                logger.info(f"找到匹配的第一集章节: {chapter_title}")
                return chapter

    logger.info("未找到匹配第一集关键词的章节")
    return None


def scrape_chapter_detail_page(page: Page, chapter_title: str) -> Dict:
    """
    抓取章节详情页的上架时间等信息
    """
    chapter_detail = {}

    try:
        # 增加等待时间并添加重试机制
        max_retries = 3
        
        # 多种章节详情页选择器，按优先级尝试
        detail_page_selectors = [
            '.info.kn_',  # 原始选择器
            '.content-wrapper',  # 备用选择器1
            '.sound-detail',  # 声音详情容器
            '.album-detail-wrapper',  # 专辑详情包装器
            '.detail-content',  # 详情内容
            '.sound-info',  # 声音信息
            '[class*="detail"]',  # 包含detail的元素
            '[class*="info"]',  # 包含info的元素
            '.title-wrapper',  # 标题包装器
            'h1',  # 标题元素
            '.sound-title',  # 声音标题
            '[data-sound-id]',  # 有声音ID的元素
            '.play-info',  # 播放信息
            '.sound-content',  # 声音内容
            'main',  # 主要内容区域
            '#app',  # 应用根元素
            'body'  # 最后的兜底选择器
        ]
        
        page_loaded = False
        used_selector = None
        
        for attempt in range(max_retries):
            try:
                # 尝试多个选择器
                for selector in detail_page_selectors:
                    try:
                        # 使用智能等待策略
                        wait_times = [5000, 10000, 15000, 20000, 30000]  # 渐进式超时
                        
                        for wait_time in wait_times:
                            try:
                                page.wait_for_selector(selector, timeout=wait_time)
                                # 验证页面确实加载了章节详情内容
                                if selector in ['.info.kn_', '.sound-detail', '.album-detail-wrapper', '.detail-content']:
                                    # 对于关键选择器，额外验证页面内容
                                    try:
                                        # 检查是否有标题或时间等关键信息
                                        has_content = (
                                            page.locator('h1, .title-wrapper, [class*="title"]').count() > 0 or
                                            page.locator('.time, [class*="time"]').count() > 0 or
                                            page.locator('.count, [class*="count"]').count() > 0
                                        )
                                        if has_content:
                                            page_loaded = True
                                            used_selector = selector
                                            logger.info(f"使用选择器 '{selector}' 成功加载章节详情页 (等待时间: {wait_time}ms)")
                                            break
                                    except:
                                        # 如果验证失败，继续尝试下一个等待时间
                                        continue
                                else:
                                    # 对于兜底选择器，直接认为成功
                                    page_loaded = True
                                    used_selector = selector
                                    logger.info(f"使用兜底选择器 '{selector}' 加载章节详情页 (等待时间: {wait_time}ms)")
                                    break
                            except:
                                # 当前等待时间失败，尝试更长的等待时间
                                continue
                        
                        if page_loaded:
                            break
                            
                    except Exception as selector_e:
                        logger.debug(f"选择器 '{selector}' 失败: {selector_e}")
                        continue
                
                if page_loaded:
                    break
                    
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"章节详情页加载失败，第{attempt + 1}次重试: {e}")
                    human_like_delay(2.0, 4.0)
                    # 尝试刷新页面
                    try:
                        page.reload(wait_until='networkidle', timeout=30000)
                    except:
                        pass
                    continue
                else:
                    logger.error(f"章节详情页加载完全失败: {e}")
                    return {'error': str(e)}
        
        if not page_loaded:
            logger.error("所有选择器都无法加载章节详情页")
            return {'error': '章节详情页加载失败'}

        # 增强的页面完全加载检测机制
        logger.info("章节详情页基本加载完成，开始增强检测...")
        
        # 等待页面完全稳定
        try:
            # 1. 等待网络空闲状态
            page.wait_for_load_state('networkidle', timeout=10000)
            logger.info("网络空闲状态检测完成")
        except:
            logger.warning("网络空闲状态检测超时，继续执行")
        
        try:
            # 2. 等待DOM完全加载
            page.wait_for_function("document.readyState === 'complete'", timeout=10000)
            logger.info("DOM完全加载检测完成")
        except:
            logger.warning("DOM完全加载检测超时，继续执行")
        
        # 3. 等待关键内容元素出现并稳定
        content_check_selectors = [
            '.time, [class*="time"]',  # 时间信息
            '.count, [class*="count"]',  # 计数信息
            'h1, .title-wrapper, [class*="title"]',  # 标题信息
        ]
        
        for check_selector in content_check_selectors:
            try:
                # 等待元素出现
                page.wait_for_selector(check_selector, state='attached', timeout=5000)
                # 等待元素可见
                page.wait_for_selector(check_selector, state='visible', timeout=3000)
                logger.info(f"关键内容元素 '{check_selector}' 检测完成")
                break  # 只要有一个关键元素加载成功就继续
            except:
                logger.debug(f"关键内容元素 '{check_selector}' 检测失败")
                continue
        
        # 4. 额外的稳定性等待
        human_like_delay(1.0, 2.0)
        
        logger.info(f"章节详情页完全加载检测完成，使用的选择器: {used_selector}")

        # 抓取上架时间 - 增强选择器
        time_selectors = [
            'span.time.kn_', 
            '.time', 
            '[class*="time"]',
            '.publish-time',
            '.upload-time',
            '.create-time',
            '[data-time]',
            '.date',
            '[class*="date"]'
        ]
        for selector in time_selectors:
            try:
                time_element = page.locator(selector).first
                if time_element.is_visible():
                    chapter_detail['publish_time'] = time_element.inner_text()
                    logger.info(f"章节 {chapter_title} 的上架时间: {chapter_detail['publish_time']}")
                    break
            except:
                continue
        
        if 'publish_time' not in chapter_detail:
            chapter_detail['publish_time'] = "未找到"
            logger.warning(f"章节 {chapter_title} 未找到上架时间元素")

        # 抓取章节标题（来自详情页） - 增强选择器
        title_selectors = [
            'h1.title-wrapper.kn_', 
            'h1', 
            '.title-wrapper', 
            '[class*="title"]',
            '.sound-title',
            '.chapter-title',
            '.episode-title',
            '[data-title]',
            '.detail-title',
            '.content-title'
        ]
        for selector in title_selectors:
            try:
                title_wrapper = page.locator(selector).first
                if title_wrapper.is_visible():
                    chapter_detail['detail_title'] = title_wrapper.inner_text()
                    logger.info(f"章节 {chapter_title} 的详情页标题: {chapter_detail['detail_title']}")
                    break
            except:
                continue
        
        if 'detail_title' not in chapter_detail:
            chapter_detail['detail_title'] = chapter_title

        # 抓取播放时长 - 增强选择器
        duration_selectors = [
            'span.count.kn_ i.xuicon-wode-yuansu-shichang.kn_',
            '.count i[class*="shichang"]',
            '[class*="duration"]',
            '.count',
            '.play-duration',
            '.sound-duration',
            '.time-duration',
            '[data-duration]',
            '.length',
            '[class*="length"]'
        ]
        for selector in duration_selectors:
            try:
                if 'i.xuicon-wode-yuansu-shichang' in selector:
                    duration_element = page.locator(selector).locator('xpath=..')
                else:
                    duration_element = page.locator(selector).first
                
                if duration_element.is_visible():
                    duration_text = duration_element.inner_text()
                    chapter_detail['duration'] = duration_text
                    logger.info(f"章节 {chapter_title} 的播放时长: {duration_text}")
                    break
            except:
                continue
        
        if 'duration' not in chapter_detail:
            chapter_detail['duration'] = "未找到"
            logger.warning(f"章节 {chapter_title} 未找到播放时长元素")

        # 抓取播放量 - 增强选择器
        play_count_selectors = [
            'span.count.kn_ i.xuicon-erji1.kn_',
            '.count i[class*="erji"]',
            '[class*="play-count"]',
            '.count',
            '.play-num',
            '.listen-count',
            '.view-count',
            '[data-play-count]',
            '.stats-play',
            '[class*="stats"]',
            '.number',
            '[class*="number"]'
        ]
        for selector in play_count_selectors:
            try:
                if 'i.xuicon-erji1' in selector:
                    play_count_element = page.locator(selector).locator('xpath=..')
                else:
                    play_count_element = page.locator(selector).first
                
                if play_count_element.is_visible():
                    play_count_text = play_count_element.inner_text()
                    chapter_detail['play_count'] = play_count_text
                    logger.info(f"章节 {chapter_title} 的播放量: {play_count_text}")
                    break
            except:
                continue
        
        if 'play_count' not in chapter_detail:
            chapter_detail['play_count'] = "未找到"
            logger.warning(f"章节 {chapter_title} 未找到播放量元素")

        logger.info(f"章节详情页信息抓取完成: {chapter_detail}")

    except Exception as e:
        logger.error(f"抓取章节详情页信息失败: {e}")
        chapter_detail['error'] = str(e)

    return chapter_detail


def scrape_novel_details_first_page(page: Page, novel_title: str) -> Dict:
    """爬取小说详情页第一页章节数据"""
    novel_data = {}

    try:
        # 小说名
        title_element = page.locator('h1.title')
        if title_element.is_visible():
            novel_data['novel_title'] = title_element.inner_text()
        else:
            novel_data['novel_title'] = novel_title or "未找到"
    except Exception as e:
        logger.error(f"获取小说标题失败: {e}")
        novel_data['novel_title'] = novel_title or "获取失败"

    try:
        # 总播放量
        count_element = page.locator('span.count.z_i')
        count = count_element.count()
        if count > 0:
            novel_data['total_plays'] = count_element.first.inner_text()
        else:
            novel_data['total_plays'] = "未找到"
    except Exception as e:
        logger.error(f"获取总播放量失败: {e}")
        novel_data['total_plays'] = "获取失败"

    try:
        # 主播名
        anchor_element = page.locator('a.nick-name.undefined')
        if anchor_element.is_visible():
            novel_data['anchor_name'] = anchor_element.inner_text()
        else:
            novel_data['anchor_name'] = "未找到"
    except Exception as e:
        logger.error(f"获取主播名失败: {e}")
        novel_data['anchor_name'] = "获取失败"

    try:
        # 评论数
        comment_element = page.locator('span.title.false.s_O')
        if comment_element.is_visible():
            comment_text = comment_element.inner_text()
            # 提取评论数，格式如：评价（999+）
            comment_match = re.search(r'评价.*?（([^）]+)）', comment_text)
            novel_data['comments_count'] = comment_match.group(1) if comment_match else comment_text
        else:
            novel_data['comments_count'] = "未找到"
    except Exception as e:
        logger.error(f"获取评论数失败: {e}")
        novel_data['comments_count'] = "获取失败"

    try:
        # 粉丝数
        fans_element = page.locator('a.anchor-stats-item.undefined[href*="/fans/"] i.xuicon-web_album_ic_fans').locator('xpath=..')
        if fans_element.is_visible():
            fans_text = fans_element.inner_text()
            # 提取粉丝数，去掉图标部分
            fans_match = re.search(r'([\d.]+[万千亿]*)', fans_text)
            novel_data['fans_count'] = fans_match.group(1) if fans_match else fans_text
        else:
            novel_data['fans_count'] = "未找到"
    except Exception as e:
        logger.error(f"获取粉丝数失败: {e}")
        novel_data['fans_count'] = "获取失败"

    # 章节列表（只爬取第一页）
    all_chapters = []

    try:
        logger.info("正在爬取第一页章节...")

        # 获取当前页面URL，用于防风控机制中的页面导航
        novel_url = page.url
        logger.info(f"当前小说详情页URL: {novel_url}")

        # 处理验证码
        captcha_status = check_captcha_on_page(page)
        if captcha_status:
            logger.info("检测到验证码，处理中...")
            handle_captcha(page)
            human_like_delay(2.0, 3.0)

        # 等待章节列表加载，改进的重试机制和多选择器策略
        max_chapter_retries = 5
        count = 0

        # 多种章节选择器策略，按优先级尝试
        chapter_selectors = [
            'li._nO',  # 原始选择器
            '.sound-list li',  # 备用选择器1
            '[data-name="sound-list"] li',  # 备用选择器2
            '.tracklist-item',  # 备用选择器3
            '.episode-item',  # 备用选择器4
            # 新增更多现代化选择器
            'ul[class*="sound"] li',  # 包含sound的ul下的li
            'div[class*="sound"] li',  # 包含sound的div下的li
            'li[class*="_n"]',  # 包含_n的li元素
            'li[data-id]',  # 有data-id属性的li
            '.album-sound-list li',  # 专辑声音列表
            '.track-list li',  # 音轨列表
            '[class*="track"] li',  # 包含track的元素下的li
            '[class*="episode"] li',  # 包含episode的元素下的li
            'li[role="listitem"]',  # 有role属性的li
            'ul li:has([class*="title"])',  # 包含title类的li
            'li:has(.title)',  # 包含title类的li
            'li:has([class*="count"])',  # 包含count类的li
        ]

        for retry_count in range(max_chapter_retries):
            try:
                logger.info(f"等待章节列表加载 (尝试 {retry_count + 1}/{max_chapter_retries})...")

                # 渐进式超时策略：每次重试增加超时时间
                current_timeout = 15000 + (retry_count * 5000)  # 15s, 20s, 25s, 30s, 35s

                # 增强的页面完全加载检查机制
                try:
                    logger.info("检查页面完全加载状态...")
                    
                    # 1. 等待页面基本加载完成
                    page.wait_for_load_state('networkidle', timeout=30000)
                    human_like_delay(1, 2)
                    
                    # 2. 等待DOM内容完全加载
                    page.wait_for_function("document.readyState === 'complete'", timeout=15000)
                    human_like_delay(0.5, 1)
                    
                    # 3. 检查页面是否有加载指示器，等待其消失
                    loading_indicators = [
                        '.loading', '.spinner', '.loader', 
                        '[class*="loading"]', '[class*="spinner"]',
                        '.xm-loading', '.page-loading'
                    ]
                    for indicator in loading_indicators:
                        try:
                            page.wait_for_selector(indicator, state='hidden', timeout=5000)
                        except:
                            pass
                    
                    # 4. 等待页面主要内容区域出现
                    main_content_selectors = [
                        '.album-detail', '.album-info', '.sound-list',
                        '[class*="album"]', '[class*="detail"]', 'main'
                    ]
                    for selector in main_content_selectors:
                        try:
                            page.wait_for_selector(selector, state='attached', timeout=5000)
                            logger.info(f"页面主要内容区域已加载: {selector}")
                            break
                        except:
                            continue
                    
                    logger.info("页面完全加载检查完成")
                    
                except Exception as load_e:
                    logger.warning(f"页面加载检查异常: {load_e}")

                # 尝试滚动触发章节列表加载
                try:
                    logger.info("执行滚动操作触发章节加载...")
                    # 先滚动到页面顶部
                    page.evaluate("window.scrollTo(0, 0)")
                    human_like_delay(0.5, 1)
                    
                    # 缓慢滚动到中部
                    page.evaluate("window.scrollTo({top: window.innerHeight * 0.5, behavior: 'smooth'})")
                    human_like_delay(1, 2)
                    
                    # 继续滚动到下部
                    page.evaluate("window.scrollTo({top: window.innerHeight * 1.5, behavior: 'smooth'})")
                    human_like_delay(1, 2)
                    
                    # 滚动到章节列表可能的位置
                    page.evaluate("window.scrollTo({top: window.innerHeight * 2, behavior: 'smooth'})")
                    human_like_delay(1, 2)
                    
                except Exception as scroll_e:
                    logger.warning(f"滚动操作异常: {scroll_e}")

                # 按优先级尝试不同的选择器
                chapter_items = None
                found_selector = None

                for selector in chapter_selectors:
                    try:
                        logger.info(f"尝试选择器: {selector}")
                        
                        # 智能等待策略：先短时间等待，再逐步增加
                        wait_times = [3000, 5000, current_timeout]  # 3s, 5s, 然后是完整超时
                        
                        for wait_time in wait_times:
                            try:
                                page.wait_for_selector(selector, state='attached', timeout=wait_time)
                                chapter_items = page.locator(selector)
                                count = chapter_items.count()

                                if count > 0:
                                    found_selector = selector
                                    logger.info(f"使用选择器 '{selector}' 成功找到 {count} 个章节 (等待时间: {wait_time}ms)")
                                    break
                                else:
                                    logger.info(f"选择器 '{selector}' 找到元素但数量为0，继续等待...")
                                    if wait_time < current_timeout:
                                        continue
                                    
                            except Exception as wait_e:
                                if wait_time < current_timeout:
                                    logger.info(f"选择器 '{selector}' 在 {wait_time}ms 内未找到，尝试更长等待时间...")
                                    continue
                                else:
                                    raise wait_e
                        
                        if count > 0:
                            break
                            
                    except Exception as selector_e:
                        logger.warning(f"选择器 '{selector}' 失败: {selector_e}")
                        
                        # 在选择器失败后，尝试额外的页面交互
                        try:
                            logger.info(f"选择器 '{selector}' 失败后，尝试页面交互...")
                            # 点击可能触发章节加载的元素
                            trigger_selectors = [
                                '.album-detail', '.sound-list', '.tracklist',
                                '[class*="album"]', '[class*="sound"]', '[class*="track"]'
                            ]
                            for trigger in trigger_selectors:
                                try:
                                    if page.locator(trigger).count() > 0:
                                        page.locator(trigger).first.click(timeout=2000)
                                        human_like_delay(0.5, 1)
                                        break
                                except:
                                    continue
                        except:
                            pass
                        
                        continue

                if count > 0:
                    break
                else:
                    logger.warning(f"第 {retry_count + 1} 次尝试所有选择器均未找到章节")
                    if retry_count < max_chapter_retries - 1:  # 不是最后一次重试
                        # 防风控机制：返回都市分类榜单页面刷新
                        logger.info("防风控机制：返回都市分类榜单页面刷新...")
                        try:
                            page.goto(CONFIG['base_url'], wait_until='networkidle', timeout=60000)
                            human_like_delay(2, 4)
                            # 重新进入小说详情页
                            page.goto(novel_url, wait_until='networkidle', timeout=45000)
                            human_like_delay(2, 4)
                        except Exception as nav_e:
                            logger.error(f"防风控导航失败: {nav_e}，使用页面重载")
                            try:
                                page.reload(wait_until='networkidle', timeout=30000)
                                human_like_delay(2, 4)
                            except Exception as reload_e:
                                logger.error(f"页面重载也失败: {reload_e}")
                                human_like_delay(3, 5)

            except Exception as e:
                logger.error(f"第 {retry_count + 1} 次尝试加载章节列表时出错: {e}")
                if retry_count < max_chapter_retries - 1:  # 不是最后一次重试
                    # 防风控机制：返回都市分类榜单页面刷新
                    logger.info("防风控机制：返回都市分类榜单页面刷新...")
                    try:
                        page.goto(CONFIG['base_url'], wait_until='networkidle', timeout=60000)
                        human_like_delay(2, 4)
                        # 重新进入小说详情页
                        page.goto(novel_url, wait_until='networkidle', timeout=45000)
                        human_like_delay(2, 4)
                    except Exception as nav_e:
                        logger.error(f"防风控导航失败: {nav_e}，使用页面重载")
                        try:
                            page.reload(wait_until='networkidle', timeout=30000)
                            human_like_delay(2, 4)
                        except Exception as reload_e:
                            logger.error(f"页面重载也失败: {reload_e}")
                            human_like_delay(3, 5)
                    
        if count == 0:
            logger.warning("经过5次重试仍然未找到章节，跳过章节爬取")
        else:
            logger.info(f"最终找到 {count} 个章节")

        for i in range(count):
            chapter_data = {'chapter_order_type':'ASC'}

            try:
                # 章节名称
                chapter_title_element = chapter_items.nth(i).locator('span.title._nO')
                if chapter_title_element.is_visible():
                    chapter_data['title'] = chapter_title_element.inner_text()
                else:
                    chapter_data['title'] = "未找到"
            except Exception as e:
                logger.error(f"获取章节标题失败: {e}")
                chapter_data['title'] = "获取失败"

            try:
                # 章节播放量
                chapter_play_element = chapter_items.nth(i).locator('span.count._nO')
                if chapter_play_element.is_visible():
                    play_text = chapter_play_element.inner_text()
                    # 使用正则表达式提取数字和单位
                    play_match = re.search(r'[\d.]+[亿万千]*', play_text)
                    chapter_data['plays'] = play_match.group(0) if play_match else play_text
                else:
                    chapter_data['plays'] = "未找到"
            except Exception as e:
                logger.error(f"获取章节播放量失败: {e}")
                chapter_data['plays'] = "获取失败"

            try:
                # 章节上架时间
                chapter_time_element = chapter_items.nth(i).locator('span.time._nO')
                if chapter_time_element.is_visible():
                    chapter_data['publish_time'] = chapter_time_element.inner_text()
                else:
                    chapter_data['publish_time'] = "未找到"
            except Exception as e:
                logger.error(f"获取章节上架时间失败: {e}")
                chapter_data['publish_time'] = "获取失败"

            all_chapters.append(chapter_data)

        novel_data['chapters'] = all_chapters
        logger.info(f"第一页章节爬取完成，共获取 {len(all_chapters)} 个章节")

        # 搜索匹配的第一集章节并点击进入详情页
        if len(all_chapters) > 0:
            logger.info("正在搜索匹配第一集关键词的章节...")
            first_episode_chapter = find_first_episode_chapter(all_chapters)

            if first_episode_chapter:
                chapter_title = first_episode_chapter.get('title', '')
                logger.info(f"找到匹配的第一集章节，准备点击: {chapter_title}")

                try:
                    # 查找并点击对应的章节元素 - 改进章节定位逻辑
                    chapter_elements = page.locator('li._nO')
                    chapter_count = chapter_elements.count()
                    logger.info(f"页面上共找到 {chapter_count} 个章节元素")

                    clicked_chapter = False
                    target_chapter_element = None
                    
                    # 首先遍历所有章节，找到精确匹配的章节
                    for i in range(chapter_count):
                        try:
                            chapter_element = chapter_elements.nth(i)
                            
                            # 尝试多种标题选择器
                            title_selectors = [
                                'span.title._nO',
                                '.title',
                                'a[title]',
                                'span[class*="title"]'
                            ]
                            
                            element_title = None
                            for title_selector in title_selectors:
                                try:
                                    title_element = chapter_element.locator(title_selector).first
                                    if title_element.is_visible():
                                        element_title = title_element.inner_text().strip()
                                        break
                                except:
                                    continue
                            
                            # 如果通过title属性获取
                            if not element_title:
                                try:
                                    link_element = chapter_element.locator('a[title]').first
                                    if link_element.is_visible():
                                        element_title = link_element.get_attribute('title').strip()
                                except:
                                    pass
                            
                            if element_title:
                                logger.info(f"第 {i+1} 个章节元素标题: {element_title}")
                                
                                # 精确匹配章节标题
                                if element_title == chapter_title:
                                    logger.info(f"找到精确匹配的章节元素 (索引 {i}): {element_title}")
                                    target_chapter_element = chapter_element
                                    break
                            else:
                                logger.warning(f"第 {i+1} 个章节元素无法获取标题")
                                
                        except Exception as e:
                            logger.warning(f"处理第 {i+1} 个章节元素时出错: {e}")
                            continue
                    
                    if target_chapter_element:
                        logger.info(f"准备点击匹配的章节: {chapter_title}")
                        
                        detail_success = False
                        try:
                            # 记录当前URL，用于检测页面跳转
                            current_url = page.url
                            logger.info(f"点击前URL: {current_url}")
                            
                            # 简化策略：直接使用URL跳转，不再尝试点击
                            click_success = False
                            
                            try:
                                logger.info("直接通过URL导航到章节页面...")
                                # 获取章节链接
                                link_element = target_chapter_element.locator('a[href]').first
                                if link_element.is_visible():
                                    chapter_href = link_element.get_attribute('href')
                                    if chapter_href:
                                        # 构造完整URL
                                        if chapter_href.startswith('/'):
                                            chapter_url = f"https://www.ximalaya.com{chapter_href}"
                                        else:
                                            chapter_url = chapter_href
                                        
                                        logger.info(f"直接导航到章节URL: {chapter_url}")
                                        # 使用更短的超时时间和更宽松的等待条件
                                        page.goto(chapter_url, wait_until='domcontentloaded', timeout=15000)
                                        click_success = True
                                        logger.info("URL导航成功")
                                    else:
                                        logger.warning("无法获取章节href属性")
                                else:
                                    logger.warning("无法找到章节链接元素")
                                    
                            except Exception as nav_e:
                                logger.warning(f"URL导航失败: {nav_e}")
                            
                            if not click_success:
                                logger.error("URL导航失败，无法跳转到章节页面")
                                raise Exception("章节导航失败，页面未跳转")
                            
                            # 如果成功跳转，等待章节详情页加载
                            logger.info("章节点击成功，等待章节详情页加载...")
                            human_like_delay(2.0, 3.0)  # 等待页面稳定
                            
                            # 记录跳转后的URL
                            new_url = page.url
                            logger.info(f"点击后URL: {new_url}")
                            
                            # 等待页面稳定
                            human_like_delay(2.0, 3.0)

                            # 抓取章节详情页信息
                            chapter_detail = scrape_chapter_detail_page(page, chapter_title)
                            novel_data['first_episode_detail'] = chapter_detail

                            logger.info(f"章节详情抓取完成: {chapter_detail}")

                            # 更新章节数据中的上架时间信息
                            if chapter_detail.get('publish_time') and chapter_detail['publish_time'] != "未找到":
                                # 在章节列表中找到对应章节，更新其上架时间
                                for chapter in all_chapters:
                                    if chapter.get('title') == chapter_title:
                                        chapter['detail_publish_time'] = chapter_detail['publish_time']
                                        chapter['detail_title'] = chapter_detail.get('detail_title', chapter_title)
                                        chapter['duration'] = chapter_detail.get('duration', '')
                                        chapter['detail_play_count'] = chapter_detail.get('play_count', '')
                                        logger.info(f"已更新章节 {chapter_title} 的详情页信息")
                                        break

                            detail_success = True

                        except Exception as detail_e:
                            logger.error(f"抓取章节详情时出错: {detail_e}")
                            novel_data['first_episode_detail'] = {"error": str(detail_e)}
                        finally:
                            # 无论成功与否都要尝试返回
                            try:
                                logger.info("尝试返回小说详情页...")
                                page.go_back()
                                human_like_delay(2.0, 3.0)
                                
                                # 增加重试机制等待小说详情页重新加载
                                max_retries = 3
                                for attempt in range(max_retries):
                                    try:
                                        page.wait_for_selector('li._nO', state='attached', timeout=30000)
                                        logger.info("成功返回小说详情页")
                                        break
                                    except Exception as e:
                                        if attempt < max_retries - 1:
                                            logger.warning(f"等待小说详情页加载失败，第{attempt + 1}次重试: {e}")
                                            human_like_delay(2.0, 4.0)
                                            # 尝试刷新页面
                                            try:
                                                page.reload(wait_until='networkidle', timeout=30000)
                                            except:
                                                pass
                                            continue
                                        else:
                                            # 尝试备用选择器
                                            try:
                                                page.wait_for_selector('.album-detail', timeout=15000)
                                                logger.info("使用备用选择器成功返回小说详情页")
                                            except:
                                                raise e
                                                        
                            except Exception as back_e:
                                logger.error(f"返回小说详情页失败: {back_e}")
                                # 如果返回失败，尝试直接导航到小说详情页
                                try:
                                    current_url = page.url
                                    if '/sound/' in current_url:
                                        # 从章节页面提取小说ID并重新导航
                                        novel_url = novel_data.get('novel_url', '')
                                        if novel_url:
                                            page.goto(novel_url, wait_until='networkidle', timeout=30000)
                                            human_like_delay(2.0, 3.0)
                                            logger.info("通过直接导航返回小说详情页")
                                except Exception as nav_e:
                                    logger.error(f"直接导航也失败: {nav_e}")

                                clicked_chapter = True if detail_success else False

                    if not clicked_chapter:
                        logger.warning(f"未能找到或点击匹配的章节: {chapter_title}")
                        novel_data['first_episode_detail'] = {"error": "未能点击章节"}

                except Exception as search_e:
                    logger.error(f"搜索和点击匹配章节时出错: {search_e}")
                    novel_data['first_episode_detail'] = {"error": str(search_e)}
            else:
                logger.info("未找到匹配第一集关键词的章节")
                novel_data['first_episode_detail'] = {"message": "未找到匹配的第一集章节"}

    except Exception as e:
        logger.error(f"爬取章节列表时出错: {e}")
        novel_data['chapters'] = all_chapters  # 保存已爬取的部分

    # 点击倒序按钮并爬取倒序章节数据
    reverse_chapters = []
    try:
        logger.info("尝试点击倒序按钮...")
        reverse_btn = page.locator('a[href="javascript:;"].H_g >> text=倒序')
        
        if reverse_btn.is_visible():
            logger.info("找到倒序按钮，模拟人类点击...")
            human_like_click(page, 'a[href="javascript:;"].H_g >> text=倒序', "倒序按钮")
            
            # 等待页面刷新
            human_like_delay(2.0, 3.0)
            
            # 等待倒序章节列表加载，添加重试机制（防风控）
            max_reverse_retries = 5
            reverse_count = 0
            
            for retry_count in range(max_reverse_retries):
                try:
                    logger.info(f"等待倒序章节列表加载 (尝试 {retry_count + 1}/{max_reverse_retries})...")
                    page.wait_for_selector('li._nO', state='attached', timeout=15000)
                    
                    # 获取倒序后的第一页章节
                    reverse_chapter_items = page.locator('li._nO')
                    reverse_count = reverse_chapter_items.count()
                    
                    if reverse_count > 0:
                        logger.info(f"倒序模式下成功找到 {reverse_count} 个章节")
                        break
                    else:
                        logger.warning(f"第 {retry_count + 1} 次尝试未找到倒序章节")
                        if retry_count < max_reverse_retries - 1:  # 不是最后一次重试
                            logger.info("防风控机制：返回都市分类榜单页面刷新后重试...")
                            try:
                                page.goto(CONFIG['base_url'], wait_until='networkidle')
                                human_like_delay(2.0, 3.0)
                                # 重新导航到小说详情页
                                page.goto(novel_url, wait_until='networkidle')
                                human_like_delay(1.5, 2.5)
                            except Exception as nav_e:
                                logger.warning(f"导航失败，使用页面重载: {nav_e}")
                                page.reload()
                                human_like_delay(1.5, 2.5)
                            # 重新点击倒序按钮
                            reverse_btn = page.locator('a[href="javascript:;"].H_g >> text=倒序')
                            if reverse_btn.is_visible():
                                human_like_click(page, 'a[href="javascript:;"].H_g >> text=倒序', "倒序按钮")
                                human_like_delay(1.0, 1.5)
                            
                except Exception as e:
                    logger.error(f"第 {retry_count + 1} 次尝试加载倒序章节列表时出错: {e}")
                    if retry_count < max_reverse_retries - 1:  # 不是最后一次重试
                        logger.info("防风控机制：返回都市分类榜单页面刷新后重试...")
                        try:
                            page.goto(CONFIG['base_url'], wait_until='networkidle')
                            human_like_delay(2.0, 3.0)
                            # 重新导航到小说详情页
                            page.goto(novel_url, wait_until='networkidle')
                            human_like_delay(1.5, 2.5)
                        except Exception as nav_e:
                            logger.warning(f"导航失败，使用页面重载: {nav_e}")
                            page.reload()
                            human_like_delay(1.5, 2.5)
                        # 重新点击倒序按钮
                        reverse_btn = page.locator('a[href="javascript:;"].H_g >> text=倒序')
                        if reverse_btn.is_visible():
                            human_like_click(page, 'a[href="javascript:;"].H_g >> text=倒序', "倒序按钮")
                            human_like_delay(2.0, 3.0)
                            
            if reverse_count == 0:
                logger.warning("经过5次重试仍然未找到倒序章节，跳过倒序章节爬取")
            else:
                logger.info(f"最终找到 {reverse_count} 个倒序章节")
            
            for i in range(reverse_count):
                chapter_data = {'chapter_order_type':'desc'}
                
                try:
                    # 章节名称
                    chapter_title_element = reverse_chapter_items.nth(i).locator('span.title._nO')
                    if chapter_title_element.is_visible():
                        chapter_data['title'] = chapter_title_element.inner_text()
                    else:
                        chapter_data['title'] = "未找到"
                except Exception as e:
                    logger.error(f"获取倒序章节标题失败: {e}")
                    chapter_data['title'] = "获取失败"
                
                try:
                    # 章节播放量
                    chapter_play_element = reverse_chapter_items.nth(i).locator('span.count._nO')
                    if chapter_play_element.is_visible():
                        play_text = chapter_play_element.inner_text()
                        play_match = re.search(r'[\d.]+[亿万千]*', play_text)
                        chapter_data['plays'] = play_match.group(0) if play_match else play_text
                    else:
                        chapter_data['plays'] = "未找到"
                except Exception as e:
                    logger.error(f"获取倒序章节播放量失败: {e}")
                    chapter_data['plays'] = "获取失败"
                
                try:
                    # 章节上架时间
                    chapter_time_element = reverse_chapter_items.nth(i).locator('span.time._nO')
                    if chapter_time_element.is_visible():
                        chapter_data['publish_time'] = chapter_time_element.inner_text()
                    else:
                        chapter_data['publish_time'] = "未找到"
                except Exception as e:
                    logger.error(f"获取倒序章节上架时间失败: {e}")
                    chapter_data['publish_time'] = "获取失败"
                
                reverse_chapters.append(chapter_data)
            
            novel_data['reverse_chapters'] = reverse_chapters
            logger.info(f"倒序第一页章节爬取完成，共获取 {len(reverse_chapters)} 个章节")

            # 搜索匹配的第一集章节并点击进入详情页（倒序模式）
            if len(reverse_chapters) > 0:
                logger.info("在倒序模式下搜索匹配第一集关键词的章节...")
                first_episode_chapter_reverse = find_first_episode_chapter(reverse_chapters)

                if first_episode_chapter_reverse:
                    chapter_title = first_episode_chapter_reverse.get('title', '')
                    logger.info(f"倒序模式下找到匹配的第一集章节，准备点击: {chapter_title}")

                    try:
                        # 查找并点击对应的章节元素（倒序）
                        reverse_chapter_elements = page.locator('li._nO')
                        reverse_chapter_count = reverse_chapter_elements.count()

                        clicked_chapter = False
                        for i in range(reverse_chapter_count):
                            try:
                                chapter_element = reverse_chapter_elements.nth(i)
                                element_title = chapter_element.locator('span.title._nO').inner_text()

                                if element_title == chapter_title:
                                    logger.info(f"倒序模式下找到匹配的章节元素，模拟点击: {element_title}")

                                    detail_success = False
                                    try:
                                        # 在点击章节前使用增强的验证码检测
                                        logger.info("倒序模式点击章节前检测验证码...")
                                        
                                        # 使用统一的验证码检测函数
                                        captcha_detected = check_captcha_on_page(page)
                                        
                                        if captcha_detected:
                                            logger.info("验证码已处理，继续点击章节")
                                        else:
                                            logger.info("未检测到验证码，直接点击章节")
                                        
                                        # 等待一下确保页面稳定
                                        human_like_delay(0.5, 1.0)
                                        
                                        if captcha_detected:
                                            logger.info("验证码已处理，继续点击章节")
                                        else:
                                            logger.info("未检测到验证码，直接点击章节")
                                        
                                        # 使用多种点击策略来绕过验证码拦截
                                        logger.info("倒序模式开始点击章节...")
                                        click_success = False
                                        
                                        # 策略1: 尝试JavaScript点击（绕过拦截）
                                        try:
                                            logger.info("尝试JavaScript点击...")
                                            page.evaluate("""
                                                (element) => {
                                                    if (element) {
                                                        element.click();
                                                        return true;
                                                    }
                                                    return false;
                                                }
                                            """, chapter_element.element_handle())
                                            click_success = True
                                            logger.info("JavaScript点击成功")
                                        except Exception as js_e:
                                            logger.warning(f"JavaScript点击失败: {js_e}")
                                        
                                        # 策略2: 如果JavaScript点击失败，尝试force点击
                                        if not click_success:
                                            try:
                                                logger.info("尝试force点击...")
                                                chapter_element.click(force=True)
                                                click_success = True
                                                logger.info("force点击成功")
                                            except Exception as force_e:
                                                logger.warning(f"force点击失败: {force_e}")
                                        
                                        # 策略3: 如果前两种都失败，尝试等待验证码消失后再点击
                                        if not click_success:
                                            logger.info("前两种点击策略失败，等待验证码消失后重试...")
                                            human_like_delay(5.0, 8.0)
                                            
                                            # 再次检查验证码状态
                                            captcha_still_exists = False
                                            try:
                                                captcha_elements = page.locator('div[class*="geetest_bg"], div[class*="geetest_popup_ghost"], div[class*="geetest_captcha"][class*="geetest_boxShow"]')
                                                if captcha_elements.count() > 0:
                                                    for i in range(captcha_elements.count()):
                                                        if captcha_elements.nth(i).is_visible():
                                                            captcha_still_exists = True
                                                            break
                                            except:
                                                pass
                                            
                                            if captcha_still_exists:
                                                logger.warning("验证码仍然存在，尝试再次处理...")
                                                try:
                                                    handle_captcha(page)
                                                    human_like_delay(3.0, 5.0)
                                                except:
                                                    pass
                                            
                                            # 最后尝试普通点击
                                            try:
                                                logger.info("最后尝试普通点击...")
                                                chapter_element.click()
                                                click_success = True
                                                logger.info("普通点击成功")
                                            except Exception as normal_e:
                                                logger.error(f"所有点击策略都失败: {normal_e}")
                                                raise normal_e
                                        
                                        if click_success:
                                            logger.info("章节点击成功，等待页面加载...")
                                            human_like_delay(2.0, 3.0)

                                        # 抓取章节详情页信息
                                        chapter_detail_reverse = scrape_chapter_detail_page(page, chapter_title)
                                        novel_data['first_episode_detail_reverse'] = chapter_detail_reverse

                                        logger.info(f"倒序模式章节详情抓取完成: {chapter_detail_reverse}")

                                        # 更新倒序章节数据中的上架时间信息
                                        if chapter_detail_reverse.get('publish_time') and chapter_detail_reverse['publish_time'] != "未找到":
                                            # 在倒序章节列表中找到对应章节，更新其上架时间
                                            for chapter in reverse_chapters:
                                                if chapter.get('title') == chapter_title:
                                                    chapter['detail_publish_time'] = chapter_detail_reverse['publish_time']
                                                    chapter['detail_title'] = chapter_detail_reverse.get('detail_title', chapter_title)
                                                    chapter['duration'] = chapter_detail_reverse.get('duration', '')
                                                    chapter['detail_play_count'] = chapter_detail_reverse.get('play_count', '')
                                                    logger.info(f"已更新倒序章节 {chapter_title} 的详情页信息")
                                                    break

                                        detail_success = True

                                    except Exception as detail_e:
                                        logger.error(f"倒序模式抓取章节详情时出错: {detail_e}")
                                        novel_data['first_episode_detail_reverse'] = {"error": str(detail_e)}
                                    finally:
                                        # 无论成功与否都要尝试返回
                                        try:
                                            logger.info("倒序模式尝试返回小说详情页...")
                                            page.go_back()
                                            human_like_delay(2.0, 3.0)
                                            
                                            # 增加重试机制等待小说详情页重新加载
                                            max_retries = 5  # 增加重试次数
                                            for attempt in range(max_retries):
                                                try:
                                                    # 使用多个选择器尝试等待页面加载
                                                    selectors_to_try = [
                                                        'li._nO',
                                                        '.album-detail',
                                                        '.sound-list',
                                                        '[class*="sound-list"]',
                                                        '.album-info'
                                                    ]
                                                    
                                                    page_loaded = False
                                                    for selector in selectors_to_try:
                                                        try:
                                                            page.wait_for_selector(selector, state='attached', timeout=15000)
                                                            logger.info(f"倒序模式使用选择器 {selector} 成功返回小说详情页")
                                                            page_loaded = True
                                                            break
                                                        except:
                                                            continue
                                                    
                                                    if page_loaded:
                                                        break
                                                    else:
                                                        raise Exception("所有选择器都无法找到页面元素")
                                                        
                                                except Exception as e:
                                                    if attempt < max_retries - 1:
                                                        logger.warning(f"等待小说详情页加载失败，第{attempt + 1}次重试: {e}")
                                                        human_like_delay(3.0, 5.0)  # 增加等待时间
                                                        
                                                        # 尝试不同的恢复策略
                                                        if attempt == 0:
                                                            # 第一次重试：刷新页面
                                                            try:
                                                                logger.info("尝试刷新页面...")
                                                                page.reload(wait_until='networkidle', timeout=20000)
                                                            except:
                                                                logger.warning("页面刷新失败")
                                                        elif attempt == 1:
                                                            # 第二次重试：再次后退
                                                            try:
                                                                logger.info("尝试再次后退...")
                                                                page.go_back()
                                                                human_like_delay(2.0, 3.0)
                                                            except:
                                                                logger.warning("再次后退失败")
                                                        elif attempt == 2:
                                                            # 第三次重试：检测并处理可能的验证码
                                                            try:
                                                                logger.info("检测是否有验证码阻挡...")
                                                                captcha_selectors = [
                                                                    '.geetest_captcha',
                                                                    '[class*="geetest_captcha"]'
                                                                ]
                                                                captcha_found = False
                                                                for selector in captcha_selectors:
                                                                    if page.locator(selector).count() > 0:
                                                                        elements = page.locator(selector)
                                                                        for i in range(elements.count()):
                                                                            if elements.nth(i).is_visible():
                                                                                logger.info("发现验证码，尝试处理...")
                                                                                handle_captcha(page)
                                                                                captcha_found = True
                                                                                break
                                                                        if captcha_found:
                                                                            break
                                                            except Exception as captcha_e:
                                                                logger.error(f"处理验证码时出错: {captcha_e}")
                                                        continue
                                                    else:
                                                        raise e
                                                            
                                        except Exception as back_e:
                                            logger.error(f"倒序模式返回小说详情页失败: {back_e}")
                                            # 如果返回失败，尝试直接导航到小说详情页
                                            try:
                                                current_url = page.url
                                                if '/sound/' in current_url:
                                                    # 从章节页面提取小说ID并重新导航
                                                    novel_url = novel_data.get('novel_url', '')
                                                    if novel_url:
                                                        page.goto(novel_url, wait_until='networkidle', timeout=30000)
                                                        human_like_delay(2.0, 3.0)
                                                        # 重新点击倒序按钮
                                                        try:
                                                            reverse_btn_retry = page.locator('a[href="javascript:;"].H_g >> text=倒序')
                                                            if reverse_btn_retry.is_visible():
                                                                reverse_btn_retry.click()
                                                                human_like_delay(2.0, 3.0)
                                                        except:
                                                            pass
                                                        logger.info("倒序模式通过直接导航返回小说详情页")
                                            except Exception as nav_e:
                                                logger.error(f"倒序模式直接导航也失败: {nav_e}")

                                    clicked_chapter = True if detail_success else False
                                    break

                            except Exception as click_e:
                                logger.error(f"倒序模式下点击章节 {element_title} 时出错: {click_e}")
                                continue

                        if not clicked_chapter:
                            logger.warning(f"倒序模式下未能找到或点击匹配的章节: {chapter_title}")
                            novel_data['first_episode_detail_reverse'] = {"error": "未能点击章节"}

                    except Exception as search_e:
                        logger.error(f"倒序模式下搜索和点击匹配章节时出错: {search_e}")
                        novel_data['first_episode_detail_reverse'] = {"error": str(search_e)}
                else:
                    logger.info("倒序模式下未找到匹配第一集关键词的章节")
                    novel_data['first_episode_detail_reverse'] = {"message": "未找到匹配的第一集章节"}

        else:
            logger.info("未找到倒序按钮")
            novel_data['reverse_chapters'] = []
            
    except Exception as e:
        logger.error(f"爬取倒序章节列表时出错: {e}")
        novel_data['reverse_chapters'] = reverse_chapters  # 保存已爬取的部分

    # 添加小说详情页URL到数据中
    novel_data['novel_url'] = page.url

    return novel_data


def crawl_novels_data(page, category_name="未知分类", base_dir=None):
    """遍历榜单小说并爬取数据（收集模式，最后统一保存）"""
    all_novels_data = []

    try:
        # 等待榜单页面加载完成
        page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)  # 增加榜单页面加载超时时间

        # 获取所有小说项
        novel_items = page.locator('div.album-item._Sq')
        count = novel_items.count()

        logger.info(f"发现 {count} 个小说")

        if count == 0:
            logger.warning("未找到小说项，请检查页面状态")
            return all_novels_data

        # 爬取所有小说
        actual_count = count
        logger.info(f"准备爬取 {actual_count} 个小说")
        
        # 遍历每个小说
        i = 0
        while i < actual_count:
            current_position = i + 1
            max_retries = CONFIG['max_retries']  # 最大重试次数
            retry_count = 0
            success = False

            logger.info(f"\n===== 开始处理第 {current_position} 个小说 (共{actual_count}个) =====\n")

            while retry_count < max_retries and not success:
                try:
                    if retry_count > 0:
                        logger.info(f"第 {retry_count + 1} 次尝试处理第 {current_position} 个小说")

                    # 重新获取当前项（防止页面刷新后元素失效）
                    current_item = page.locator('div.album-item._Sq').nth(i)

                    # 获取小说标题
                    title_element = current_item.locator('div.title._Sq')
                    title = title_element.inner_text(timeout=5000)
                    logger.info(f"小说标题: {title}")

                    # 处理之前遗留的验证码
                    captcha_status = check_captcha_on_page(page)
                    if captcha_status:
                        logger.info("处理遗留验证码")
                        handle_captcha(page)
                        human_like_delay(2.0, 3.0)
                    else:
                        logger.info("该小说无遗留验证码")

                    # 模拟人类滚动到该元素位置
                    logger.info("滚动到小说位置...")
                    current_item.scroll_into_view_if_needed()
                    human_like_delay(0.5, 1.5)

                    # 获取当前小说项中的链接元素
                    novel_link = current_item.locator('a.album-right._Sq').first

                    # 模拟人类点击进入详情页
                    logger.info(f"点击进入详情页: {title}")
                    with page.expect_navigation(timeout=60000):  # 增加导航超时时间到60秒
                        # 滚动到链接位置并点击
                        novel_link.scroll_into_view_if_needed()
                        human_like_delay(0.3, 0.8)
                        novel_link.click()
                        logger.info(f"已点击小说《{title}》的链接")

                    # 等待详情页加载
                    logger.info("等待详情页加载...")
                    page.wait_for_load_state('load', timeout=45000)  # 增加加载超时时间到45秒

                    # 详情页加载后模拟人类浏览行为
                    logger.info("模拟浏览小说详情页...")
                    simulate_browsing_behavior(page, duration_range=(3, 6))

                    # 检查验证码
                    captcha_status = check_captcha_on_page(page)
                    if captcha_status:
                        logger.info("处理验证码")
                        handle_captcha(page)
                        human_like_delay(2.0, 3.0)
                    else:
                        logger.info("该小说无验证码")

                    # 爬取小说详情数据（只爬取第一页）
                    logger.info("开始爬取小说详情数据...")
                    novel_data = scrape_novel_details_first_page(page, title)
                    novel_data['rank'] = current_position  # 添加排名信息
                    novel_data['category'] = category_name  # 添加分类信息
                    all_novels_data.append(novel_data)


                    chapters = novel_data.get('chapters')
                    reverse_chapters = novel_data.get('reverse_chapters')

                    def extract_episode_number(chapters):
                        """
                        chapters: 按播放顺序排列的章节列表，每个元素是 dict，必须含有 'title' 字段。
                        return: 匹配到的集号（int），如果整部列表都没有符合规则的标题则返回 None。
                        """
                        # 先倒序，保证“最后一集”优先
                        for ch in reversed(chapters):
                            title = ch.get('title', '')
                            m = re.search(r'第(\d+)集', title)
                            m_ = re.search(r'(\d+)', title)
                            if m:
                                return int(m.group(1))
                            else:
                                if m_:
                                    return int(m_.group(1))

                        return None
                    num = extract_episode_number(reverse_chapters)
                    novel_data['chapter_count'] = num

                    logger.info(f"爬取完成: {novel_data['novel_title']}")
                    logger.info(f"总播放量: {novel_data['total_plays']}")
                    logger.info(f"主播: {novel_data['anchor_name']}")
                    logger.info(f"章节数: {num}")

                    # 将小说数据添加到收集列表中，稍后统一保存
                    logger.info(f"小说《{novel_data['novel_title']}》数据已收集，等待最后统一保存")

                    # 返回榜单页面（使用浏览器后退按钮）
                    logger.info("返回榜单页面...")
                    try:
                        # 增加重试机制返回榜单页面
                        max_back_retries = 3
                        back_success = False
                        
                        for back_attempt in range(max_back_retries):
                            try:
                                # 使用浏览器后退功能
                                page.go_back()
                                human_like_delay(2.0, 3.0)

                                # 等待URL变化，增加超时时间到90秒
                                page.wait_for_url('**/top/**', timeout=90000)

                                # 等待关键元素加载，增加超时时间到90秒
                                page.wait_for_selector('div.album-item._Sq', state='attached', timeout=90000)

                                # 返回榜单页面后模拟人类浏览行为
                                logger.info("返回榜单页面后模拟浏览...")
                                simulate_browsing_behavior(page, duration_range=(2, 4))

                                logger.info("成功返回榜单页面")
                                back_success = True
                                break
                                
                            except Exception as back_e:
                                if back_attempt < max_back_retries - 1:
                                    logger.warning(f"返回榜单页面失败，第{back_attempt + 1}次重试: {back_e}")
                                    human_like_delay(3.0, 5.0)
                                    # 尝试刷新页面
                                    try:
                                        page.reload(wait_until='networkidle', timeout=30000)
                                    except:
                                        pass
                                    continue
                                else:
                                    raise back_e
                        
                        if not back_success:
                            raise Exception("所有返回榜单页面的重试都失败了")
                            
                    except Exception as e:
                        logger.error(f"返回榜单页面时出错: {str(e)}")

                        # 尝试直接导航回榜单页面
                        logger.info("尝试直接导航回榜单页面...")
                        try:
                            page.goto('https://www.ximalaya.com/top/', timeout=90000)
                            page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)

                            # 添加额外等待和滚动
                            human_like_delay(3.0, 5.0)
                            human_like_scroll(page)
                            logger.info("直接导航回榜单页面成功")
                        except Exception as nav_e:
                            logger.error(f"直接导航回榜单页面也失败: {nav_e}")
                            # 尝试备用榜单页面URL
                            try:
                                page.goto('https://www.ximalaya.com/top/all', timeout=90000)
                                page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)
                                human_like_delay(3.0, 5.0)
                                logger.info("使用备用榜单页面URL成功")
                            except Exception as backup_e:
                                logger.error(f"备用榜单页面URL也失败: {backup_e}")
                                raise Exception("所有返回榜单页面的方法都失败了")

                    # 等待一段时间再处理下一个
                    human_like_delay(1.5, 3.0)

                    # 标记成功
                    success = True
                    logger.info(f"第 {current_position} 个小说处理成功")

                except Exception as e:
                    retry_count += 1
                    logger.error(f"处理第 {current_position} 个小说时出错 (第{retry_count}次尝试): {str(e)}")

                    # 检查是否为浏览器关闭错误
                    if is_browser_closed_error(str(e)):
                        logger.warning("检测到浏览器关闭错误，尝试重新创建浏览器实例...")
                        browser, context, page, recovery_success = handle_browser_closed_error(logger, browser, context, page)
                        
                        if recovery_success:
                            logger.info("浏览器实例重新创建成功，重新获取小说列表...")
                            # 重新获取小说数量
                            novel_items = page.locator('div.album-item._Sq')
                            count = novel_items.count()
                            logger.info(f"重新获取到 {count} 个小说")
                            
                            # 调整当前索引
                            if i >= count:
                                logger.warning(f"当前索引 {i} 超出范围，调整为最后一个小说")
                                i = count - 1
                                current_position = i + 1
                            
                            # 重置重试计数，继续处理
                            retry_count = 0
                            continue
                        else:
                            logger.error("浏览器实例重新创建失败，停止处理")
                            break

                    if retry_count < max_retries:
                        logger.info(f"准备进行第 {retry_count + 1} 次重试...")

                        try:
                            # 第一次重试：刷新当前页面清理缓存
                            if retry_count == 1:
                                logger.info("第一次重试：刷新当前页面清理缓存...")
                                page.reload(timeout=60000)
                                page.wait_for_load_state('load', timeout=45000)
                                human_like_delay(2.0, 4.0)

                                # 检查是否回到了榜单页面
                                try:
                                    page.wait_for_selector('div.album-item._Sq', state='attached', timeout=10000)
                                    logger.info("刷新后仍在榜单页面")
                                except:
                                    logger.info("刷新后不在榜单页面，导航回榜单页面")
                                    page.goto('https://www.ximalaya.com/top/', timeout=90000)
                                    page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)
                                    human_like_delay(2.0, 4.0)

                            # 第二次及以后重试：返回榜单页面重新开始
                            else:
                                logger.info("返回榜单页面重新开始...")
                                try:
                                    # 尝试后退到榜单页面
                                    page.go_back()
                                    page.wait_for_url('**/top/**', timeout=30000)
                                except:
                                    # 如果后退失败，直接导航
                                    logger.info("后退失败，直接导航到榜单页面")
                                    page.goto('https://www.ximalaya.com/top/', timeout=90000)

                                # 等待榜单页面加载
                                page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)
                                human_like_delay(2.0, 4.0)

                                # 重新获取小说数量（可能页面已更新）
                                novel_items = page.locator('div.album-item._Sq')
                                new_count = novel_items.count()
                                if new_count != count:
                                    logger.info(f"页面更新，小说数量从 {count} 变为 {new_count}")
                                    count = new_count
                                    if i >= count:
                                        logger.warning(f"当前索引 {i} 超出范围，调整为最后一个小说")
                                        i = count - 1
                                        current_position = i + 1

                        except Exception as recovery_error:
                            logger.error(f"恢复操作失败: {str(recovery_error)}")
                            
                            # 检查恢复操作失败是否为浏览器关闭错误
                            if is_browser_closed_error(str(recovery_error)):
                                logger.warning("恢复操作中检测到浏览器关闭错误，尝试重新创建浏览器实例...")
                                browser, context, page, recovery_success = handle_browser_closed_error(logger, browser, context, page)
                                
                                if recovery_success:
                                    logger.info("恢复操作中浏览器实例重新创建成功")
                                    # 重新获取小说数量
                                    novel_items = page.locator('div.album-item._Sq')
                                    count = novel_items.count()
                                    logger.info(f"重新获取到 {count} 个小说")
                                    
                                    # 调整当前索引
                                    if i >= count:
                                        logger.warning(f"当前索引 {i} 超出范围，调整为最后一个小说")
                                        i = count - 1
                                        current_position = i + 1
                                    continue
                                else:
                                    logger.error("恢复操作中浏览器实例重新创建失败，停止处理")
                                    break
                            
                            # 如果恢复失败，尝试重新导航到榜单页面
                            try:
                                page.goto('https://www.ximalaya.com/top/', timeout=90000)
                                page.wait_for_selector('div.album-item._Sq', state='attached', timeout=60000)
                                human_like_delay(3.0, 5.0)
                            except Exception as final_error:
                                logger.error(f"最终恢复尝试也失败: {str(final_error)}")
                                
                                # 检查最终恢复尝试失败是否为浏览器关闭错误
                                if is_browser_closed_error(str(final_error)):
                                    logger.warning("最终恢复尝试中检测到浏览器关闭错误，尝试重新创建浏览器实例...")
                                    browser, context, page, final_recovery_success = handle_browser_closed_error(logger, browser, context, page)
                                    
                                    if final_recovery_success:
                                        logger.info("最终恢复尝试中浏览器实例重新创建成功")
                                        # 重新获取小说数量
                                        novel_items = page.locator('div.album-item._Sq')
                                        count = novel_items.count()
                                        logger.info(f"重新获取到 {count} 个小说")
                                        
                                        # 调整当前索引
                                        if i >= count:
                                            logger.warning(f"当前索引 {i} 超出范围，调整为最后一个小说")
                                            i = count - 1
                                            current_position = i + 1
                                        continue
                                    else:
                                        logger.error("最终恢复尝试中浏览器实例重新创建失败，停止处理")
                                        break
                                else:
                                    break
                    else:
                        logger.error(
                            f"第 {current_position} 个小说处理失败，已达到最大重试次数 {max_retries}，跳过该小说")

            # 移动到下一个小说
            i += 1

        logger.info(f"\n===== 已完成所有小说访问，共爬取 {len(all_novels_data)} 个小说 =====\n")

    except Exception as e:
        logger.error(f"遍历榜单小说时出错: {str(e)}")
        
        # 检查是否为浏览器关闭错误
        if is_browser_closed_error(str(e)):
            logger.warning("遍历榜单小说时检测到浏览器关闭错误")
            # 这里不进行恢复，因为已经在主循环中处理了

    return all_novels_data


def main():
    """主函数"""
    logger.info("开始执行喜马拉雅热播榜自动检测更新程序")

    try:
        # 使用配置中的数据存储路径创建基础文件夹结构
        base_dir = create_novel_folder_structure(CONFIG['data_folder_path'])
        
        # 初始化数据库 - 使用程序同级目录
        db_path = os.path.join(script_dir, 'ximalaya_novels.db')
        db_manager = DatabaseManager(db_path)
        logger.info(f"数据库初始化完成: {db_path}")

        # 显示分类选择菜单并获取用户选择
        selected_category = show_category_menu()
        if not selected_category:
            logger.info("用户取消操作")
            return

        # 初始化更新器
        with XimalayaNovelUpdater() as updater:
            # 导航到榜单页面
            if not navigate_to_ranking_page(updater.page):
                logger.error("导航到榜单页面失败")
                return

            logger.info(f"成功导航到榜单页面，开始处理{selected_category['name']}分类")

            # 处理选定分类（收集模式）
            category_novels_data = process_category(updater.page, selected_category, base_dir)

            if category_novels_data:
                logger.info(f"成功爬取{selected_category['name']}分类数据，共 {len(category_novels_data)} 个小说")

                # 统一保存所有数据到数据库
                logger.info("开始统一保存所有数据到数据库...")
                saved_count = 0
                failed_count = 0

                for novel_data in category_novels_data:
                    try:
                        # 保存小说详情到数据库
                        novel_id = db_manager.insert_novel_detail(novel_data, selected_category['name'])

                        if novel_id:
                            # 保存章节详情到数据库
                            category_id = db_manager.get_or_create_category(selected_category['name'])
                            anchor_name = novel_data.get('anchor_name', '')

                            # 插入正序章节
                            chapters = novel_data.get('chapters', [])
                            if chapters:
                                db_manager.insert_chapter_details(chapters, novel_data['novel_title'], 'ASC', category_id, anchor_name=anchor_name)

                            # 插入倒序章节
                            reverse_chapters = novel_data.get('reverse_chapters', [])
                            if reverse_chapters:
                                db_manager.insert_chapter_details(reverse_chapters, novel_data['novel_title'], 'DESC', category_id, anchor_name=anchor_name)

                            logger.info(f"小说《{novel_data['novel_title']}》保存成功，ID: {novel_id}")
                            saved_count += 1
                        else:
                            logger.info(f"小说《{novel_data['novel_title']}》已存在数据库中")

                    except Exception as db_error:
                        logger.error(f"保存小说《{novel_data.get('novel_title', '未知')}》失败: {db_error}")
                        failed_count += 1

                logger.info(f"{selected_category['name']}分类数据保存完成: 成功 {saved_count} 个，失败 {failed_count} 个")

            else:
                logger.warning(f"{selected_category['name']}分类未爬取到任何小说数据")

    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        raise

    logger.info("程序执行完成")


def setup_program_config():
    """设置程序配置"""
    try:
        # 显示程序菜单
        show_program_menu()

        # 自动选择全局变量的浏览器
        print("\n=== 浏览器设置 ===")
        CONFIG['browser_path'] = ''  # 使用默认浏览器（全局变量）
        logger.info("自动使用全局变量的默认浏览器")

        # 数据库将直接保存在程序同级目录
        logger.info(f"数据库将保存在程序同级目录: {CONFIG['data_folder_path']}")

        print(f"\n配置完成!")
        print(f"浏览器: 全局变量默认浏览器")
        print(f"数据库将保存到: {CONFIG['data_folder_path']}\\ximalaya_novels.db")

        input("\n按回车键开始运行程序...")

    except Exception as e:
        logger.error(f"程序配置失败: {e}")
        raise


if __name__ == "__main__":
    try:
        # 设置程序配置
        setup_program_config()

        # 运行主程序
        main()

    except KeyboardInterrupt:
        print("\n程序被用户中断")
        logger.info("程序被用户中断")
    except Exception as e:
        print(f"\n程序运行出错: {e}")
        logger.error(f"程序运行出错: {e}")
        input("按回车键退出...")
    finally:
        print("程序结束")