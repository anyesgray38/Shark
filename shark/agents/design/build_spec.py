"""Build a Penpot-ready design specification from validated requirements."""
from .penpot_adapter import PenpotState


def build_spec(name: str, purpose: str, surfaces: list[str], components: list[str] | None = None):
    if not name.strip() or not purpose.strip():
        raise ValueError("name and purpose are required")
    return {
        "name": name.strip(),
        "purpose": purpose.strip(),
        "state": PenpotState.DESIGN_SPEC_ONLY.value,
        "surfaces": surfaces,
        "components": components or [],
        "tokens": ["color", "spacing", "typography", "radius", "shadow", "motion"],
        "implementation_notes": [
            "Use reusable components and variants.",
            "Preserve semantic status and confidence states.",
            "Do not visually overstate unvalidated research findings."
        ]
    }
