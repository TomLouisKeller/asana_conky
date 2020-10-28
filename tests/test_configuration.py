# Tests for market_env.MarketEnvironment

"""
We run pytest from the root directory of this project, so the file imports work, and we therefore have to fake being in src
"""

# Imports
from asana_conky.configuration import Configuration
#from finpred.market_env import MarketEnvironment, Action


class TestConfiguration:

    # setup
    # @classmethod
    # def setup_class(cls):
    #     cont = IocContainer()
    #     cls.logger = cont.testing_logger()
    #     cls.close_diff_first_row = -0.5

#    @staticmethod
#    def get_stub_data():
#        pass

    def setup_method(self, method):
        self.config = Configuration()
        # self.data = pd.read_csv("tests/resources/market_data.csv")
        # self.logger.debug(f"Testing Market Data: \n{self.data}\n")
        # self.env = MarketEnvironment(self.logger, self.data)
        # self.env.reset()

    # test init

    def test_config_is_not_none(self):
        # action_spec has to be an int and therefore ()
        assert self.config is not None

    def test_tagged_task_path_is_there(self):
        # action_spec has to be an int and therefore ()
        assert len(self.config.get('tagged_tasks')['output_path']) > 0

    # def test_obs_space(self):
    #     # Make sure we have data
    #     assert self.env._observation_spec.shape[0] > 0
    #     # Make sure obs_spec is one dimensional
    #     assert len(self.env._observation_spec.shape) == 1

    # # test reset

    # def test_reset_gets_first_entry(self):
    #     expected = np.array([0.2, 0.4, 0.05, 0.07, 0.0], dtype=np.float32)
    #     state = self.env.reset().observation
    #     assert np.all([state == expected])

    # def test_reset_returns_same_data_after_step(self):
    #     state_before = self.env.reset().observation
    #     state_step = self.env.step(Action.HOLD).observation
    #     state_after = self.env.reset().observation
    #     assert np.all([state_before == state_after])
    #     assert np.any([state_before != state_step])
    #     assert np.any([state_after != state_step])

    # def test_step_returns_same_data_after_reset(self):
    #     _ = self.env.reset()
    #     ts1 = self.env.step(Action.HOLD)
    #     (state_1, reward_1) = (ts1.observation, ts1.reward)
    #     _ = self.env.reset()
    #     ts2 = self.env.step(Action.HOLD)
    #     (state_2, reward_2) = (ts2.observation, ts2.reward)

    #     assert np.all([state_1 == state_2])
    #     assert np.all([reward_1 == reward_2])

    # # test step

    # def test_step_returns_different_data(self):
    #     self.env.reset()
    #     state_1 = self.env.step(Action.HOLD).observation
    #     state_2 = self.env.step(Action.HOLD).observation
    #     assert np.any([state_1 != state_2])

    # def test_step_nopos_hold(self):
    #     self.env.reset()
    #     actual = self.env.step(Action.HOLD).reward
    #     assert actual == 0

    # def test_step_nopos_sell(self):
    #     self.env.reset()
    #     actual = self.env.step(Action.SELL_TO_CLOSE).reward
    #     assert actual == 0

    # def test_step_nopos_buy(self):
    #     # change - spread - slippage - commission
    #     expected = self.close_diff_first_row - 0.01 - 0.0 - 0.0
    #     self.env.reset()
    #     actual = self.env.step(Action.BUY_TO_OPEN).reward
    #     self.logger.debug(f"actual {actual} - expected {expected} - difference {expected-actual}")
    #     assert np.isclose(actual, expected)

    # def test_step_pos_hold(self):
    #     # Cheat and create a position so we don't also test buying
    #     self.env._position_size = 1
    #     # test
    #     actual = self.env.step(Action.HOLD).reward
    #     assert actual == self.close_diff_first_row

    # def test_step_pos_buy(self):
    #     # Cheat and create a position so we don't also test buying
    #     self.env._position_size = 1
    #     reward = self.env.step(Action.BUY_TO_OPEN).reward
    #     assert reward == self.close_diff_first_row

    # def test_step_pos_sell(self):
    #     # change - spread - slippage - commission
    #     expected = - 0.01 - 0.0 - 0.0
    #     # Cheat and create a position so we don't also test buying
    #     self.env._position_size = 1

    #     actual = self.env.step(Action.SELL_TO_CLOSE).reward
    #     assert np.isclose(actual, expected)

    # # test if spread is calculated properly
    # def test_spread_nopos_buy(self):
    #     spread = 0.05
    #     env = MarketEnvironment(self.logger, self.data, bid_ask_spread=spread)
    #     env.reset()
    #     # change - spread - slippage - commission
    #     expected = self.close_diff_first_row - spread - 0.0 - 0.0
    #     actual = env.step(Action.BUY_TO_OPEN).reward
    #     assert np.isclose(actual, expected)

    # def test_spread_pos_sell(self):
    #     spread = 0.05
    #     env = MarketEnvironment(self.logger, self.data, bid_ask_spread=spread)
    #     env.reset()
    #     # Cheat and create a position so we don't also test buying
    #     env._position_size = 1
    #     # change - spread - slippage - commission
    #     expected = - spread - 0.0 - 0.0
    #     actual = env.step(Action.SELL_TO_CLOSE).reward
    #     assert np.isclose(actual, expected)

    # # test if slippage is calculated properly
    # def test_slippage_nopos_buy(self):
    #     slippage = 0.10
    #     env = MarketEnvironment(self.logger, self.data, slippage=slippage)
    #     env.reset()
    #     # change - spread - slippage - commission
    #     expected = self.close_diff_first_row - 0.01 - slippage - 0.0
    #     actual = env.step(Action.BUY_TO_OPEN).reward
    #     assert np.isclose(actual, expected)

    # def test_slippage_pos_sell(self):
    #     slippage = 0.10
    #     env = MarketEnvironment(self.logger, self.data, slippage=slippage)
    #     env.reset()
    #     # Cheat and create a position so we don't also test buying
    #     env._position_size = 1
    #     # change - spread - slippage - commission
    #     expected = - 0.01 - slippage - 0.0
    #     actual = env.step(Action.SELL_TO_CLOSE).reward
    #     assert np.isclose(actual, expected)

    # # test if commission is calculated properly
    # def test_commission_nopos_buy(self):
    #     commission = 0.20
    #     env = MarketEnvironment(self.logger, self.data, commission=commission)
    #     env.reset()
    #     # change - spread - slippage - commission
    #     expected = self.close_diff_first_row - 0.01 - 0.0 - commission
    #     actual = env.step(Action.BUY_TO_OPEN).reward
    #     assert np.isclose(actual, expected)

    # # test if commission is calculated properly
    # def test_commission_pos_sell(self):
    #     commission = 0.20
    #     env = MarketEnvironment(self.logger, self.data, commission=commission)
    #     env.reset()
    #     # Cheat and create a position so we don't also test buying
    #     env._position_size = 1
    #     # change - spread - slippage - commission
    #     expected = - 0.01 - 0.0 - commission
    #     actual = env.step(Action.SELL_TO_CLOSE).reward
    #     assert np.isclose(actual, expected)

    # # test if the pnl is calculated properly over multiple steps
    # def test_pnl_over_3_steps(self):
    #     cost_of_trade = - 0.01 - 0.0 - 0.0
    #     expected = (cost_of_trade - 0.5) + 0.8 + cost_of_trade
    #     self.env.step(Action.BUY_TO_OPEN)
    #     self.env.step(Action.HOLD)
    #     self.env.step(Action.SELL_TO_CLOSE)
    #     assert self.env.pnl == expected

    # # test if trades_n is reported correctly after 2 trades in 3 steps
    # def test_pnl_over_2_trades(self):
    #     expected = 2
    #     self.env.step(Action.BUY_TO_OPEN)
    #     self.env.step(Action.HOLD)
    #     self.env.step(Action.SELL_TO_CLOSE)
    #     assert self.env.trades_n == expected

    # # test trades_n and pnl is being reset
    # def test_reset_pnl_and_trades_n(self):
    #     self.env.step(Action.BUY_TO_OPEN)
    #     self.env.step(Action.HOLD)
    #     self.env.step(Action.SELL_TO_CLOSE)
    #     self.env.reset()

    #     assert self.env.trades_n == 0
    #     assert self.env.pnl == 0
