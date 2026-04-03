import pytest
import pyads
from py_src.logger import PLCLogger
from py_src.plc_connector import plc_connector


## Pytest Fixture to handle all mocking
@pytest.fixture
def plc_logging_mocker(mocker):
    mock_conn = mocker.patch("pyads.Connection", autospec=True)
    mock_conn_inst = mock_conn.return_value
    mock_logger = mocker.patch("py_src.plc_connector.PLCLogger", autospec = True)
    mock_logger_inst = mock_logger.return_value

    connect_obj = plc_connector("192.168.1.1", 852)

    return connect_obj, mock_conn_inst, mock_logger_inst

###################
# Tests
##################
def test_initialization(plc_logging_mocker):
    conn_obj, mock_conn, _ = plc_logging_mocker
    assert conn_obj.plc is not None
    mock_conn.open.assert_not_called()  # At this point the connection is not called


def test_connect(plc_logging_mocker):
    conn_obj, mock_conn, _ = plc_logging_mocker
    conn_obj.connect()
    mock_conn.open.assert_called_once()  

def test_is_connected_true(plc_logging_mocker):
    conn_obj, mock_conn, _ = plc_logging_mocker
    mock_conn.read_state.return_value = (pyads.ADSSTATE_RUN, 0)
    assert conn_obj.is_connected is True

def test_is_connected_false_on_ads_error(plc_logging_mocker):
    conn_obj, mock_conn, mock_logger = plc_logging_mocker
    mock_conn.read_state.side_effect = pyads.ADSError(1808)
    assert conn_obj.is_connected is False
    mock_logger.error.assert_called()

def test_connect_exception_handling(plc_logging_mocker):
    conn_obj, mock_conn, mock_logger = plc_logging_mocker
    mock_conn.open.side_effect = Exception("Socket closed by remote")
    conn_obj.connect()
    mock_logger.error.assert_any_call("Failed opening connection to PLC Socket closed by remote")

def test_read_from_plc(plc_logging_mocker):
    Conn_obj, mock_conn, _ = plc_logging_mocker
    mock_conn.read_by_name.return_value = True
    val = Conn_obj.read_variable("MAIN.mbData", pyads.PLCTYPE_BOOL)
    assert val is True
    mock_conn.read_by_name.assert_called_with("MAIN.mbData", pyads.PLCTYPE_BOOL)  