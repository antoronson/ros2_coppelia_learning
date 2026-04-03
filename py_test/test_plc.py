import pytest
import pyads
from py_src.plc_connector import plc_connector
from py_src.logger import PLCLogger

@pytest.fixture
def mock_plc_env():
    with patch('py_src.logger.PLCLogger') as MockLogger, patch('pyads.Connection') as Mockconn:
        mock_conn_inst = Mockconn.return_value
        connector = plc_connector("192.168.2.137.1.1", 851)
        yield connector, mock_conn_inst, MockLogger.return_value

    
def test_initialization(mock_plc_env):
    "Verify init setups pyads object but doesnt open it yet"
    connector, mock_conn, _ = mock_plc_env
    assert connector.plc is not None
    mock_conn.open.assert_not_called()

def test_connection_success(mock_plc_env):
    "verify connect triggers pyads open method"
    connector, mock_conn, _ = mock_plc_env
    connector.connect()
    mock_conn.open.assert_called_once()

def test_is_connected_true(mock_plc_env):
    """Verify is_connected returns True when PLC state is RUN (5)."""
    connector, mock_conn, _ = mock_plc_env
    
    # Mock the return value of read_state (ads_state, device_state)
    # Note: Ensure you fixed the typo ADSSRARE_RUN to ADSSTATE_RUN in your class!
    mock_conn.read_state.return_value = (pyads.ADSSTATE_RUN, 0)
    
    assert connector.is_connected is True

def test_is_connected_false_on_ads_error(mock_plc_env):
    """Verify is_connected handles ADS errors (like timeout) gracefully."""
    connector, mock_conn, mock_logger = mock_plc_env
    
    # Simulate a 'Target Not Found' or 'Timeout' error
    mock_conn.read_state.side_effect = pyads.ADSError(1808)
    
    assert connector.is_connected is False
    # Check if the error was logged
    mock_logger.error.assert_called()

def test_connect_exception_handling(mock_plc_env):
    """Verify that if .open() crashes, the error is logged."""
    connector, mock_conn, mock_logger = mock_plc_env
    
    mock_conn.open.side_effect = Exception("Socket closed by remote host")
    
    connector.connect()
    mock_logger.error.assert_any_call("Failed opening connection to plc socket")