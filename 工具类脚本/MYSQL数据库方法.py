import pymysql
import sys


# 连接数据库
def connDB():
    conn = pymysql.connect(host="host_IP", user="username", passwd="password", charset='utf8')
    cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return conn, cur


# 更新操作
def db_update(sql):
    """

    :param sql: sql语句
    :return: 无
    """
    # 获取数据库连接
    conn, cur = connDB()
    # 使用cursor() 方法创建一个游标对象 cursor
    try:
        # 执行sql语句
        cur.execute(sql)
        conn.commit()
    except:
        # 如果发生异常，则回滚
        conn.rollback()
    finally:
        # 最终关闭数据库连接
        connClose(conn, cur)


# 数据库插入数据
def db_insert(sql):
    """

    :param sql: sql语句
    :return: 无
    """
    # 获取数据库连接
    conn, cur = connDB()

    try:
        # 执行sql语句
        cur.execute(sql)
        # 提交到数据库执行
        conn.commit()
    except Exception:  # 方法一：捕获所有异常
        # 如果发生异常，则回滚
        print("Error was found", Exception)
        print(sql)
        conn.rollback()
    finally:
        # 最终关闭数据库连接
        connClose(conn, cur)


# 删除操作
def exeDelete(conn, cur, sql):
    """

    :param conn: 连接
    :param cur: 游标
    :param sql: sql语句
    :return: 无
    """
    cur.execute(sql)
    conn.commit()


# 关闭连接，释放资源
def connClose(conn, cur):
    """

    :param conn: 连接
    :param cur: 游标
    :return: 无
    """
    cur.close()
    conn.close()


# 查询
def db_query(sql):
    """

    :param sql: sql语句
    :return: 查询结果
    """
    # 获取数据库连接
    conn, cur = connDB()

    try:
        # 执行sql语句
        cur.execute(sql)
        results = cur.fetchall()
    except:  # 方法三：采用sys模块回溯最后的异常
        # 输出异常信息
        info = sys.exc_info()
        print(info[0], ":", info[1])
        # 如果发生异常，则回滚
        conn.rollback()
    finally:
        # 最终关闭数据库连接
        connClose(conn, cur)
    return results


if '__main__' == __name__:
    pass
