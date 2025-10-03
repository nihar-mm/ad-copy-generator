# MyMuse Brand Voice Integration

## Overview

This document outlines the comprehensive integration of MyMuse's brand voice analysis and prompt template into the ad copy regenerator system. The integration ensures that all generated ad copy aligns with MyMuse's sensual, playful, and empowering brand voice while maintaining category-specific tone variations.

## Key Features Implemented

### 1. Brand Voice Configuration (`server/app/pipeline/brand_voice/mymuse_config.py`)

- **Core Brand Voice**: Sensual, playful, and empowering tone
- **Category-Specific Modifiers**: Different tone adjustments for vibrators, lubricants, massage oils, candles, games, and accessories
- **Brand Lexicon**: Preferred terms, sensory words, empowering phrases, and playful elements
- **Style Guardrails**: Clear guidelines on what to use and avoid
- **Prompt Template**: Structured template for generating MyMuse-specific ad copy

### 2. Product Category Detection (`server/app/pipeline/brand_voice/category_detector.py`)

- **Automatic Detection**: Analyzes OCR text and product names to detect product category
- **Confidence Scoring**: Provides confidence levels for category detection
- **Tone Adjustments**: Automatically adjusts tone based on detected category
- **Validation**: Ensures text consistency with expected category

### 3. Brand Voice Validation (`server/app/pipeline/brand_voice/validation_guardrails.py`)

- **Comprehensive Validation**: Validates headlines, subheadlines, and full copy
- **MyMuse-Specific Checks**: Ensures adherence to brand voice guidelines
- **Issue Detection**: Identifies buzzwords, corporate speak, clinical terms, and vulgar language
- **Recommendations**: Provides specific suggestions for improvement
- **Scoring System**: Quantifies brand voice alignment

### 4. Enhanced Pipeline Integration

#### Updated Files:
- `server/app/pipeline/generate/generate.py`: MyMuse-specific prompts and validation
- `server/app/pipeline/guardrails/constraints.py`: Brand voice scoring and validation
- `server/app/pipeline/semantics/extract.py`: Category detection integration
- `server/app/workers/tasks.py`: Enhanced scoring and prioritization
- `server/app/routes/jobs.py`: Product category parameter support

## Category-Specific Tone Guidelines

### Vibrators
- **Tone**: Sensual, bold, empowering, cheeky
- **Keywords**: "unleash", "inner goddess", "powerful vibes", "playful sensations"
- **Style**: Enthusiastic about pleasure and discovery, empowering language

### Lubricants
- **Tone**: Playful, inviting, cheeky, reassuring
- **Keywords**: "all fun and no friction", "ultra smooth", "silky", "gentle"
- **Style**: Fun wordplay to remove awkwardness, lighthearted promises

### Massage Oils
- **Tone**: Sensual, romantic, indulgent, warm
- **Keywords**: "heat things up", "deliciously warm", "fragrant", "skin-tingling"
- **Style**: Descriptive and mood-setting, evokes multiple senses

### Candles
- **Tone**: Sensual, romantic, indulgent, warm
- **Keywords**: "heat things up", "deliciously warm", "fragrant", "skin-tingling"
- **Style**: Descriptive and mood-setting, evokes multiple senses

### Games
- **Tone**: Fun, daring, flirty, energetic
- **Keywords**: "wild adventure", "excitement", "fun", "flirty", "spice up"
- **Style**: Playful and lighthearted, focuses on building excitement

### Accessories
- **Tone**: Fun, daring, flirty, energetic
- **Keywords**: "wild adventure", "excitement", "fun", "flirty", "spice up"
- **Style**: Playful and lighthearted, focuses on building excitement

## API Enhancements

### New Parameter
- `product_category`: Specifies the product category (vibrators, lubricants, massage_oils, candles, games, accessories)
- **Default**: "vibrators"
- **Validation**: Automatically validates and falls back to default if invalid

### Enhanced Scoring
The system now prioritizes variants based on:
1. MyMuse validation score
2. Brand voice alignment
3. Tone consistency
4. Category alignment
5. Fit score
6. Voice similarity
7. Readability

## Validation System

### Brand Voice Checks
- ✅ Sensual, playful, and empowering language
- ✅ Category-appropriate keywords
- ✅ Avoids buzzwords and corporate speak
- ✅ Maintains tasteful, non-vulgar tone
- ✅ Focuses on benefits and experiences

### Issue Detection
- ❌ Buzzwords ("premium quality", "innovative", "revolutionary")
- ❌ Corporate speak ("ensures optimal", "provides superior")
- ❌ Clinical terms ("medically approved", "therapeutically")
- ❌ Vulgar language
- ❌ Length violations
- ❌ Lack of brand characteristics

## Usage Examples

### API Request
```json
{
  "image": "uploaded_image.jpg",
  "product_name": "Premium Vibrator",
  "product_category": "vibrators",
  "brand_voice": "sensual and empowering",
  "n_variants": 10
}
```

### Generated Output
```json
{
  "headline": "Unleash Your Inner Goddess",
  "subheadline": "Discover new heights of pleasure with our premium vibrator",
  "cta": "Shop now",
  "scores": {
    "mymuse_validation": 1.0,
    "mymuse_brand_voice": 0.85,
    "mymuse_tone_consistency": 0.9,
    "mymuse_category_alignment": 0.95
  },
  "mymuse_validation_details": {
    "valid": true,
    "score": 1.0,
    "issues": [],
    "recommendations": []
  }
}
```

## Testing Results

The integration has been thoroughly tested with:
- ✅ Product category detection (6/6 categories correctly identified)
- ✅ Brand voice prompt generation (all categories working)
- ✅ Validation system (high-quality copy scores high, low-quality copy scores low)
- ✅ Category tone modifiers (all categories properly configured)
- ✅ Individual validation functions (working correctly)
- ✅ Complete category and tone suggestion (working correctly)

## Benefits

1. **Consistent Brand Voice**: All generated copy maintains MyMuse's distinctive tone
2. **Category Optimization**: Copy is tailored to specific product categories
3. **Quality Assurance**: Comprehensive validation ensures high-quality output
4. **Automatic Detection**: System can automatically detect product categories
5. **Scalable**: Easy to add new categories or modify existing ones
6. **Maintainable**: Clear separation of concerns and modular design

## Future Enhancements

- Add more product categories as needed
- Implement A/B testing for different tone variations
- Add sentiment analysis for emotional alignment
- Create category-specific image analysis
- Implement learning from user feedback

## Conclusion

The MyMuse brand voice integration provides a comprehensive solution for generating ad copy that perfectly aligns with the brand's sensual, playful, and empowering voice. The system ensures consistency across all product categories while maintaining the flexibility to adapt to specific product types and marketing contexts.
