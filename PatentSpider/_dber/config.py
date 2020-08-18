import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from _dber.pg_orm import Base
'''
我們在這裡設定有關數據庫的設定
如果要更改存取的數據庫的話，請在此處更改
spider跟parser所存取的資料會根據這個來定義
'''

import psycopg2
# Address to external database where data should be stored
engine = create_engine(
    'postgresql+psycopg2://postgres@localhost:5432/Capstone')

# local testing database 測試用本端數據庫
#engine = create_engine('sqlite:///test.db', echo=False)

# create tables 開啟pg_orm 中的所有的表
Base.metadata.create_all(engine)

# 程式中需要與數據庫互動用的 session
session = sessionmaker(bind=engine)

# close engine completely
# use: engine.dispose() ***
