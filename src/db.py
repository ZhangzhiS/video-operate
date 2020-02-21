#!/usr/bin/python3.6
# -*- coding: UTF-8 -*-

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Sliclog(Base):
    __tablename__ = "sliclog"
    id = Column(Integer, primary_key=True)
    execstartctime = Column(String(20))  # 切片程序开始执行时间
    execendtime = Column(String(20))  # 切片程序结束执行时间
    slicenumber = Column(Integer)  # 此次任务总共多少条mp4需要处理
    completenumber = Column(Integer)  # 此次切片任务处理了多少条
    # 目前状态 - 格式：startkey（生成key）、slice（切片中）、complete（任务完成）
    currentstate = Column(String(14))
    # 目前状态 - 格式：startkey（生成key）、slice（切片中）、complete（任务完成）
    msg = Column(String(255))


class Slicdata(Base):
    __tablename__ = "slicdata"
    id = Column(Integer, primary_key=True)
    originalmp4name = Column(String(255))  # 原文件名
    originalmp4path = Column(String(255))  # 原文件路径
    handlemp4path = Column(String(255))  # 切片后文件路径
    opensslkeypath = Column(String(255))  # key的路径及文件名
    filenamekeystring = Column(String(255))  # handlemp4path路径文件夹使用到的加密key
    opensslkeystring = Column(String(255))  # opensslkeypath中文件名使用到的加密key
    # 切片状态 - 参数为： 1 表示已经切片完成，0 表示切片未完成
    status = Column(String(1))
    # 这条记录对应的是那一次切片任务 - 该参数与 sliclog 表中的 id 对应
    tasknumber = Column(Integer)


class Slicerror(Base):
    __tablename__ = "slicerror"
    id = Column(Integer, primary_key=True)
    logtask = Column(Integer)  # 对应sliclog 表中的 id
    datatask = Column(Integer)  # 对应slicdata 表中的 id
    time = Column(String(20))  # 错误发生时间
    errorlog = Column(String(255))  # 具体的错误原因


class DataBaseORM(object):

    def __init__(self, user, password, host, port, db_name, debug=False):
        url_str = "mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        url_str = url_str.format(user=user, password=password, host=host, port=port, db_name=db_name)
        self.engine = create_engine(url_str, echo=debug)

    def check_database_connect(self):
        """检查数据库连接"""
        self.engine.connect()

    def create_sliclog_obj(self, *args):
        """创建sliclog对象"""
        start_time, end_time, task_count, complete_count, status, msg = args
        sliclog_obj = Sliclog(
            execstartctime=start_time,
            execendtime=end_time,
            slicenumber=task_count,
            completenumber=complete_count,
            currentstate=status,
            msg=msg
        )
        return sliclog_obj

    def create_slicdata_obj(self, *args):
        """创建slicdata对象"""
        originalmp4name, originalmp4path, handlemp4path,\
        opensslkeypath, filenamekeystring, opensslkeystring, status, tasknumber = args
        slicdata_obj = Slicdata(
            originalmp4name=originalmp4name,
            originalmp4path=originalmp4path,
            handlemp4path=handlemp4path,
            opensslkeypath=opensslkeypath,
            filenamekeystring=filenamekeystring,
            opensslkeystring=opensslkeystring,
            status=status,
            tasknumber=tasknumber,
        )
        return slicdata_obj

    def create_slicerror_obj(self, *args):
        """创建slicerror对象"""
        logtask, datatask, time, errorlog = args
        slicerror_obj = Slicerror(
            logtask=logtask,
            datatask=datatask,
            time=time,
            errorlog=errorlog,
        )
        return slicerror_obj

    def create_column(self):
        """创建数据表"""
        Base.metadata.create_all(self.engine)

    def create_session(self):
        """创建与数据库的会话"""
        Session_class = sessionmaker(bind=self.engine)
        session = Session_class()
        return session


if __name__ == '__main__':
    # u, pw, h, p, db = ("root", "123..0", "127.0.0.1", "3306", "test")
    # db = DataBaseORM(u, pw, h, p, db, debug=True)
    # db.check_database_connect()
    # db.create_column()
    mat = "{:20}\t{:28}\t{:32}"
    print(mat.format("占4个长度", "占8个长度", "占12长度"))
    # 如果需要居中输出在宽度前面加一个^
    mat = "{:^20}\t{:^28}\t{:^32}"
    print(mat.format("占4个长度", "占8个长度", "占12长度"))

