DEFAULT_ITEMS = {
    "EXC-001": ("Earth excavation", "m³"),
    "CON-001": ("Plain cement concrete", "m³"),
    "RCC-001": ("Reinforced cement concrete", "m³"),
    "MASON-001": ("Brick masonry", "m³"),
    "PLS-001": ("Cement plaster", "m²"),
    "FLR-001": ("Floor finish / tiles", "m²"),
    "FORM-001": ("Formwork", "m²"),
    "REBAR-001": ("Reinforcement steel", "kg"),
}

def calculate_item(item_code, **kwargs):
    """Deterministic calculation engine. AI should call/describe this engine,
    not invent engineering arithmetic."""
    if item_code == "EXC-001":
        return kwargs["length"] * kwargs["width"] * kwargs["depth"]
    if item_code in {"CON-001", "RCC-001"}:
        return kwargs["length"] * kwargs["width"] * kwargs["depth"]
    if item_code == "MASON-001":
        return kwargs["length"] * kwargs["height"] * kwargs["thickness"]
    if item_code in {"PLS-001", "FLR-001"}:
        return kwargs["length"] * kwargs["width"]
    if item_code == "FORM-001":
        return kwargs["area"]
    if item_code == "REBAR-001":
        # Weight per metre = d² / 162 kg/m
        return kwargs["diameter"] ** 2 / 162 * kwargs["length"]
    raise ValueError("Unknown calculation item.")
