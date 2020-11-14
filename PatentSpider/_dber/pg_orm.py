# table models
# reference samePost.py
from sqlalchemy import Column, Integer, String, Table, Text, Date, Boolean, Time, TIMESTAMP, VARCHAR, func
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
metadata = Base.metadata
'''
two base tables:
PageSource -- store results from spider
Content -- store results from parser
Since we only need the final data and not the page source
I decided to not have a PageSource Table that would take up space.
In the future, if we need more information from the web pages (if we want additional text data)
We can activate this table and save entire HTML pages for future parsing
'''
# modify tables according to the information needed to be retrieved

'''
class PageSource(Base):
    __tablename__ = "uspto_pagesource"  # 這個為表名根據要爬的網站來命名
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    page_source = Column(VARCHAR)
    write_date = Column(Date)

    def __repr__(self):
        return f"USPTO Source(Url: '{self.url}', Write Date: '{self.write_date})'"
'''


class Content(Base):
    __tablename__ = "uspto_content"
    __table_args__ = {"useexisting": False}
    uid = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    claims = Column(String)
    abstract = Column(String)
    description = Column(String)
    collection_time = Column(TIMESTAMP, nullable=True,
                             server_default=func.now())
    write_date = Column(String)

    def __repr__(self):
        return f"USPTO Content(Title: '{self.title}', Write Date: '{self.write_date}')"
