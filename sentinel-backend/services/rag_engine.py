from typing import List, Dict
import google.generativeai as genai
import os

class RAGEngine:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # For hackathon, doing simple keyword matching fallback as defined in PRD
        # since full ChromaDB setup can be overkill/fragile for a 2-minute demo
        
    async def search_incidents(self, query: str, incident_history: List[Dict], top_k: int = 3) -> List[Dict]:
        # Simple fallback search
        keywords = query.lower().split()
        scored = []
        for incident in incident_history:
            score = 0
            text_to_search = f"{incident['title']} {incident['type']} {incident['contributing_factors']} {incident['description']}".lower()
            for kw in keywords:
                if kw in text_to_search:
                    score += 1
            if score > 0:
                scored.append((score, incident))
                
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]
        
    async def search_regulations(self, query: str, regulations: List[Dict], top_k: int = 3) -> List[Dict]:
        keywords = query.lower().split()
        scored = []
        for reg in regulations:
            score = 0
            text_to_search = f"{reg['title']} {reg['content']} {reg['applicability']} {reg['section']}".lower()
            for kw in keywords:
                if kw in text_to_search:
                    score += 1
            if score > 0:
                scored.append((score, reg))
                
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_k]]
        
    def format_incident_context(self, incidents: List[Dict]) -> str:
        if not incidents:
            return "No similar historical incidents found."
        
        ctx = "SIMILAR HISTORICAL INCIDENTS:\n"
        for i in incidents:
            ctx += f"- {i['title']} ({i['date']}): {i['type']} resulting in {i['casualties']} deaths. Root cause: {i['root_cause']}\n"
        return ctx
        
    def format_regulation_context(self, regulations: List[Dict]) -> str:
        if not regulations:
            return "No specific regulatory references found."
            
        ctx = "APPLICABLE REGULATIONS:\n"
        for r in regulations:
            ctx += f"- {r['standard']} {r['section']} ({r['title']}): {r['content']}\n"
        return ctx
