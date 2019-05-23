# -*- coding:utf-8 -*-


class DataProcessing(object):
    """
    对数据文件进行解析
    """
    def __init__(self, src):
        self.data_src = src

    @property
    def Data(self):
        """
        打开数据文件并进行解析
        :return: list<tuple> labels
        """
        try:
            with open(self.data_src, 'r', encoding='utf-8') as f:
                data = f.readlines()
            head_labels = data[0]
            del data[0]
        except IOError:
            print("Error: 没有找到文件或读取文件失败")
            raise Exception
        else:
            import re
            labels = re.findall(r'\w{1,4}', head_labels)
            del labels[0]
            xy_list = []
            for i in range(0, len(data)):
                # 解析
                single_data_tuple = DataProcessing.__parser_data(data[i])
                if single_data_tuple is None:
                    return None,None
                xy_list.append(single_data_tuple)
            return xy_list, labels

    @staticmethod
    def __parser_data(data_str):
        import re
        pattern = r'\d{1,7}\.\d{1,}'
        assert isinstance(data_str, str)
        data_list = re.findall(pattern, data_str)
        if len(data_list) < 3:
            return None
        for i in range(0, len(data_list)):
            data_list[i] = float(data_list[i])
        return tuple(data_list)

