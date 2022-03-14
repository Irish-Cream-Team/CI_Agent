from ..folder_lisener import FolderLisenenr
import time
import shutil

class test:
    # def __init__(self):
        # test_path = '/home/ofek/Documents/CI_Agent/Yesodot/Unorganize'
        # self.folder_lisener = FolderLisenenr(test_path)


    # def test_folder_lisener(self):
        # print(self.folder_lisener.listen())

    '''
    Get time of function execution
    '''
    def get_time(self, func,*args):
        start = time.time()
        func(*args)
        end = time.time()
        return end - start

    '''
    copy file from src to dst
    '''
    def copy_file(self, src, dst):
        shutil.copyfile(src, dst)

    def test_copy_file(self):
        src = '/home/ofek/Documents/CI_Agent/test/test_TeamName'
        dst = '/home/ofek/Documents/CI_Agent/Yesodot/Unorganize/test_TeamName'
        self.copy_file(src, dst)



if __name__ == '__main__':
    test_obj = test()
    # test_obj.test_folder_lisener()
    # print(test_obj.get_time(test_obj.test_folder_lisener))
    test_obj.test_copy_file()
    print(test_obj.get_time(test_obj.test_copy_file))