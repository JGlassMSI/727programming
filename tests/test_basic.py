import pytest

from .support import ProductivitySuiteTest


class TestFoo(ProductivitySuiteTest):
    def test_start_state_0(self):
        assert self.get_value("NoseGear_State") == 0
        assert self.get_value("NoseGear_NextState") == 0

    @pytest.mark.xfail(reason="Need to deactivate the up limit")
    def test_down_request(self):
        assert self.get_value("_NoseGear_UpRequest") == 0
        self.set_value("NoseGear_Request_Up_Ext", True)
        self.run_one_scan()
        assert self.get_value("_NoseGear_UpRequest") == 1
        self.run_one_scan()
        assert self.get_value("NoseGear_State") == 10
        self.run_one_scan()
        # Un-set the up-limit here
        assert self.get_value("NoseGear_MoveUp.InProgress")
