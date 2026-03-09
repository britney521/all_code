# app.py 最终版：仅保留一级分类（subcategory），删除 category 字段
import os
import re
import subprocess
from typing import Tuple, List

import dateutil
import pandas as pd
from flask import Flask, render_template, jsonify, request, g, current_app
from datetime import datetime, timedelta, date
import sqlite3

app = Flask(__name__)

DB_FILE = 'ximalaya_novels.db'  # 当前目录


def get_conn():
    """获取连接 + 行工厂"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- 业务函数 ----------
def total_play_in_week(note_id: str) -> Tuple[List[int], List[str]]:
    """
    最近 7 天（含今天）在 novel_details 表中，
    同一 novel_title 的 total_plays 之和。
    返回 (data, dates)
    """
    today = date.today()
    conn = get_conn()
    data, dates = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        row = conn.execute(
            "SELECT total_plays FROM novel_details "
            "WHERE note_id=? AND crawl_date=?",
            (note_id, day.strftime("%Y-%m-%d"))
        ).fetchone()
        data.append(parse_number(row["total_plays"]) if row else 0)
        dates.append(day.strftime("%Y-%m-%d"))
    conn.close()
    return data, dates


def play_increment(note_id: int, date: str) -> int:
    """
    指定日期与前一天同一 novel_title 的 total_plays 增量
    :param date: 日期字符串，格式 yyyy-mm-dd
    """
    today = date
    yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    def _get(dt: str) -> int:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT total_plays FROM novel_details "
                "WHERE note_id=? AND crawl_date=?",
                (note_id, dt)
            ).fetchone()
            return parse_number(row["total_plays"]) if row else 0

    return _get(today) - _get(yesterday)


def play_chapter_count(note_id: int, date: str) -> int:
    """
    指定日期与前一天同一 novel_title 的 chapter_count 增量
    :param date: 日期字符串，格式 yyyy-mm-dd
    """
    today = date
    yesterday = (datetime.strptime(date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

    def _get(dt: str) -> int:
        with get_conn() as conn:
            row = conn.execute(
                "SELECT chapter_count FROM novel_details "
                "WHERE note_id=? AND crawl_date=?",
                (note_id, dt)
            ).fetchone()
            return parse_number(row["chapter_count"]) if row else 0

    return _get(today) - _get(yesterday)

def safe_days_since(dt_str: str) -> int:
    """
    把任意日期字符串转成天数差；失败返回 0
    """
    if not dt_str or dt_str.lower() in {'未找到', '', 'nan'}:
        return 0
    try:
        # 先尝试标准解析
        dt = datetime.fromisoformat(dt_str)
    except Exception:
        try:
            # 用 dateutil 解析「2021-03」/「26天前」等
            dt = dateutil.parser.parse(dt_str, default=datetime.now())
        except Exception:
            # 完全看不懂就按今天算
            dt = datetime.now()
    return (datetime.now() - dt).days


def safe_filename(title: str) -> str:
    """
    去掉 Windows/Linux 非法字符，保留中文、数字、字母、空格、-_，
    连续空白压缩成单个空格，首尾空格去掉。
    """
    # 先去掉系统非法字符
    title = re.sub(r'[<>:\"|?*/\\]', '', title)
    # 只保留中文、字母、数字、空格、-_
    title = re.sub(r'[^\u4e00-\u9fffA-Za-z0-9 \-_]+', '', title)

    return title


def parse_number(s: str) -> int:
    """
    把带中文/英文单位字符串统一转成整型
    支持：万、千、百、亿、w、k、b（不区分大小写）
    无法解析或缺失返回 0
    """
    if pd.isna(s) or s is None:
        return 0
    s = str(s).replace(',', '').replace(' ', '').replace('+', '').lower()
    # 缺失值
    if s in {'未找到', '', 'nan', 'null'}:
        return 0

    # 单位映射（万/亿优先，其余依次）
    unit_map = {
        '万': 10_000,
        'w': 10_000,
        '千': 1_000,
        'k': 1_000,
        '百': 100,
        '亿': 100_000_000,
        'b': 100_000_000,
    }

    # 从长到短匹配，防止“万”被“千”截断
    for unit, factor in sorted(unit_map.items(), key=lambda x: -len(x[0])):
        if s.endswith(unit):
            try:
                return int(float(s[:-len(unit)]) * factor)
            except ValueError:
                return 0

    # 没有单位，直接转
    try:
        return int(float(s))
    except ValueError:
        return 0


def read_from_db(cate_name: str,date):
    if not cate_name:
        return []
    conn = get_conn()
    # 1. 取分类id
    cur = conn.execute('SELECT id FROM categories WHERE category_name = ?', (cate_name,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return []
    cate_id = row['id']
    novel_db = f"novel_details"
    sql = f"""
    SELECT note_id,
           rank_position,
           novel_title   AS title,
           anchor_name   AS anchor,
           total_plays   AS plays,
           chapter_count AS episodes,
           comments_count AS reviews,
           fans_count    AS followers,
           created_at
    FROM {novel_db}
    WHERE category_id = ?
    AND crawl_date = ?
    ORDER BY rank_position
    """

    cur = conn.execute(sql, (cate_id, date))
    novels = cur.fetchall()
    if len(novels) == 0:
        return []
    data = []
    for nv in novels:
        note_id = nv['note_id']
        chapter_db = f"chapter_details"
        # 3. 从chapters取第1/10集播放量（正序已排好，行0=第1集，行9=第10集）
        cur.execute(f"""
            SELECT chapter_plays,detail_publish_time as publish_time
            FROM {chapter_db}
            WHERE note_id = ?
            ORDER BY id
            LIMIT 10
        """, (note_id,))
        chap_rows = cur.fetchall()

        first_play = parse_number(chap_rows[0]['chapter_plays']) if len(chap_rows) >= 1 else 0
        tenth_play = parse_number(chap_rows[9]['chapter_plays']) if len(chap_rows) >= 10 else 0
        conversion = round(tenth_play / first_play * 100, 2) if first_play else None

        playsIncrease = play_increment(note_id,date)
        episodesIncrease = play_chapter_count(note_id,date)
        reviews_num = parse_number(nv['reviews'])
        rating = 7 + (reviews_num % 3000) / 1000
        # 不再手动算 days
        publish_time = next(
            (row['publish_time'] for row in chap_rows if row['publish_time']),
            datetime.now().strftime('%Y-%m-%d')  # 10 条全空才用当前日期
        )
        # days = safe_days_since(publish_time)  # 容错后的天数

        data.append({
            'id': note_id,
            'rank': nv['rank_position'],
            'title': nv['title'],
            'anchor': nv['anchor'],
            'plays': nv['plays'],  # 原字符串（带万）
            'playsNumber': parse_number(nv['plays']),
            'playsIncrease': playsIncrease,
            'episodesIncrease': episodesIncrease,
            'episodes': nv['episodes'],
            'totalEpisodes': nv['episodes'],
            'reviews': nv['reviews'],
            'reviewsNumber': reviews_num,
            'firstEpisodePlays': first_play,  # ← 第1集
            'tenthEpisodePlays': tenth_play,  # ← 第10集
            'conversionRate': conversion,
            'followers': nv['followers'],
            'followersNumber': parse_number(nv['followers']),
            'rating': round(rating, 1),
            'publishedDate': publish_time,
            # 'daysSincePublish': days,
            'subcategory': cate_name,
        })

    conn.close()
    return data


@app.route('/')
def index():
    return render_template('index.html')


subcategoryMap = {
    'all': '全部',
    'new': '新品',
    'hot': '热门',
    'city': '都市',
    'free': '免费',
    'fantasy': '玄幻',
    'xianxia': '仙侠',
    'suspense': '悬疑',
    'history': '历史',
    'military': '军事',
    'science': '科幻',
    'game': '游戏',
    'koubei': '口碑',
    'yuepiao': '月票',
    'boys': '男生'
}


# 白名单：只允许这些 exe 被启动
ALLOWED_EXES = {
    "notepad": r"C:\Windows\System32\notepad.exe",
    "calc": r"C:\Windows\System32\calc.exe"
}

@app.route('/run', methods=['POST'])
def run_exe():
    data = request.get_json()
    exe_key = data.get("exe")

    if not exe_key or exe_key not in ALLOWED_EXES:
        return jsonify({"error": "Invalid or forbidden executable"}), 400

    exe_path = ALLOWED_EXES[exe_key]

    if not os.path.isfile(exe_path):
        return jsonify({"error": "Executable not found"}), 404

    try:
        # 启动 exe，不等待完成（后台运行）
        subprocess.Popen([exe_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return jsonify({"status": "started", "exe": exe_key})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rank')
def api_rank():
    today = date.today()
    tp = request.args.get('type', 'new').strip().lower()
    date_str = request.args.get('date',today.strftime("%Y-%m-%d")).strip()
    type = subcategoryMap.get(tp)
    DATA = read_from_db(type,date_str)
    if len(DATA) == 0:
        return jsonify({'error': f'分类 "{subcategoryMap.get(tp)}" 暂无数据', 'data': []}), 404

    return jsonify({'data': DATA})  # 正常 payload


@app.route('/detail')
def detail():
    title = request.args.get('title', '').strip()
    id = request.args.get('id', '').strip()
    # 可选：根据标题去 Excel/数据库里再查一次，或直接把标题传给模板
    return render_template('detail.html', title=title, id=id)


@app.route('/api/detail/daily')
def detail_daily():
    note_id = request.args.get('id')

    plays, dates = total_play_in_week(note_id)
    data = {
        "dates": dates,
        "plays": plays
    }
    return jsonify(data)


if __name__ == '__main__':
    # 启动Flask应用，host='0.0.0.0'允许所有网络接口访问
    app.run(host='0.0.0.0', port=5000, debug=True)
