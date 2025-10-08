"""
Product Category Detection and Tone Adjustment
Automatically detects product category from image text and adjusts tone accordingly
"""

import re
from typing import Dict, List, Optional, Tuple
from .mymuse_config import CATEGORY_TONE_MODIFIERS, get_category_tone

class ProductCategoryDetector:
    """Detects product category from text and provides tone adjustments"""
    
    def __init__(self):
        self.category_keywords = {
            "vibrators": [
                "vibrator", "vibe", "massager", "stimulator", "bullet", "rabbit", 
                "wand", "g-spot", "clitoral", "internal", "external", "dual",
                "rechargeable", "waterproof", "silicone", "pleasure", "orgasm"
            ],
            "lubricants": [
                "lube", "lubricant", "lubrication", "water-based", "silicone-based",
                "hybrid", "aloe", "glycerin", "paraben-free", "smooth", "slippery",
                "friction", "comfort", "sensation", "wet", "moisture"
            ],
            "massage_oils": [
                "massage oil", "massage", "oil", "aromatherapy", "essential oil",
                "warming", "cooling", "tingling", "sensual", "relaxing", "stress",
                "tension", "muscle", "skin", "moisturizing", "fragrant"
            ],
            "candles": [
                "candle", "melt", "wax", "warming", "mood", "ambiance", "light",
                "fragrant", "aromatic", "romantic", "dim", "glow", "flame",
                "massage oil", "melted", "warm", "sensual"
            ],
            "games": [
                "game", "card", "dice", "board", "couple", "date night", "fun",
                "adventure", "challenge", "question", "dare", "truth", "wild",
                "spicy", "romantic", "intimate", "playful"
            ],
            "accessories": [
                "handcuff", "blindfold", "whip", "feather", "toy", "accessory",
                "restraint", "bondage", "kink", "fetish", "leather", "silk",
                "rope", "chain", "collar", "cuff", "tie", "bind"
            ]
        }
        
        self.category_patterns = {
            "vibrators": r"\b(vibrator|vibe|massager|stimulator|bullet|rabbit|wand)\b",
            "lubricants": r"\b(lube|lubricant|water-based|silicone-based|hybrid)\b",
            "massage_oils": r"\b(massage\s+oil|aromatherapy|essential\s+oil|warming|cooling)\b",
            "candles": r"\b(candle|melt|wax|warming|mood|ambiance)\b",
            "games": r"\b(game|card|dice|board|couple|date\s+night|adventure)\b",
            "accessories": r"\b(handcuff|blindfold|whip|feather|restraint|bondage|kink)\b"
        }
    
    def detect_category(self, text: str, product_name: str = "") -> Tuple[str, float]:
        """
        Detect product category from text with confidence score
        
        Args:
            text: Text to analyze (OCR results, product descriptions, etc.)
            product_name: Optional product name for additional context
            
        Returns:
            Tuple of (category, confidence_score)
        """
        if not text and not product_name:
            return "vibrators", 0.0
        
        combined_text = f"{text} {product_name}".lower()
        
        category_scores = {}
        
        # Score based on keyword matches
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword.lower() in combined_text:
                    score += 1
            category_scores[category] = score / len(keywords)
        
        # Score based on pattern matches
        for category, pattern in self.category_patterns.items():
            matches = len(re.findall(pattern, combined_text, re.IGNORECASE))
            if matches > 0:
                category_scores[category] = category_scores.get(category, 0) + (matches * 0.2)
        
        # Find best category
        if not category_scores or max(category_scores.values()) == 0:
            return "vibrators", 0.0
        
        best_category = max(category_scores, key=category_scores.get)
        confidence = min(1.0, category_scores[best_category])
        
        return best_category, confidence
    
    def get_tone_adjustments(self, category: str) -> Dict[str, any]:
        """
        Get tone adjustments for a specific category
        
        Args:
            category: Product category
            
        Returns:
            Dictionary with tone adjustments
        """
        category_tone = get_category_tone(category)
        
        return {
            "tone_modifiers": category_tone.get("tone", "").split(", "),
            "keywords": category_tone.get("keywords", []),
            "style_guidance": category_tone.get("style", ""),
            "example_headline": category_tone.get("example_headline", ""),
            "example_subheadline": category_tone.get("example_subheadline", "")
        }
    
    def suggest_category_from_image_text(self, ocr_text: str, product_name: str = "") -> Dict[str, any]:
        """
        Suggest product category and tone adjustments from image text
        
        Args:
            ocr_text: Text extracted from image
            product_name: Optional product name
            
        Returns:
            Dictionary with category detection results and tone adjustments
        """
        category, confidence = self.detect_category(ocr_text, product_name)
        tone_adjustments = self.get_tone_adjustments(category)
        
        return {
            "detected_category": category,
            "confidence": confidence,
            "tone_adjustments": tone_adjustments,
            "suggested_keywords": tone_adjustments["keywords"][:5],  # Top 5 keywords
            "style_guidance": tone_adjustments["style_guidance"]
        }
    
    def validate_category_consistency(self, text: str, category: str) -> Dict[str, any]:
        """
        Validate if text is consistent with the given category
        
        Args:
            text: Text to validate
            category: Expected category
            
        Returns:
            Validation results
        """
        expected_keywords = self.category_keywords.get(category, [])
        text_lower = text.lower()
        
        keyword_matches = sum(1 for keyword in expected_keywords if keyword in text_lower)
        keyword_score = keyword_matches / max(1, len(expected_keywords))
        
        # Check for category-specific patterns
        pattern = self.category_patterns.get(category, "")
        pattern_matches = len(re.findall(pattern, text, re.IGNORECASE)) if pattern else 0
        pattern_score = min(1.0, pattern_matches * 0.3)
        
        overall_score = (keyword_score + pattern_score) / 2
        
        return {
            "is_consistent": overall_score > 0.3,
            "keyword_score": keyword_score,
            "pattern_score": pattern_score,
            "overall_score": overall_score,
            "matched_keywords": [kw for kw in expected_keywords if kw in text_lower]
        }

# Global instance
category_detector = ProductCategoryDetector()

def detect_product_category(text: str, product_name: str = "") -> Tuple[str, float]:
    """Convenience function for category detection"""
    return category_detector.detect_category(text, product_name)

def get_category_tone_adjustments(category: str) -> Dict[str, any]:
    """Convenience function for tone adjustments"""
    return category_detector.get_tone_adjustments(category)

def suggest_category_and_tone(ocr_text: str, product_name: str = "") -> Dict[str, any]:
    """Convenience function for complete category and tone suggestion"""
    return category_detector.suggest_category_from_image_text(ocr_text, product_name)
