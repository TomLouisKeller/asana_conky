# Imports
from asana_conky.configuration import Configuration


class TestConfiguration:

    # @classmethod
    # def setup_class(cls):
    #    pass

    def setup_method(self, method):
        self.config = Configuration()

    # test init

    def test_config_is_not_none(self):
        # action_spec has to be an int and therefore ()
        assert self.config is not None

    def test_tagged_task_path_is_there(self):
        # action_spec has to be an int and therefore ()
        assert len(self.config.get('tagged_tasks')['output_path']) > 0
