"""
Enhanced Core Validation using Custom AI Models
Replaces the basic validation with advanced AI-powered analysis
"""

from typing import Dict, Any, List
import os
import sys

# Add the project root to Python path to import our custom AI
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.ai.orchestrator import CustomAIOrchestrator, AIConfig

# Initialize the custom AI system
AI_CONFIG = AIConfig(
    model_dir=os.path.join(project_root, "models"),
    training_data_dir=os.path.join(project_root, "training_data"),
    knowledge_base_dir=os.path.join(project_root, "references"),
    cache_dir=os.path.join(project_root, "cache"),
    enable_custom_embeddings=True,
    enable_compliance_ml=True,
    enable_document_generation=True,
    enable_advanced_rag=True
)

# Global AI orchestrator instance
_ai_orchestrator = None

def get_ai_orchestrator() -> CustomAIOrchestrator:
    """Get or create the AI orchestrator instance"""
    global _ai_orchestrator
    if _ai_orchestrator is None:
        _ai_orchestrator = CustomAIOrchestrator(AI_CONFIG)
        # Train models if needed
        _ai_orchestrator.train_models_if_needed()
    return _ai_orchestrator

def analyze_bundle_advanced(proc_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Advanced document bundle analysis using custom AI models
    This replaces the basic analyze_bundle function with AI-powered analysis
    """
    orchestrator = get_ai_orchestrator()
    
    # Convert proc_info to file_bytes format for AI analysis
    file_bytes = {}
    for doc_name, doc_data in proc_info.get('documents', {}).items():
        if 'text' in doc_data and doc_data['text']:
            # Convert text back to bytes for AI processing
            # In a real implementation, you'd store the original bytes
            file_bytes[doc_name] = doc_data['text'].encode('utf-8')
    
    if not file_bytes:
        # Fallback to basic analysis if no valid documents
        return fallback_basic_analysis(proc_info)
    
    try:
        # Use the AI orchestrator for comprehensive analysis
        ai_results = orchestrator.analyze_document_bundle(file_bytes)
        
        # Convert AI results to the expected format
        return convert_ai_results_to_legacy_format(ai_results, proc_info)
        
    except Exception as e:
        print(f"AI analysis failed, falling back to basic analysis: {e}")
        return fallback_basic_analysis(proc_info)

def convert_ai_results_to_legacy_format(ai_results: Dict[str, Any], proc_info: Dict[str, Any]) -> Dict[str, Any]:
    """Convert AI analysis results to the legacy format expected by the UI"""
    
    # Extract key information from AI results
    executive_summary = ai_results.get('executive_summary', {})
    compliance_analysis = ai_results.get('compliance_analysis', {})
    missing_docs_info = ai_results.get('missing_documents', {})
    
    # Build issues list from compliance analysis
    issues_found = []
    
    for doc_name, compliance_data in compliance_analysis.items():
        for rule_name, rule_data in compliance_data.get('rule_scores', {}).items():
            if rule_data['score'] < 0.8:  # Flag issues with low scores
                
                # Determine severity based on score and weight
                if rule_data['score'] < 0.3 and rule_data['weight'] > 15:
                    severity = 'High'
                elif rule_data['score'] < 0.6 and rule_data['weight'] > 10:
                    severity = 'Medium'
                else:
                    severity = 'Low'
                
                # Get suggestions from AI
                suggestions = compliance_data.get('recommendations', [])
                suggestion = suggestions[0] if suggestions else f"Address {rule_name} compliance issue"
                
                # Get citations from RAG insights
                citations = []
                rag_insights = ai_results.get('rag_insights', {}).get('insights', [])
                for insight in rag_insights:
                    if insight.get('document') == doc_name and insight.get('issue') == rule_name:
                        citations.extend(insight.get('relevant_regulations', []))
                
                issue = {
                    'document': doc_name,
                    'issue': rule_name.replace('_', ' ').title(),
                    'severity': severity,
                    'suggestion': suggestion,
                    'citations': citations[:3],  # Limit to top 3 citations
                    'rationale': f"Compliance score: {rule_data['score']:.2f}, Weight: {rule_data['weight']}"
                }
                issues_found.append(issue)
    
    # Add insights from cross-document analysis
    cross_doc_issues = ai_results.get('cross_document_analysis', {}).get('consistency_issues', [])
    for cross_issue in cross_doc_issues:
        issue = {
            'document': 'Cross-Document',
            'issue': cross_issue.get('description', 'Consistency Issue'),
            'severity': cross_issue.get('severity', 'Medium'),
            'suggestion': 'Review and align information across all documents',
            'citations': ['Cross-document consistency check'],
            'rationale': cross_issue.get('type', 'consistency_check')
        }
        issues_found.append(issue)
    
    # Calculate compliance score
    compliance_score = executive_summary.get('overall_compliance_score', 50.0)
    
    # Get process information
    process = executive_summary.get('process_detected', 'Unknown')
    
    # Get missing documents
    missing_documents = missing_docs_info.get('missing_documents', [])
    
    # Count documents
    documents_uploaded = executive_summary.get('total_documents_analyzed', 0)
    
    # Estimate required documents based on process
    process_required_docs = {
        'Company Incorporation': 5,
        'Employment & HR': 1,
        'General Legal': 1
    }
    required_documents = process_required_docs.get(process, len(missing_documents) + documents_uploaded)
    
    # Build the legacy format result
    result = {
        'process': process,
        'documents_uploaded': documents_uploaded,
        'required_documents': required_documents,
        'missing_documents': missing_documents,
        'issues_found': issues_found,
        'compliance_score': int(compliance_score),
        
        # Additional AI-powered insights
        'ai_insights': {
            'approval_likelihood': executive_summary.get('approval_likelihood', 'Unknown'),
            'timeline_estimate': executive_summary.get('timeline_estimate', 'Unknown'),
            'high_priority_issues': executive_summary.get('high_priority_issues', 0),
            'ai_confidence': ai_results.get('ai_confidence', 0.0),
            'recommended_actions': ai_results.get('predictive_analysis', {}).get('recommended_actions', [])
        },
        
        # Generated document templates
        'generated_templates': missing_docs_info.get('generated_templates', {}),
        
        # Performance metrics
        'processing_time': ai_results.get('performance_metrics', {}).get('average_processing_time', 0.0),
        'analysis_timestamp': ai_results.get('generated_timestamp', 0)
    }
    
    return result

def fallback_basic_analysis(proc_info: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback to basic analysis if AI fails"""
    # Import the original validation logic
    from src.core.validate import analyze_bundle as original_analyze_bundle
    
    return original_analyze_bundle(proc_info)

def get_ai_system_status() -> Dict[str, Any]:
    """Get the status of the AI system"""
    try:
        orchestrator = get_ai_orchestrator()
        return orchestrator.get_system_status()
    except Exception as e:
        return {
            'system_ready': False,
            'error': str(e),
            'fallback_mode': True
        }

def generate_missing_document(doc_type: str, company_details: Dict[str, Any]) -> str:
    """Generate a missing document template using AI"""
    try:
        orchestrator = get_ai_orchestrator()
        if orchestrator.document_generator:
            return orchestrator.document_generator.generate_document(doc_type, company_details)
        else:
            return f"Template for {doc_type} (AI generator not available)"
    except Exception as e:
        return f"Error generating {doc_type}: {str(e)}"

def get_compliance_insights(query: str, document_text: str) -> List[Dict[str, Any]]:
    """Get RAG-based compliance insights for a specific query"""
    try:
        orchestrator = get_ai_orchestrator()
        if orchestrator.rag_retriever:
            results = orchestrator.rag_retriever.retrieve(query, k=5)
            return [
                {
                    'source': result['metadata'].get('source', 'Unknown'),
                    'text': result['text'][:300] + '...' if len(result['text']) > 300 else result['text'],
                    'similarity_score': result['similarity_score'],
                    'relevance_score': result.get('relevance_score', result['similarity_score'])
                }
                for result in results
            ]
        else:
            return []
    except Exception as e:
        return [{'error': str(e)}]

def train_ai_models():
    """Manually trigger AI model training"""
    try:
        orchestrator = get_ai_orchestrator()
        orchestrator.train_models_if_needed(force_retrain=True)
        return {'status': 'success', 'message': 'AI models trained successfully'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

# Advanced features that will blow away the competition
def get_document_similarity_analysis(documents: Dict[str, str]) -> Dict[str, Any]:
    """Analyze similarity between multiple documents"""
    try:
        orchestrator = get_ai_orchestrator()
        if orchestrator.document_embedder:
            # This would use the document similarity analyzer
            doc_texts = list(documents.values())
            doc_names = list(documents.keys())
            
            # Placeholder for actual similarity analysis
            return {
                'similarity_matrix': 'Would contain document similarity scores',
                'duplicate_clauses': 'Would identify duplicate or similar clauses',
                'inconsistencies': 'Would flag inconsistent information'
            }
    except Exception as e:
        return {'error': str(e)}

def get_predictive_approval_analysis(document_bundle: Dict[str, Any]) -> Dict[str, Any]:
    """Predict approval likelihood and timeline"""
    try:
        orchestrator = get_ai_orchestrator()
        # This would use the predictive analysis from the orchestrator
        return {
            'approval_probability': 'Would provide ML-based approval prediction',
            'timeline_estimate': 'Would estimate processing timeline',
            'risk_factors': 'Would identify key risk factors',
            'recommended_actions': 'Would provide prioritized action items'
        }
    except Exception as e:
        return {'error': str(e)}

def get_automated_document_generation(process_type: str, company_info: Dict[str, Any]) -> Dict[str, str]:
    """Generate complete document set for a process"""
    try:
        orchestrator = get_ai_orchestrator()
        if orchestrator.document_generator:
            
            # Define required documents for each process
            process_documents = {
                'Company Incorporation': [
                    'Articles of Association',
                    'Memorandum of Association', 
                    'Board Resolution',
                    'Shareholder Resolution',
                    'UBO Declaration'
                ],
                'Employment & HR': [
                    'Employment Contract'
                ]
            }
            
            generated_docs = {}
            required_docs = process_documents.get(process_type, [])
            
            for doc_type in required_docs:
                generated_docs[doc_type] = orchestrator.document_generator.generate_document(
                    doc_type, company_info
                )
                
            return generated_docs
    except Exception as e:
        return {'error': str(e)}

# Export the main function to replace the original
analyze_bundle = analyze_bundle_advanced
