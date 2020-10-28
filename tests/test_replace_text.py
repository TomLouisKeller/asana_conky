from asana_conky.configuration import Configuration
from asana_conky.helper import replace_text


class TestReplaceText:

    # setup
    @classmethod
    def setup_class(cls):
        cls.config = Configuration()

    # def setup_method(self, method):
    #     self.data = pd.read_csv("tests/resources/market_data.csv")
    #     self.logger.debug(f"Testing Market Data: \n{self.data}\n")
    #     self.env = MarketEnvironment(self.logger, self.data)
    #     self.env.reset()

    # test init

    def test_replace(self):
        tagged_tasks = self.config.get('tagged_tasks')
        line_string = "this is the new text"
        replace_text(tagged_tasks['output_path'], tagged_tasks['start_tag'], tagged_tasks['end_tag'], line_string)
