"""
Configuration management module for Playwright Pytest Framework.

This module provides a Config class for managing environment variables,
configuration settings, and other application-level configurations.
"""

import os
from typing import Optional, Any, Dict
from pathlib import Path


class Config:
    """
    Configuration class for managing environment variables and settings.
    
    This class provides a centralized way to manage all configuration settings
    used throughout the test framework, including URLs, timeouts, browser
    settings, and other environment-specific configurations.
    """
    
    # ============ BASE PATHS ============
    BASE_DIR: Path = Path(__file__).parent.parent
    TESTS_DIR: Path = BASE_DIR / "tests"
    REPORTS_DIR: Path = BASE_DIR / "reports"
    LOGS_DIR: Path = BASE_DIR / "logs"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # ============ ENVIRONMENT SETTINGS ============
    ENV: str = os.getenv("ENV", "dev").lower()
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # ============ BASE URLS ============
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:3000")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000/api")
    
    # ============ BROWSER CONFIGURATION ============
    BROWSER_TYPE: str = os.getenv("BROWSER_TYPE", "chromium").lower()
    HEADLESS: bool = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")
    SLOW_MO: int = int(os.getenv("SLOW_MO", "0"))
    VIEWPORT_WIDTH: int = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT: int = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    DISABLE_ANIMATIONS: bool = os.getenv("DISABLE_ANIMATIONS", "True").lower() in ("true", "1", "yes")
    
    # ============ TIMEOUT SETTINGS (in milliseconds) ============
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT: int = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    WAIT_FOR_TIMEOUT: int = int(os.getenv("WAIT_FOR_TIMEOUT", "5000"))
    NETWORK_IDLE_TIMEOUT: int = int(os.getenv("NETWORK_IDLE_TIMEOUT", "10000"))
    
    # ============ RETRY CONFIGURATION ============
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "1000"))  # milliseconds
    
    # ============ PARALLEL EXECUTION ============
    PARALLEL_WORKERS: int = int(os.getenv("PARALLEL_WORKERS", "4"))
    
    # ============ SCREENSHOT & VIDEO SETTINGS ============
    SCREENSHOT_ON_FAILURE: bool = os.getenv("SCREENSHOT_ON_FAILURE", "True").lower() in ("true", "1", "yes")
    RECORD_VIDEO: bool = os.getenv("RECORD_VIDEO", "False").lower() in ("true", "1", "yes")
    VIDEO_DIR: Path = REPORTS_DIR / "videos"
    SCREENSHOT_DIR: Path = REPORTS_DIR / "screenshots"
    
    # ============ TEST REPORTING ============
    GENERATE_HTML_REPORT: bool = os.getenv("GENERATE_HTML_REPORT", "True").lower() in ("true", "1", "yes")
    REPORT_FORMAT: str = os.getenv("REPORT_FORMAT", "html").lower()
    
    # ============ AUTHENTICATION ============
    USERNAME: Optional[str] = os.getenv("USERNAME", None)
    PASSWORD: Optional[str] = os.getenv("PASSWORD", None)
    API_KEY: Optional[str] = os.getenv("API_KEY", None)
    AUTH_TOKEN: Optional[str] = os.getenv("AUTH_TOKEN", None)
    
    # ============ DATABASE CONFIGURATION ============
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "test_db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: Optional[str] = os.getenv("DB_PASSWORD", None)
    
    # ============ NOTIFICATION SETTINGS ============
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("SLACK_WEBHOOK_URL", None)
    EMAIL_RECIPIENTS: Optional[str] = os.getenv("EMAIL_RECIPIENTS", None)
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key name
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return getattr(cls, key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key name
            value: Value to set
        """
        setattr(cls, key, value)
    
    @classmethod
    def get_all_as_dict(cls) -> Dict[str, Any]:
        """
        Get all configuration settings as a dictionary.
        
        Returns:
            Dictionary of all class attributes (excluding private/magic methods)
        """
        return {
            key: value for key, value in cls.__dict__.items()
            if not key.startswith("_") and not callable(value)
        }
    
    @classmethod
    def is_dev(cls) -> bool:
        """Check if running in development environment."""
        return cls.ENV == "dev"
    
    @classmethod
    def is_test(cls) -> bool:
        """Check if running in test environment."""
        return cls.ENV == "test"
    
    @classmethod
    def is_prod(cls) -> bool:
        """Check if running in production environment."""
        return cls.ENV == "prod"
    
    @classmethod
    def is_ci(cls) -> bool:
        """Check if running in CI/CD environment."""
        return os.getenv("CI", "False").lower() in ("true", "1", "yes")
    
    @classmethod
    def ensure_directories(cls) -> None:
        """Create all required directories if they don't exist."""
        directories = [
            cls.TESTS_DIR,
            cls.REPORTS_DIR,
            cls.LOGS_DIR,
            cls.DATA_DIR,
            cls.VIDEO_DIR,
            cls.SCREENSHOT_DIR,
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """
        Get browser launch options.
        
        Returns:
            Dictionary of browser launch options
        """
        return {
            "headless": cls.HEADLESS,
            "slow_mo": cls.SLOW_MO,
            "args": [
                f"--disable-animations" if cls.DISABLE_ANIMATIONS else "",
            ]
        }
    
    @classmethod
    def get_context_options(cls) -> Dict[str, Any]:
        """
        Get browser context options.
        
        Returns:
            Dictionary of context options
        """
        return {
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT,
            },
            "record_video_dir": str(cls.VIDEO_DIR) if cls.RECORD_VIDEO else None,
        }
    
    @classmethod
    def print_config(cls) -> None:
        """Print all configuration settings for debugging purposes."""
        print("\n" + "=" * 60)
        print("CONFIGURATION SETTINGS")
        print("=" * 60)
        
        config_dict = cls.get_all_as_dict()
        for key, value in sorted(config_dict.items()):
            # Mask sensitive information
            if any(sensitive in key.upper() for sensitive in ["PASSWORD", "TOKEN", "KEY", "SECRET"]):
                value = "***MASKED***"
            print(f"{key}: {value}")
        
        print("=" * 60 + "\n")
