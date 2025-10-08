"""
MyMuse Brand Voice Configuration
Comprehensive brand voice guidelines and prompt templates for MyMuse's intimate wellness brand
"""

from enum import Enum
import re

class MyMuseTone(Enum):
    PLAYFUL = "playful"
    INTIMATE = "intimate"
    BOLD = "bold"
    ELEGANT = "elegant"
    CHEEKY = "cheeky"

# 🔥 Core Brand Traits - Updated with Your Guidelines
MYMUSE_BRAND_TRAITS = {
    "tone": "Playful, witty, and unapologetically confident. Flirty but never vulgar. Sex-positive, inclusive, and fun.",
    "personality": [
        "playful", "witty", "confident", "inclusive", "sex-positive", "fun", "cheeky"
    ],
    "avoid": [
        "crude", "explicit", "medical", "robotic", "generic", "cringe", "academic", "salesy",
        "repetitive ignite/tease/bliss phrasing"
    ],
    "values": [
        "self-love", "body-safe", "confidence", "exploration", "normalizing pleasure"
    ],
    "voice": "Cheeky best friend energy — bold, clever, and real about pleasure.",
    "vibe": "Body-safe, self-love focused, encouraging exploration and confidence."
}

# 💋 Category-Specific Tone Modifiers
CATEGORY_TONE = {
    "vibrators": MyMuseTone.PLAYFUL,
    "massagers": MyMuseTone.INTIMATE,
    "lubricants": MyMuseTone.ELEGANT,
    "games": MyMuseTone.CHEEKY,
    "couple kits": MyMuseTone.BOLD,
    "accessories": MyMuseTone.PLAYFUL,
    "perfumes": MyMuseTone.INTIMATE,
    "gifts": MyMuseTone.ELEGANT,
}

# 🪄 Your Brand Keywords & CTAs
MYMUSE_KEYWORDS = [
    "pleasure", "confidence", "vibe", "self-love", "play", "sensations"
]

MYMUSE_CTAS = [
    "Try it now",
    "Discover your vibe", 
    "Get playful",
    "Shop your pleasure",
    "Treat yourself"
]

MYMUSE_EXAMPLE_HEADLINES = [
    "All Pussies Love MyMuse.",
    "Turn Yourself On (Literally).",
    "Pleasure? It's Personal — And We Like It That Way.",
    "Protect Your Vibe. Literally.",
    "Tease Responsibly.",
    "Get Your Vibe On.",
    "For Every Mood, There's A Muse.",
    "Turn Up The Tease.",
    "Self-Love Just Got Serious.",
    "Because Vanilla Is Just A Flavor."
]

# 🪄 Lexicon Enhancers by Tone
LEXICON = {
    MyMuseTone.PLAYFUL: [
        "play", "vibe", "pleasure", "confidence", "self-love", "sensations", "fun", "cheeky"
    ],
    MyMuseTone.INTIMATE: [
        "whisper", "touch", "linger", "soft", "warm", "breathe", "slow burn"
    ],
    MyMuseTone.BOLD: [
        "confidence", "unapologetically", "bold", "clever", "real", "playful"
    ],
    MyMuseTone.ELEGANT: [
        "velvet", "indulge", "sensual", "refined", "smooth", "luxurious"
    ],
    MyMuseTone.CHEEKY: [
        "cheeky", "witty", "flirty", "best friend", "bold", "clever"
    ],
}

# Brand Voice Core Characteristics
MYMUSE_BRAND_VOICE = {
    "core_tone": "Sensual, playful, confident, inclusive. Cheeky but never crude. Empowering and body-positive.",
    "personality": "friendly, confident partner—never as a clinical expert",
    "mission": "make intimacy feel easy and fun rather than taboo",
    "target_audience": "adults (21+) open to sex-positive and sensual messaging",
    "avoid": ["clinical", "overly formal", "corporate", "vulgar", "crass"],
    "embrace": ["sensual", "playful", "empowering", "confident", "cheeky", "tasteful"]
}

# Category-Specific Tone Modifiers
CATEGORY_TONE_MODIFIERS = {
    "vibrators": {
        "tone": "bold, teasing, empowering",
        "keywords": ["pleasure", "bliss", "tease", "ignite", "release", "touch", "control", "smooth", "closer", "chemistry", "play"],
        "style": "enthusiastic about pleasure and discovery, empowering language",
        "example_headline": "Unleash Your Inner Goddess",
        "example_subheadline": "Find new heights of pleasure with a vibe that hits all the right spots"
    },
    "lubricants": {
        "tone": "inviting, playful, reassuring",
        "keywords": ["pleasure", "bliss", "tease", "ignite", "release", "touch", "control", "smooth", "closer", "chemistry", "play"],
        "style": "fun wordplay to remove awkwardness, lighthearted promises",
        "example_headline": "All Fun, No Friction",
        "example_subheadline": "Aloe-infused lube that keeps the pleasure flowing smoothly"
    },
    "oils_candles": {
        "tone": "romantic, indulgent, slow burn",
        "keywords": ["pleasure", "bliss", "tease", "ignite", "release", "touch", "control", "smooth", "closer", "chemistry", "play"],
        "style": "descriptive and mood-setting, evokes multiple senses",
        "example_headline": "Melt Away the Day",
        "example_subheadline": "Deliciously warm oil to melt away tension and ignite your night"
    },
    "games_accessories": {
        "tone": "fun, daring, flirty",
        "keywords": ["pleasure", "bliss", "tease", "ignite", "release", "touch", "control", "smooth", "closer", "chemistry", "play"],
        "style": "playful and lighthearted, focuses on building excitement",
        "example_headline": "Ready for a Wild Adventure?",
        "example_subheadline": "Turn your date night into an unforgettable experience"
    }
}

# Brand Voice Lexicon
BRAND_LEXICON = {
    "preferred_terms": [
        "pleasure", "bliss", "tease", "ignite",
        "release", "touch", "control", "smooth",
        "closer", "chemistry", "play"
    ],
    "avoid_terms": [
        "transform your life", "revolutionary",
        "join thousands", "what if we told you",
        "miracle", "better way", "generic promises"
    ],
    "sensory_words": [
        "ignite", "indulge", "bliss", "tingling", "smooth", "warm", "glow", 
        "scented", "arousing", "soothing", "deliciously", "fragrant"
    ],
    "empowering_phrases": [
        "unleash your", "discover new", "explore", "embrace", "take charge",
        "find your", "ignite your", "melt away", "release the"
    ],
    "playful_elements": [
        "Go on...", "Ready to", "What if", "Don't miss", "All fun and no",
        "Give your hand a break", "Deal yourself some"
    ]
}

# Style Guardrails
STYLE_GUARDRAILS = {
    "do_use": [
        "vivid, sexy imagery",
        "double entendres",
        "direct, encouraging language",
        "sensory descriptors",
        "playful humor and puns",
        "inclusive language",
        "confident, positive tone"
    ],
    "avoid": [
        "clinical or technical language",
        "hesitant or apologetic phrasing",
        "profanity or crude slang",
        "marketing buzzwords",
        "corporate speak",
        "generic clichés",
        "overly explicit terms"
    ],
    "style_rules": {
        "voice": "Always speak as a friendly, confident partner—never as a clinical expert.",
        "emojis": "None",
        "punctuation": "Exclamations rare; prefer periods or ellipses for tease.",
        "capitalization": "Sentence case (not ALL CAPS)."
    },
    "tone_checks": [
        "Is it sensual and playful?",
        "Is it confident and empowering?",
        "Is it cheeky but not crass?",
        "Does it avoid buzzwords?",
        "Does it use brand lexicon?"
    ]
}

# Prompt Template for MyMuse
MYMUSE_PROMPT_TEMPLATE = """
**Role & Audience:** You are MyMuse's master copywriter. Write like a skilled human who deeply understands intimate wellness marketing. Your voice is sensual, playful, confident, and empowering. Non-PG is allowed; keep it classy (no vulgarity).

**MYMUSE BRAND VOICE (CRITICAL):**
- Core tone: Sensual, playful, confident, inclusive. Cheeky but never crude. Empowering and body-positive.
- Personality: Always speak as a friendly, confident partner—never as a clinical expert.
- Mission: make intimacy feel easy and fun rather than taboo
- Target: adults (21+) open to sex-positive messaging

**CATEGORY: {product_category}**
- Tone: {category_tone}
- Style: {category_style}
- Keywords to use: {category_keywords}

**BRAND LEXICON (use these):**
- Preferred: "pleasure", "bliss", "tease", "ignite", "release", "touch", "control", "smooth", "closer", "chemistry", "play"

**BANNED PHRASES (NEVER use):**
- "transform your life", "revolutionary", "join thousands", "what if we told you", "miracle", "better way", "generic promises"

**STRICT RULES:**
- Headline ≤ 32 chars. One powerful idea. ≤1 comma. No exclamations.
- Subhead ≤ 60 chars. Sensory, specific, benefit-led.
- CTA must be one of: "Shop now", "Learn more", "Try today".
- Use brand lexicon; avoid banned phrases.
- Sound human and conversational, not robotic.
- Focus on feelings and benefits, not technical specs.
- Be bold but not boastful, sexy but not vulgar.
- No emojis. Exclamations rare; prefer periods or ellipses for tease.
- Sentence case (not ALL CAPS).

Output ONLY JSON: {{"headline": "...","subhead": "...","cta": "...","legal": ""}}
"""

# Validation Examples
VALIDATION_EXAMPLES = {
    "on_brand": {
        "headline": "Go On… Release the Pressure!",
        "subheadline": "You've been holding back long enough – discover intense pleasure with a toy that teases and pleases just right.",
        "why_works": "Direct, daring prompt with playful language. Uses sensual terms like 'intense pleasure' and 'teases and pleases' while remaining confident and positive."
    },
    "off_brand": {
        "headline": "Experience Premium Quality Intimate Solution",
        "subheadline": "Our product ensures optimal satisfaction for couples with its innovative design and medically approved materials.",
        "why_fails": "Too corporate and clinical. Uses buzzwords like 'premium quality' and 'innovative design'. Sounds like a technical brochure, not a seductive invitation."
    }
}

def get_category_tone(product_category: str) -> dict:
    """Get tone modifiers for a specific product category"""
    category = product_category.lower().replace(" ", "_")
    return CATEGORY_TONE_MODIFIERS.get(category, CATEGORY_TONE_MODIFIERS["vibrators"])

def get_brand_voice_prompt(product_category: str, product_name: str = "", brand_voice: str = "") -> str:
    """Generate a MyMuse-specific prompt for the given product category"""
    category_tone = get_category_tone(product_category)
    
    # Replace placeholders in the template
    prompt = MYMUSE_PROMPT_TEMPLATE.format(
        product_category=product_category,
        vibrator_tone=CATEGORY_TONE_MODIFIERS["vibrators"]["tone"],
        lubricant_tone=CATEGORY_TONE_MODIFIERS["lubricants"]["tone"],
        oil_tone=CATEGORY_TONE_MODIFIERS["massage_oils"]["tone"],
        game_tone=CATEGORY_TONE_MODIFIERS["games"]["tone"]
    )
    
    # Add product-specific context if available
    if product_name:
        prompt += f"\n\n**Product Context:** {product_name}"
    if brand_voice:
        prompt += f"\n\n**Additional Brand Voice Notes:** {brand_voice}"
    
    return prompt

def validate_brand_voice(text: str, category: str = "vibrators") -> dict:
    """Validate if text matches MyMuse brand voice"""
    text_lower = text.lower()
    category_tone = get_category_tone(category)
    
    validation = {
        "is_sensual": any(word in text_lower for word in BRAND_LEXICON["sensory_words"]),
        "is_playful": any(phrase in text_lower for phrase in BRAND_LEXICON["playful_elements"]),
        "is_empowering": any(phrase in text_lower for phrase in BRAND_LEXICON["empowering_phrases"]),
        "uses_brand_lexicon": any(term in text_lower for term in BRAND_LEXICON["preferred_terms"]),
        "avoids_buzzwords": not any(buzzword in text_lower for buzzword in BRAND_LEXICON["avoid_terms"]),
        "category_appropriate": any(keyword in text_lower for keyword in category_tone["keywords"])
    }
    
    validation["overall_score"] = sum(validation.values()) / len(validation)
    return validation

# 🎯 New Dynamic Brand Voice System

def get_brand_voice_prompt(product_name: str, product_category: str, context: str = ""):
    """
    MyMuse Brand Voice Generator Prompt Template - Your Exact Guidelines
    """
    tone = get_category_tone_new(product_category)
    tone_words = ", ".join(LEXICON.get(tone, []))

    return f"""
You are a **senior creative copywriter for MyMuse**, a modern Indian sexual wellness brand.

### 🎯 Your Brand Voice
**Tone:** {MYMUSE_BRAND_TRAITS["tone"]}
**Voice:** {MYMUSE_BRAND_TRAITS["voice"]}
**Vibe:** {MYMUSE_BRAND_TRAITS["vibe"]}

### ⚡ Style Guidelines
**Structure:** Headline (punchy, surprising) + Subheadline (playful payoff) + CTA

**DO:**
- Use innuendo and smart wordplay (like "purr", "vibe check", "turn yourself on")
- Normalize pleasure and confidence with humor
- Use humor to make taboo topics feel light and natural
- Sound like a cheeky best friend — bold, clever, and real about pleasure
- Be direct and confident (don't hedge or use weak language)
- Use short, punchy sentences

**DON'T:**
- ❌ NO "ignite", "unleash", "discover", "bliss", "embrace", "unlock" (overused!)
- ❌ NO crude or explicit terms
- ❌ NO medical brochure language ("enhance", "improve", "optimal")
- ❌ NO generic phrases ("your pleasure journey", "new heights", "inner goddess")
- ❌ NO weak phrases ("ready to", "are you", "want to")

### 🧠 Product Context
Product: {product_name}
Category: {product_category}
Creative Context: {context}

### 🪄 Your CTAs
{", ".join(MYMUSE_CTAS)}

### 🎯 Your Keywords
{", ".join(MYMUSE_KEYWORDS)}

### 🔥 Your Example Headlines
{chr(10).join(f'{i+1}. "{headline}"' for i, headline in enumerate(MYMUSE_EXAMPLE_HEADLINES))}

### 📝 Output Requirements
Generate **8 variants** of ad copy that sound like your examples above.

**CRITICAL - Each variant MUST include ALL THREE fields:**
1. **headline** - Punchy, surprising, cheeky (5-8 words max)
2. **subhead** - Playful payoff that expands the headline (10-15 words)
3. **cta** - ONE of your approved CTAs above

**Examples of complete variants:**
{{
"headline": "All Pussies Love MyMuse",
"subhead": "Because pleasure should purr, not roar.",
"cta": "Try it now"
}}

{{
"headline": "Turn Yourself On (Literally)",
"subhead": "Self-love just got a serious upgrade.",
"cta": "Discover your vibe"
}}

Output ONLY valid JSON array with ALL fields:
[
{{
"headline": "...",
"subhead": "...", 
"cta": "..."
}}
]
"""

def get_category_tone_new(category: str) -> MyMuseTone:
    """Get tone for category using new system"""
    category = category.lower().strip()
    for key, tone in CATEGORY_TONE.items():
        if key in category:
            return tone
    return MyMuseTone.PLAYFUL  # default fallback

def validate_brand_voice_new(text: str) -> dict:
    """Lightweight Brand Voice Validator"""
    issues = []
    for bad in MYMUSE_BRAND_TRAITS["avoid"]:
        if bad in text.lower():
            issues.append(f"Avoided word detected: {bad}")

    tone_score = sum(any(word in text.lower() for word in words) for words in LEXICON.values())
    score = min(100, 60 + tone_score * 5)

    return {"brand_voice_score": score, "issues": issues}
