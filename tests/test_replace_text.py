from asana_conky.configuration import Configuration
from asana_conky.helper import replace_text_in_file


class TestReplaceText:

    # setup
    @classmethod
    def setup_class(cls):
        cls.config = Configuration()

    # helper
    @staticmethod
    def read_file(file_path: str):
        with open(file_path, 'r') as file:
            filedata = file.read()
        return filedata

    # test replace_text_in_file
    def test_replace_text_in_file(self):
        path = 'tests/resources/replace_in_here.txt'
        start_tag = '${start_tag}'
        end_tag = '${end_tag}'

        # Reset file
        replace_text_in_file(path, start_tag, end_tag, "")
        one = self.read_file(path)
        replace_text_in_file(path, start_tag, end_tag, "this is the new text")
        two = self.read_file(path)

        assert one != two
