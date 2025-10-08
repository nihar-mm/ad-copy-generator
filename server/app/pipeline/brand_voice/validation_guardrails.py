"""
MyMuse Brand Voice Validation Guardrails
Comprehensive validation system to ensure generated copy aligns with MyMuse's brand voice
"""

import re
from typing import Dict, List, Tuple, Optional
from .mymuse_config import (
    MYMUSE_BRAND_VOICE, 
    CATEGORY_TONE_MODIFIERS, 
    BRAND_LEXICON, 
    STYLE_GUARDRAILS,
    VALIDATION_EXAMPLES
)

class MyMuseBrandVoiceValidator:
    """Validates ad copy against MyMuse brand voice guidelines"""
    
    def __init__(self):
        self.buzzwords = [
            "premium quality", "innovative", "revolutionary", "best-in-class", 
            "world-class", "cutting-edge", "state-of-the-art", "next-generation",
            "optimal", "maximum", "ultimate", "superior", "advanced", "professional"
        ]
        
        self.corporate_phrases = [
            "ensures optimal", "guarantees maximum", "provides superior",
            "delivers exceptional", "offers unparalleled", "features advanced",
            "utilizes cutting-edge", "leverages innovative", "implements state-of-the-art"
        ]
        
        self.clinical_terms = [
            "medically approved", "clinically tested", "scientifically proven",
            "therapeutic", "treatment", "therapy", "medical grade", "pharmaceutical"
        ]
        
        self.vulgar_terms = [
            "fuck", "shit", "damn", "bitch", "asshole", "dick", "pussy", "cock"
        ]
        
        self.empowering_phrases = [
            "unleash", "discover", "explore", "embrace", "empower", "confidence",
            "goddess", "inner", "release", "ignite", "melt", "indulge"
        ]
        
        self.sensual_words = [
            "pleasure", "intimacy", "passion", "bliss", "tingling", "smooth",
            "warm", "sensual", "arousing", "delicious", "fragrant", "glow"
        ]
        
        self.playful_elements = [
            "fun", "playful", "adventure", "excitement", "wild", "spice",
            "wink", "tease", "cheeky", "flirty", "naughty", "mischievous"
        ]

    def validate_headline(self, headline: str, category: str = "vibrators") -> Dict[str, any]:
        """Validate headline against MyMuse brand voice"""
        if not headline:
            return {"valid": False, "score": 0.0, "issues": ["Empty headline"]}
        
        issues = []
        score = 1.0
        
        # Check length
        if len(headline) > 32:
            issues.append("Headline too long")
            score -= 0.2
        
        # Check for buzzwords
        buzzword_matches = [bw for bw in self.buzzwords if bw.lower() in headline.lower()]
        if buzzword_matches:
            issues.append(f"Contains buzzwords: {', '.join(buzzword_matches)}")
            score -= 0.3
        
        # Check for corporate speak
        corporate_matches = [cp for cp in self.corporate_phrases if cp.lower() in headline.lower()]
        if corporate_matches:
            issues.append(f"Contains corporate speak: {', '.join(corporate_matches)}")
            score -= 0.3
        
        # Check for clinical terms
        clinical_matches = [ct for ct in self.clinical_terms if ct.lower() in headline.lower()]
        if clinical_matches:
            issues.append(f"Contains clinical terms: {', '.join(clinical_matches)}")
            score -= 0.2
        
        # Check for vulgar language
        vulgar_matches = [vt for vt in self.vulgar_terms if vt.lower() in headline.lower()]
        if vulgar_matches:
            issues.append(f"Contains vulgar language: {', '.join(vulgar_matches)}")
            score -= 0.5
        
        # Check for MyMuse brand characteristics
        empowering_count = sum(1 for ep in self.empowering_phrases if ep.lower() in headline.lower())
        sensual_count = sum(1 for sw in self.sensual_words if sw.lower() in headline.lower())
        playful_count = sum(1 for pe in self.playful_elements if pe.lower() in headline.lower())
        
        if empowering_count == 0 and sensual_count == 0 and playful_count == 0:
            issues.append("Lacks MyMuse brand characteristics (empowering, sensual, playful)")
            score -= 0.3
        
        # Check category alignment
        category_tone = CATEGORY_TONE_MODIFIERS.get(category, {})
        category_keywords = category_tone.get("keywords", [])
        category_matches = sum(1 for kw in category_keywords if kw.lower() in headline.lower())
        
        if category_keywords and category_matches == 0:
            issues.append(f"Doesn't align with {category} category tone")
            score -= 0.2
        
        # More flexible validation - be more lenient with scoring
        validation_threshold = 0.2  # Very lenient for headlines
        
        return {
            "valid": score >= validation_threshold,
            "score": max(0.0, score),
            "issues": issues,
            "empowering_count": empowering_count,
            "sensual_count": sensual_count,
            "playful_count": playful_count,
            "category_matches": category_matches,
            "benefit_count": 0  # Headlines don't need benefit focus
        }
    
    def validate_subheadline(self, subheadline: str, category: str = "vibrators") -> Dict[str, any]:
        """Validate subheadline against MyMuse brand voice"""
        if not subheadline:
            return {"valid": False, "score": 0.0, "issues": ["Empty subheadline"]}
        
        issues = []
        score = 1.0
        
        # Check length
        if len(subheadline) > 60:
            issues.append("Subheadline too long")
            score -= 0.2
        
        # Check for buzzwords
        buzzword_matches = [bw for bw in self.buzzwords if bw.lower() in subheadline.lower()]
        if buzzword_matches:
            issues.append(f"Contains buzzwords: {', '.join(buzzword_matches)}")
            score -= 0.2
        
        # Check for corporate speak
        corporate_matches = [cp for cp in self.corporate_phrases if cp.lower() in subheadline.lower()]
        if corporate_matches:
            issues.append(f"Contains corporate speak: {', '.join(corporate_matches)}")
            score -= 0.2
        
        # Check for clinical terms
        clinical_matches = [ct for ct in self.clinical_terms if ct.lower() in subheadline.lower()]
        if clinical_matches:
            issues.append(f"Contains clinical terms: {', '.join(clinical_matches)}")
            score -= 0.2
        
        # Check for vulgar language
        vulgar_matches = [vt for vt in self.vulgar_terms if vt.lower() in subheadline.lower()]
        if vulgar_matches:
            issues.append(f"Contains vulgar language: {', '.join(vulgar_matches)}")
            score -= 0.5
        
        # Check for MyMuse brand characteristics
        empowering_count = sum(1 for ep in self.empowering_phrases if ep.lower() in subheadline.lower())
        sensual_count = sum(1 for sw in self.sensual_words if sw.lower() in subheadline.lower())
        playful_count = sum(1 for pe in self.playful_elements if pe.lower() in subheadline.lower())
        
        if empowering_count == 0 and sensual_count == 0 and playful_count == 0:
            issues.append("Lacks MyMuse brand characteristics")
            score -= 0.2
        
        # Check for benefit focus
        benefit_words = ["enhance", "improve", "boost", "increase", "better", "more", "new", "discover"]
        benefit_count = sum(1 for bw in benefit_words if bw.lower() in subheadline.lower())
        
        if benefit_count == 0:
            issues.append("Doesn't focus on benefits")
            score -= 0.1
        
        # More flexible validation - be more lenient with scoring
        validation_threshold = 0.2  # Very lenient for subheadlines
        
        return {
            "valid": score >= validation_threshold,
            "score": max(0.0, score),
            "issues": issues,
            "empowering_count": empowering_count,
            "sensual_count": sensual_count,
            "playful_count": playful_count,
            "benefit_count": benefit_count
        }
    
    def validate_full_copy(self, headline: str, subheadline: str, category: str = "vibrators") -> Dict[str, any]:
        """Validate complete ad copy against MyMuse brand voice"""
        headline_validation = self.validate_headline(headline, category)
        subheadline_validation = self.validate_subheadline(subheadline, category)
        
        # Overall validation
        overall_score = (headline_validation["score"] + subheadline_validation["score"]) / 2
        all_issues = headline_validation["issues"] + subheadline_validation["issues"]
        
        # Check for consistency
        consistency_issues = []
        
        # Check if both headline and subheadline have similar tone
        headline_tone = self._detect_tone(headline)
        subheadline_tone = self._detect_tone(subheadline)
        
        if headline_tone != subheadline_tone and abs(len(headline_tone) - len(subheadline_tone)) > 2:
            consistency_issues.append("Inconsistent tone between headline and subheadline")
            overall_score -= 0.1
        
        # Check for repetition
        headline_words = set(headline.lower().split())
        subheadline_words = set(subheadline.lower().split())
        common_words = headline_words.intersection(subheadline_words)
        
        if len(common_words) > 3:
            consistency_issues.append("Too much repetition between headline and subheadline")
            overall_score -= 0.1
        
        # More flexible validation for different product categories
        # For condoms/safe sex products, be more lenient with brand voice requirements
        is_safe_sex_content = any(word in (headline + " " + subheadline).lower() 
                                for word in ["condom", "safe", "protection", "responsible", "responsible"])
        
        if is_safe_sex_content:
            # For safe sex content, lower the validation threshold
            validation_threshold = 0.4
            max_issues = 5
        else:
            validation_threshold = 0.6
            max_issues = 3
        
        return {
            "valid": overall_score >= validation_threshold and len(all_issues) < max_issues,
            "score": max(0.0, overall_score),
            "headline_validation": headline_validation,
            "subheadline_validation": subheadline_validation,
            "consistency_issues": consistency_issues,
            "all_issues": all_issues + consistency_issues,
            "recommendations": self._generate_recommendations(headline_validation, subheadline_validation, category)
        }
    
    def _detect_tone(self, text: str) -> str:
        """Detect the tone of text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in self.empowering_phrases):
            return "empowering"
        elif any(word in text_lower for word in self.sensual_words):
            return "sensual"
        elif any(word in text_lower for word in self.playful_elements):
            return "playful"
        else:
            return "neutral"
    
    def _generate_recommendations(self, headline_validation: Dict, subheadline_validation: Dict, category: str) -> List[str]:
        """Generate recommendations for improving the copy"""
        recommendations = []
        
        category_tone = CATEGORY_TONE_MODIFIERS.get(category, {})
        category_keywords = category_tone.get("keywords", [])
        
        if headline_validation["empowering_count"] == 0:
            recommendations.append("Add empowering language to headline (e.g., 'unleash', 'discover', 'explore')")
        
        if headline_validation["sensual_count"] == 0:
            recommendations.append("Add sensual language to headline (e.g., 'pleasure', 'intimacy', 'passion')")
        
        if headline_validation["playful_count"] == 0:
            recommendations.append("Add playful elements to headline (e.g., 'fun', 'adventure', 'excitement')")
        
        if headline_validation["category_matches"] == 0 and category_keywords:
            recommendations.append(f"Use {category}-specific keywords: {', '.join(category_keywords[:3])}")
        
        if subheadline_validation["benefit_count"] == 0:
            recommendations.append("Focus on benefits in subheadline (e.g., 'enhance', 'improve', 'discover')")
        
        return recommendations

# Global validator instance
brand_voice_validator = MyMuseBrandVoiceValidator()

def validate_mymuse_copy(headline: str, subheadline: str, category: str = "vibrators") -> Dict[str, any]:
    """Convenience function for validating MyMuse copy"""
    return brand_voice_validator.validate_full_copy(headline, subheadline, category)

def validate_headline_only(headline: str, category: str = "vibrators") -> Dict[str, any]:
    """Convenience function for validating headline only"""
    return brand_voice_validator.validate_headline(headline, category)

def validate_subheadline_only(subheadline: str, category: str = "vibrators") -> Dict[str, any]:
    """Convenience function for validating subheadline only"""
    return brand_voice_validator.validate_subheadline(subheadline, category)
