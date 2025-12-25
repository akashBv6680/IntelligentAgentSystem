"""Core Agent Definitions for Intelligent Agent System"""

from typing import Any, Dict
from abc import ABC, abstractmethod
from langchain_openai import ChatOpenAI
from config import settings
from logger import track_agent_performance, logger


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm = ChatOpenAI(
            model=settings.model_name,
            temperature=settings.temperature,
            max_tokens=settings.max_tokens,
            api_key=settings.openai_api_key
        )
    
    @abstractmethod
    def execute(self, input_data: str) -> Dict[str, Any]:
        """Execute agent task"""
        pass
    
    @abstractmethod
    def validate_output(self, output: Any) -> bool:
        """Validate agent output"""
        pass


class ResearchAgent(BaseAgent):
    """Agent responsible for research and information gathering"""
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Gathers and researches information on given topics"
        )
        self.research_history = []
    
    @track_agent_performance("ResearchAgent")
    def execute(self, input_data: str) -> Dict[str, Any]:
        """Execute research task"""
        logger.logger.info(f"Starting research on: {input_data}")
        
        # Simulate research processing
        research_prompt = f"""Research and provide comprehensive information about: {input_data}
        Include:
        - Key findings
        - Relevant data points
        - Sources and references"""
        
        response = self.llm.invoke(research_prompt)
        research_result = {
            "topic": input_data,
            "findings": response.content,
            "research_type": "comprehensive"
        }
        
        self.research_history.append(research_result)
        return research_result
    
    def validate_output(self, output: Any) -> bool:
        return isinstance(output, dict) and "findings" in output


class AnalysisAgent(BaseAgent):
    """Agent responsible for analyzing information"""
    
    def __init__(self):
        super().__init__(
            name="AnalysisAgent",
            description="Analyzes gathered information and identifies patterns"
        )
        self.analysis_history = []
    
    @track_agent_performance("AnalysisAgent")
    def execute(self, input_data: str) -> Dict[str, Any]:
        """Execute analysis task"""
        logger.logger.info(f"Analyzing data: {input_data[:100]}...")
        
        analysis_prompt = f"""Analyze the following information and provide:
        {input_data}
        
        Include:
        - Key insights
        - Pattern identification
        - Recommendations
        - Risk assessment"""
        
        response = self.llm.invoke(analysis_prompt)
        analysis_result = {
            "input_summary": input_data[:200],
            "insights": response.content,
            "confidence_score": 0.85
        }
        
        self.analysis_history.append(analysis_result)
        return analysis_result
    
    def validate_output(self, output: Any) -> bool:
        return isinstance(output, dict) and "insights" in output


class WriterAgent(BaseAgent):
    """Agent responsible for creating written content"""
    
    def __init__(self):
        super().__init__(
            name="WriterAgent",
            description="Creates well-structured written reports and documents"
        )
        self.written_content = []
    
    @track_agent_performance("WriterAgent")
    def execute(self, input_data: str) -> Dict[str, Any]:
        """Execute writing task"""
        logger.logger.info(f"Creating report for: {input_data[:100]}...")
        
        writing_prompt = f"""Create a professional report based on:
        {input_data}
        
        Format:
        - Executive Summary
        - Detailed Findings
        - Conclusions
        - Next Steps"""
        
        response = self.llm.invoke(writing_prompt)
        report = {
            "report_type": "professional",
            "content": response.content,
            "word_count": len(response.content.split()),
            "status": "completed"
        }
        
        self.written_content.append(report)
        return report
    
    def validate_output(self, output: Any) -> bool:
        return isinstance(output, dict) and "content" in output


class ReviewAgent(BaseAgent):
    """Agent responsible for reviewing and quality checking"""
    
    def __init__(self):
        super().__init__(
            name="ReviewAgent",
            description="Reviews and verifies quality of outputs"
        )
        self.review_history = []
    
    @track_agent_performance("ReviewAgent")
    def execute(self, input_data: str) -> Dict[str, Any]:
        """Execute review task"""
        logger.logger.info(f"Reviewing content quality")
        
        review_prompt = f"""Review the following content and provide quality assessment:
        {input_data}
        
        Evaluate:
        - Accuracy
        - Clarity
        - Completeness
        - Professionalism
        
        Provide improvement suggestions."""
        
        response = self.llm.invoke(review_prompt)
        review = {
            "status": "reviewed",
            "quality_assessment": response.content,
            "quality_score": 0.92,
            "approved": True
        }
        
        self.review_history.append(review)
        return review
    
    def validate_output(self, output: Any) -> bool:
        return isinstance(output, dict) and "quality_assessment" in output
