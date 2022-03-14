import shutil
import time
from folder_lisener import FolderLisenenr


class UnitTest:
    """
    copy file
    """

    def copy_file(self, src, dst):
        shutil.copy(src, dst)

    """
    return run time of program
    """

    def run_time(self, program, *args):
        start = time.time()
        new_file = program(*args)
        end = time.time()
        print(new_file)
        return end - start

    def test_copy(self):
        src_path = "/home/ofek/Documents/CI_Agent/test/bigGoodFile_TeamName.txt"
        dst_path = "/home/ofek/Documents/CI_Agent/Yesodot/Unorganize/bigGoodFile_TeamName.txt"
        print(self.run_time(self.copy_file, src_path, dst_path))

    def test_folder_listener(self):
        lisener_path = "/home/ofek/Documents/CI_Agent/Yesodot/Unorganize/"
        folder_listener = FolderLisenenr(lisener_path)

        print(self.run_time(folder_listener.listen()))


if __name__ == "__main__":

    # test = UnitTest()
    # test.test_folder_listener()
    # test.test_copy()
