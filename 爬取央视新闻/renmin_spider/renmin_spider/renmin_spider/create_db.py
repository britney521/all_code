import sqlalchemy
class News(db.Model):
 '''
 @Author: 邵佳泓
 @msg: 新闻信息表
 '''
 __tablename__ = 'news'
 newsid = db.Column(db.Integer(), primary_key=True, autoincrement=True)
 title = db.Column(db.String(100), nullable=False)
 content = db.Column(db.Text(), nullable=False)
 publish_time = db.Column(
     db.DateTime,
     nullable=False,
 )
 spider_time = db.Column(
     db.DateTime,
     nullable=False,
 )
 author = db.Column(db.String(50), nullable=False)
 articleSource = db.Column(db.String(20), nullable=False)
 article_url = db.Column(db.String(255), nullable=False)

 @classmethod
 def add(cls, news):
  '''
  @Author: 邵佳泓
  @msg: 添加新闻
  @param {*} cls
  @param {*} news
  '''
  db.session.add(news)
  db.session.commit()
