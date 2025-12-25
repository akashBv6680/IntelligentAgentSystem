import logfire
import logging
import time
from functools import wraps
from typing import Any, Callable
from config import settings


# Initialize Logfire
if settings.enable_logging:
    logfire.configure(
        service_name="intelligent-agent-system",
        project_name=settings.logfire_project_name,
    )


class AgentLogger:
    """Custom logger for agent operations with Logfire integration"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, settings.log_level))
    
    def log_agent_start(self, agent_name: str, task: str, **kwargs):
        """Log when an agent starts working"""
        with logfire.span(f"Agent Start - {agent_name}") as span:
            span.set_attribute("agent_name", agent_name)
            span.set_attribute("task", task)
            for key, value in kwargs.items():
                span.set_attribute(key, str(value))
            self.logger.info(f"Agent {agent_name} started task: {task}")
    
    def log_agent_end(self, agent_name: str, result: Any, execution_time: float, **kwargs):
        """Log when an agent finishes working"""
        with logfire.span(f"Agent End - {agent_name}") as span:
            span.set_attribute("agent_name", agent_name)
            span.set_attribute("execution_time_ms", execution_time)
            span.set_attribute("result_type", type(result).__name__)
            for key, value in kwargs.items():
                span.set_attribute(key, str(value))
            self.logger.info(f"Agent {agent_name} completed in {execution_time:.2f}ms")
    
    def log_error(self, agent_name: str, error: Exception, context: str = ""):
        """Log agent errors"""
        with logfire.span(f"Agent Error - {agent_name}") as span:
            span.set_attribute("agent_name", agent_name)
            span.set_attribute("error", str(error))
            span.set_attribute("context", context)
            self.logger.error(f"Error in {agent_name}: {error}")
    
    def log_metrics(self, agent_name: str, metrics: dict):
        """Log performance metrics"""
        if settings.enable_metrics:
            with logfire.span(f"Metrics - {agent_name}") as span:
                for key, value in metrics.items():
                    span.set_attribute(key, value)
                self.logger.info(f"Metrics for {agent_name}: {metrics}")


def track_agent_performance(agent_name: str) -> Callable:
    """Decorator to track agent performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = AgentLogger(__name__)
            start_time = time.time()
            
            try:
                logger.log_agent_start(agent_name, func.__name__, args=str(args), kwargs=str(kwargs))
                result = func(*args, **kwargs)
                
                execution_time = (time.time() - start_time) * 1000  # Convert to ms
                logger.log_agent_end(agent_name, result, execution_time)
                
                return result
            except Exception as e:
                logger.log_error(agent_name, e, context=func.__name__)
                raise
        
        return wrapper
    return decorator


# Create module-level logger
logger = AgentLogger(__name__)
