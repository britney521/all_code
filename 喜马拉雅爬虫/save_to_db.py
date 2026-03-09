import sqlite3
from datetime import date
from typing import Dict, List, Any
from loguru import logger

logger.add(
    "logs/喜马拉雅_{time:YYYY-MM-DD}.log",
    rotation="00:00",          # 每天新文件
    retention="7 days",        # 保留 7 天
    encoding="utf-8",
    level="DEBUG"
)
DB_PATH = 'ximalaya_novels.db'      # 换成你的真实路径

class DbSaver:
    def __init__(self, db: str = DB_PATH):
        self.db = db

    def init_database(self):
        """初始化数据库表结构 - 按日期保存模式"""
        with self.get_conn() as conn:
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
                    score INTEGER,
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (note_id) REFERENCES novel_master (note_id)
                )
            ''')

            conn.commit()
            logger.info(f"数据库初始化完成")
    # ------- 公共工具 -------
    def get_conn(self):
        return sqlite3.connect(self.db)

    def get_or_create_category(self, category_name: str) -> int:
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO categories(category_name) VALUES(?)"
                " ON CONFLICT(category_name) DO UPDATE SET category_name=category_name"
                " RETURNING id",
                (category_name,)
            )
            return cur.fetchone()[0]

    def get_or_create_master(self, novel_title: str, anchor_name: str) -> int:
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                'INSERT OR IGNORE INTO novel_master(novel_title, anchor_name, first_seen_date) VALUES(?,?,?)',
                (novel_title, anchor_name, date.today()))
            cur.execute(
                'SELECT note_id FROM novel_master WHERE novel_title=? AND anchor_name=?',
                (novel_title, anchor_name))
            return cur.fetchone()[0]

    # ---------------- 业务 ----------------
    def save_album(self, *,
                   category_id: int,
                   rank_position: int,
                   album_data: Dict[str, Any],
                   anchor_data: Dict[str, Any],
                   crawl_date: date = None) -> int:
        """
        写入/更新 novel_details + 返回 note_id
        同一(note_id, crawl_date, category_id) 存在则更新，否则插入
        """
        crawl_date = crawl_date or date.today()
        note_id = self.get_or_create_master(album_data['albumTitle'], album_data['anchorName'])

        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO novel_details
                   (note_id, novel_title, category_id, rank_position,
                    total_plays, anchor_name, chapter_count, comments_count,score,
                    fans_count, novel_url, crawl_date)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(note_id, crawl_date, category_id) DO UPDATE SET
                      rank_position=excluded.rank_position,
                      total_plays=excluded.total_plays,
                      chapter_count=excluded.chapter_count,
                      comments_count=excluded.comments_count,
                      score=excluded.score,
                      fans_count=excluded.fans_count""",
                (note_id,
                 album_data['albumTitle'],
                 category_id,
                 rank_position,
                 str(album_data.get('playCount', 0)),
                 album_data['anchorName'],
                 album_data.get('trackCount', 0),
                 str(album_data.get('commentCount', 0)),
                 album_data.get('score', 0),
                 str(anchor_data.get('fansCount', 0)),
                 f'https://www.ximalaya.com/album/{album_data["albumId"]}',
                 crawl_date))
            conn.commit()
        return note_id

    def save_tracks(self, *,
                    note_id: int,
                    albumTitle: str,
                    nickName: str,
                    category_id: int,
                    tracks: List[Dict[str, Any]],
                    crawl_date: date = None,
                    chapter_order_type: str = 'ASC'):
        """
        章节：同一(note_id, crawl_date) 先删后插，保证幂等
        """
        crawl_date = crawl_date or date.today()
        with self.get_conn() as conn:
            cur = conn.cursor()
            # 先删
            cur.execute(
                'DELETE FROM chapter_details WHERE note_id=? AND crawl_date=?',
                (note_id, crawl_date))
            # 再插
            rows = [(
                note_id,
                albumTitle,
                nickName,
                category_id,
                tr['title'],
                str(tr.get('playCount', 0)),
                tr.get('createDateFormat', ''),
                f'https://www.ximalaya.com/sound/{tr["trackId"]}',
                crawl_date,
                chapter_order_type) for tr in tracks]
            cur.executemany(
                """INSERT INTO chapter_details
                   (note_id, novel_title, anchor_name, category_id,
                    chapter_title, chapter_plays, publish_time,
                    chapter_url, crawl_date, chapter_order_type)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""", rows)
            conn.commit()