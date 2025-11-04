#!/usr/bin/env python3
"""Test script for LLMClient."""

import os
import asyncio
import json
from app.clients.llm_client import LLMClient
from dotenv import load_dotenv

load_dotenv()

async def test_llm_client():
    """Test LLMClient with sample vacancy text."""
    
    # Create output directory
    output_dir = "llm_test_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY environment variable not set")
        print("Set it with: export GROQ_API_KEY='your_api_key_here'")
        return
    
    # Initialize client
    client = LLMClient(api_key=api_key)
    
    # Sample vacancy text
    sample_text = "JetBrains Internship Application Internships Register Sign in Software Engineering Intern - AI Agents (Kotlin) Description Overview We're an AI Engineering team focused on applied AI - we focus on integrating AI features into business and products. We handle the full agent development lifecycle: design, implementation, tool development, testing, and evaluation. Since ready-made datasets and metrics don't always exist for our use cases, we often create those as well. We develop agents using the Koog framework (built right here at JetBrains) and work closely with the Koog team, providing feedback and occasionally contributing general features back to the framework when they're broadly useful beyond our specific agents. Currently, we're preparing our SWE agent for open source release, including writing blog articles about the development process and lessons learned. What You'll Do Join our team working on cutting-edge AI agent development. Depending on when you start and the project needs, you might work on: Implementing new agent capabilities and tools Designing and running agent evaluation experiments Contributing to the Koog framework features Sharing your work in blog articles - a chance to build your CV and online presence by showcasing what you ve done You'll get hands-on experience with both the research side (studying problems, running experiments) and engineering side (implementing solutions, writing robust code). This is a 6-month internship where you'll gain deep experience in both AI agent development and production-quality software engineering. Requirements Strong software engineering fundamentals - you know your OOP, design patterns, and why SOLID principles matter Proficiency in at least one JVM language (we'd love Kotlin, but Java works great too) Demonstrated interest in AI agents - whether through personal projects, coursework, research, or just building cool stuff on weekends Understanding of LLM fundamentals - how transformers work, what tokenization does, plus modern capabilities like tool calling, structured outputs, and multimodal processing Basic ML/statistics knowledge - comfortable with datasets, evaluation metrics, and core statistical concepts Admission Internship projects 2025-2026 Contact details internship@jetbrains.com Preferred internship location Netherlands Technologies Kotlin Area Development Machine Learning Internship timing preferences Flexible start Full-time preferable Part-time acceptable Candidate graduation status Final-year students preferred Copyright 2000 2025 JetBrains s.r.o."
    
    print("Testing LLM client...")
    print(f"Sample text length: {len(sample_text)} characters")
    
    try:
        # Generate timestamp for filenames
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print("Testing LLM client with stats...")
        
        # Extract info using LLM with stats
        result_with_stats = await client.extract_vacancy_info(sample_text, include_stats=True)
        result = result_with_stats["response"]
        stats = result_with_stats["stats"]
        
        print("\nLLM extraction successful!")
        print("\n--- Extracted Information ---")
        print(f"Company: {result.company_name}")
        print(f"Role: {result.role_title}")
        print(f"Grade: {result.job_grade}")
        print(f"Salary: {result.expected_salary}")
        print(f"Contact: {result.contact_person}")
        print(f"Requirements: {result.requirements}")
        
        print(f"\n--- API Stats ---")
        print(f"TOKENS: {stats['usage']['total_tokens']} total")
        print(f"  ├── Prompt: {stats['usage']['prompt_tokens']}")
        print(f"  └── Completion: {stats['usage']['completion_tokens']}")
        print(f"Execution time: {stats['timing']['execution_time_seconds']} seconds")
        print(f"Model: {stats['model']}")
        print(f"Request ID: {stats['id']}")
        
        # Save everything in one JSON file
        test_data = {
            "metadata": {
                "timestamp": timestamp,
                "success": True,
                "test_type": "llm_extraction"
            },
            "input": {
                "text_content": sample_text,
                "text_length": len(sample_text),
                "model_config": {
                    "model": client.model,
                    "temperature": client.temperature,
                    "max_tokens": client.max_tokens
                }
            },
            "output": {
                "extraction_result": result.model_dump()
            },
            "statistics": {
                "tokens": {
                    "prompt_tokens": stats['usage']['prompt_tokens'],
                    "completion_tokens": stats['usage']['completion_tokens'], 
                    "total_tokens": stats['usage']['total_tokens']
                },
                "timing": {
                    "execution_time_seconds": stats['timing']['execution_time_seconds'],
                    "start_time": stats['timing']['start_time'],
                    "end_time": stats['timing']['end_time']
                },
                "api_info": {
                    "model": stats['model'],
                    "created": stats['created'],
                    "id": stats['id'],
                    "system_fingerprint": stats['system_fingerprint']
                },
                "full_api_stats": stats
            }
        }
        
        output_file = f"{output_dir}/test_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"\nComplete test data saved to: {output_file}")
        
    except Exception as e:
        print(f"\n❌ Error occurred: {e}")
        import traceback
        traceback.print_exc()
        
        # Save error info in same format
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        test_data = {
            "metadata": {
                "timestamp": timestamp,
                "success": False,
                "test_type": "llm_extraction"
            },
            "input": {
                "text_content": sample_text,
                "text_length": len(sample_text),
                "model_config": {
                    "model": client.model,
                    "temperature": client.temperature,
                    "max_tokens": client.max_tokens
                }
            },
            "error": {
                "message": str(e),
                "traceback": traceback.format_exc()
            }
        }
        
        output_file = f"{output_dir}/test_{timestamp}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        print(f"Error test data saved to: {output_file}")


if __name__ == "__main__":
    asyncio.run(test_llm_client())