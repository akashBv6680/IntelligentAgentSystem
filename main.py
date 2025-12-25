#!/usr/bin/env python3
"""Main entry point for Intelligent Agent System"""

import json
import argparse
import sys
from orchestrator import AgentOrchestrator, demo_workflow
from logger import logger
import logfire


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="Intelligent Agent System with Logfire Integration"
    )
    parser.add_argument(
        "--topic",
        type=str,
        default="Artificial Intelligence and Machine Learning in Enterprise",
        help="Topic for agent workflow"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo workflow"
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show workflow statistics"
    )
    
    args = parser.parse_args()
    
    try:
        logger.logger.info("=" * 60)
        logger.logger.info("Intelligent Agent System - Starting")
        logger.logger.info("=" * 60)
        
        with logfire.span("Main Application Execution") as main_span:
            main_span.set_attribute("mode", "demo" if args.demo else "workflow")
            
            if args.demo:
                logger.logger.info("Running in DEMO mode")
                result = demo_workflow()
                logger.logger.info("Demo completed successfully")
            else:
                logger.logger.info(f"Running workflow for topic: {args.topic}")
                orchestrator = AgentOrchestrator()
                result = orchestrator.execute_workflow(args.topic)
                
                if args.stats:
                    logger.logger.info("\n" + "=" * 60)
                    logger.logger.info("WORKFLOW STATISTICS")
                    logger.logger.info("=" * 60)
                    stats = orchestrator.get_workflow_statistics()
                    logger.logger.info(f"Statistics: {json.dumps(stats, indent=2)}")
            
            logger.logger.info("\n" + "=" * 60)
            logger.logger.info("Application completed successfully")
            logger.logger.info("=" * 60)
            
            return 0
    
    except Exception as e:
        logger.logger.error(f"Application error: {str(e)}", exc_info=True)
        logger.log_error("MainApp", e, context="main")
        return 1


if __name__ == "__main__":
    sys.exit(main())
