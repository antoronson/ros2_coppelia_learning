import pytest
from pytest_mock.plugin import _mocker
from python_ws.pyads_plc_sim.py_src.plc_sim_bridge import PlcSimBridge
from python_ws.pyads_plc_sim.py_src.plc_connector import plc_connector
from python_ws.pyads_plc_sim.py_src.logger import PLCLogger
from python_ws.pyads_plc_sim.py_src.plc_signals import PLC_Signals


@pytest.fixture
def plc_connector_mocker(mocker):
    mock_plc_sim_bridge = mocker.patch("py_src.plc_sim_bridge.PlcSimBridge", autospec=True)
    mock_plc_sim_bridge_inst = mock_plc_sim_bridge.return_value
    
    mock_logger_plc_connect = mocker.patch("py_src.plc_connector.PLCLogger", autospec=True)
    mock_logger_plc_connect_inst = mock_logger_plc_connect.return_value

    mock_logger_plc_sim_bridge = mocker.patch("py_src.plc_sim_bridge.PLCLogger", autospec=True)
    mock_logger_plc_sim_bridge_inst = mock_logger_plc_sim_bridge.return_value

    mock_plc_signals = mocker.patch("py_src.plc_signals.PLC_Signals", autospec=True)
    mock_plc_signals_inst = mock_plc_signals.return_value

    mock_plc_connect = mocker.patch("py_src.plc_sim_bridge.plc_connector", autspec=True)
    mock_plc_connect_inst = mock_plc_connect.return_value


    simbridge_obj = PlcSimBridge("192.168.1.1.1.1", 851)
    return simbridge_obj, \
                mock_plc_sim_bridge_inst, \
                mock_plc_connect_inst, \
                mock_plc_signals_inst, \
                mock_logger_plc_connect_inst, \
                mock_logger_plc_sim_bridge_inst


######################
# Test
######################
def test_initialization(plc_connector_mocker):
    simbridge_obj, mock_simbridge, mock_conn, mock_signals, mock_log_conn, mock_log_simbridge = plc_connector_mocker
    assert simbridge_obj.plc is not None
    assert simbridge_obj.signals is not None
    assert simbridge_obj.logger is not None
    mock_conn.connect.assert_called_once()
    #assert mock_conn.is_connected is True


def bridge_read_value(plc_connector_mocker):
    simbridge_obj, mock_simbridge, mock_conn, mock_signals, mock_log_conn, mock_log_simbridge = plc_connector_mocker
   # mock_plc_signals_inst = mock_plc_signals.return_value

    simbridge_obj = PlcSimBridge("1.1.1.1.1.1", 852)

    simbridge_obj.read_from_plc()
    assert simbridge_obj.read_from_plc.assert_called_once()