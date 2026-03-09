from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Yqj_Yqj_Yqj@sjh.mcl913.top:3306/spiders'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'spiders'

db = SQLAlchemy(app)

#新闻表


class News(db.Model):
    __tablename__ = "news_info"
    newsid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    publish_time = db.Column(db.DateTime, nullable=False,)
    spider_time = db.Column(db.DateTime, nullable=False,)
    author = db.Column(db.String(50), nullable=False)
    articleSource = db.Column(db.String(20), nullable=False)
    article_url = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(100), nullable=False)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
