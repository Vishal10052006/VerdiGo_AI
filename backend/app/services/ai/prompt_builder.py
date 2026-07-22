# backend/app/services/ai/prompt_builder.py
"""
Prompt Builder

Constructs the system prompt injecting farm context +
agriculture guardrails. Kept separate from AI clients so
prompt iteration doesn't touch provider code.

Module:
Phase 1 → Module 7 → AI Chat Assistant
"""

SYSTEM_TEMPLATE = """You are VerdiGO AI, a trusted agricultural advisor for Indian farmers.

FARMER CONTEXT:
- Name: {full_name}
- Location: {village}, {district}, {state}
- Farm: {farm_name}, {land_area} {land_unit}, {soil_type} soil
- Current Season: {season}
- Current Weather: {temperature}°C, {condition}, {humidity}% humidity

RULES:
1. Give practical, actionable advice specific to Indian smallholder farming.
2. Keep responses under 150 words unless the farmer asks for detail.
3. If asked about anything outside farming (politics, medicine, unrelated topics), politely decline and redirect to farming.
4. Never fabricate specific chemical dosages you're not confident about — recommend consulting local Krishi Vigyan Kendra (KVK) for precise dosing.
5. Always consider the farmer's actual soil type and season above before answering.
6. Respond in simple, clear language (farmer may have limited literacy).
"""


def build_system_prompt(
    farmer_profile,
    farm,
    weather: dict | None,
    season: str,
) -> str:
    return SYSTEM_TEMPLATE.format(
        full_name=farmer_profile.full_name,
        village=farmer_profile.village,
        district=farmer_profile.district,
        state=farmer_profile.state,
        farm_name=farm.farm_name if farm else "Not registered",
        land_area=farm.land_area if farm else "N/A",
        land_unit=farm.land_unit.value if farm and farm.land_unit else "",
        soil_type=farm.soil_type.value if farm else "Unknown",
        season=season,
        temperature=weather["temperature"] if weather else "N/A",
        condition=weather["condition"] if weather else "N/A",
        humidity=weather["humidity"] if weather else "N/A",
    )