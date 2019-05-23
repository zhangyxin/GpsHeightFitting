from pipe.Setting import Setting


class Argu(object):
    QUASPC = Setting.read('QUASF/PC')
    BILIPC = Setting.read('BILI/PC')
    QUANECE = Setting.read('QUASF/NECESSARY')
    BILINECE = Setting.read('BILI/NECESSARY')

    @staticmethod
    def read(key):
        return Setting.read(key)
