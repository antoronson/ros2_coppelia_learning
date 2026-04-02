import logging
import pathlib
from datetime import datetime

class PLCLogger:
    def __init__(self):
        # 1. Define paths (Parent directory > logs folder)
        base_path = pathlib.Path(__file__).parent.parent
        log_dir = base_path / "log"
        
        # 2. Create the 'log' folder if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 3. Generate filename based on today's date
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.log"
        
        # 4. Setup the logging configuration
        self.logger = logging.getLogger("TwinCAT_Logger")
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate logs if the class is instantiated multiple times
        if not self.logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(message)s', 
                datefmt='%H:%M:%S'
            )
            
            # File Handler
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Console Handler (Optional: so you see it in your terminal too)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, message):
        """Standard info log"""
        self.logger.info(message)

    def warn(self, message):
        """Warning log"""
        self.logger.warning(message)

    def error(self, message):
        """Error log"""
        self.logger.error(message)

