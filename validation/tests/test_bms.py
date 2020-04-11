import psutil
import time
import app.bms as bms

class TestSimBms:

    @classmethod
    def setup(self):
        args = [
            './app/bms.py',
            '-c'
        ]
        self.bms_process = psutil.Popen(args)
        self.bms_process.suspend()
        self.alerts_received = []

    @classmethod
    def teardown(self):
        assert self.bms_process.status() == psutil.STATUS_STOPPED
        self.bms_process.kill()
        self.alerts_received = []

    def sim_sleep(self, ms):
        '''stop test execution and resume bms script for ms milliseconds'''
        seconds = ms / 1000
        self.bms_process.resume()
        time.sleep(seconds)
        self.bms_process.suspend()

    def test_one(self):
        print('in sim test one!')
        self.sim_sleep(4000)
        print('in sim test one after sleep!')

class TestUnitBms:

    @classmethod
    def setup(self):
        pass

    @classmethod
    def teardown(self):
        pass

    def test_one(self):
        print('in unit test one!')