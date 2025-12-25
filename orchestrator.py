"""Agent Orchestrator - Coordinates multi-agent workflow"""

import time
from typing import Dict, List, Any
from agents import ResearchAgent, AnalysisAgent, WriterAgent, ReviewAgent
from logger import logger
import logfire


class AgentOrchestrator:
    """Orchestrates multi-agent workflow with performance tracking"""
    
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.writer_agent = WriterAgent()
        self.review_agent = ReviewAgent()
        
        self.workflow_history = []
        self.performance_metrics = {}
    
    def execute_workflow(self, topic: str) -> Dict[str, Any]:
        """Execute complete multi-agent workflow"""
        workflow_start = time.time()
        workflow_id = f"workflow_{int(time.time())}"
        
        logger.logger.info(f"Starting workflow {workflow_id} for topic: {topic}")
        
        with logfire.span("Complete Agent Workflow") as workflow_span:
            workflow_span.set_attribute("workflow_id", workflow_id)
            workflow_span.set_attribute("topic", topic)
            
            # Stage 1: Research
            logger.logger.info("Stage 1: Research Agent Processing")
            research_start = time.time()
            
            with logfire.span("Research Stage"):
                research_result = self.research_agent.execute(topic)
                research_time = (time.time() - research_start) * 1000
                logger.log_metrics("ResearchAgent", {"execution_time_ms": research_time})
            
            # Stage 2: Analysis
            logger.logger.info("Stage 2: Analysis Agent Processing")
            analysis_start = time.time()
            
            with logfire.span("Analysis Stage"):
                research_findings = research_result.get("findings", "")
                analysis_result = self.analysis_agent.execute(research_findings)
                analysis_time = (time.time() - analysis_start) * 1000
                logger.log_metrics("AnalysisAgent", {"execution_time_ms": analysis_time})
            
            # Stage 3: Writing
            logger.logger.info("Stage 3: Writer Agent Processing")
            writing_start = time.time()
            
            with logfire.span("Writing Stage"):
                analysis_insights = analysis_result.get("insights", "")
                writing_result = self.writer_agent.execute(analysis_insights)
                writing_time = (time.time() - writing_start) * 1000
                logger.log_metrics("WriterAgent", {"execution_time_ms": writing_time})
            
            # Stage 4: Review
            logger.logger.info("Stage 4: Review Agent Processing")
            review_start = time.time()
            
            with logfire.span("Review Stage"):
                report_content = writing_result.get("content", "")
                review_result = self.review_agent.execute(report_content)
                review_time = (time.time() - review_start) * 1000
                logger.log_metrics("ReviewAgent", {"execution_time_ms": review_time})
            
            # Compile results
            total_workflow_time = (time.time() - workflow_start) * 1000
            
            workflow_result = {
                "workflow_id": workflow_id,
                "topic": topic,
                "research_output": research_result,
                "analysis_output": analysis_result,
                "writing_output": writing_result,
                "review_output": review_result,
                "performance": {
                    "research_time_ms": research_time,
                    "analysis_time_ms": analysis_time,
                    "writing_time_ms": writing_time,
                    "review_time_ms": review_time,
                    "total_time_ms": total_workflow_time
                }
            }
            
            self.workflow_history.append(workflow_result)
            logger.log_metrics("Orchestrator", workflow_result["performance"])
            
            logger.logger.info(f"Workflow {workflow_id} completed in {total_workflow_time:.2f}ms")
            
            return workflow_result
    
    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get statistics from completed workflows"""
        if not self.workflow_history:
            return {"message": "No workflows completed yet"}
        
        total_workflows = len(self.workflow_history)
        avg_total_time = sum(
            w["performance"]["total_time_ms"] for w in self.workflow_history
        ) / total_workflows
        
        return {
            "total_workflows": total_workflows,
            "average_workflow_time_ms": avg_total_time,
            "workflows": [w["workflow_id"] for w in self.workflow_history]
        }
    
    def get_agent_performance(self, agent_name: str) -> Dict[str, Any]:
        """Get performance metrics for a specific agent"""
        agent_key = f"{agent_name.lower()}_time_ms"
        
        times = []
        for workflow in self.workflow_history:
            if agent_key in workflow["performance"]:
                times.append(workflow["performance"][agent_key])
        
        if not times:
            return {"message": f"No data for {agent_name}"}
        
        return {
            "agent": agent_name,
            "executions": len(times),
            "average_time_ms": sum(times) / len(times),
            "min_time_ms": min(times),
            "max_time_ms": max(times)
        }


def demo_workflow():
    """Demo workflow execution"""
    orchestrator = AgentOrchestrator()
    
    # Execute workflow
    result = orchestrator.execute_workflow(
        "Artificial Intelligence and Machine Learning in Enterprise"
    )
    
    # Print statistics
    logger.logger.info("\n=== Workflow Statistics ===")
    stats = orchestrator.get_workflow_statistics()
    logger.logger.info(f"Statistics: {stats}")
    
    return result
