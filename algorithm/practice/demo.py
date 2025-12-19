def solution(s: str):
    str_tem = ''
    # 转化成小写
    s = s.lower()
    for i in s:
        if i.isalnum():
            str_tem += i
    return str_tem == str_tem[::-1]




def rm_rf(path):
    """
    实现类似 rm -rf 的功能，递归删除文件和目录
    :param path: 要删除的文件或目录路径
    """
    if path.isFile():  # 如果是文件，直接删除
        path.delete()
    else:  # 如果是目录，递归删除其内容
        # 获取目录下的所有文件和子目录
        files = path.listFiles()
        for file in files:
            # 递归删除每个文件或子目录
            rm_rf(file)
        # 所有内容删除后，删除空目录
        path.delete()


if __name__ == '__main__':
    # 示例使用（假设已创建一个File对象指向要删除的路径）
    # file_obj = File("path/to/delete")
    # rm_rf(file_obj)
    pass