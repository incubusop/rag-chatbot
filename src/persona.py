# src/persona.py
import re

def extract_persona(messages):
    persona = {"habits": [], "personal_facts": [], 
               "personality": [], "communication_style": []}
    for msg in messages:
        m = msg.lower()
        # Habits
        if "sleep" in m or "bed" in m:
            persona["habits"].append("mentions sleep")
        if "gym" in m or "workout" in m:
            persona["habits"].append("fitness-oriented")
        if "coffee" in m:
            persona["habits"].append("likes coffee")
        # Personal facts
        mo = re.search(r"moving to ([A-Za-z ,]+)", m)
        if mo:
            persona["personal_facts"].append("moving to " + mo.group(1))
        mfav = re.search(r"favorite (?:food|place|book) is ([\w\s]+)", m)
        if mfav:
            persona["personal_facts"].append("likes " + mfav.group(1).strip())
        # Personality
        if "lol" in m or "haha" in m or "😂" in m:
            persona["personality"].append("funny")
        if "sorry" in m or "thank you" in m:
            persona["personality"].append("polite")
        # Communication style
        if len(msg) < 15:
            persona["communication_style"].append("short messages")
        if "?" in msg:
            persona["communication_style"].append("asks questions")
    # Deduplicate
    for k in persona:
        persona[k] = sorted(set(persona[k]))
    return persona
