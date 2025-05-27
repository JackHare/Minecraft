from typing import Dict, List, Tuple, Any
from world.Block import OAK_LOG, COBBLE_STONE, OAK_PLANK, STONE, IRON, IRON_BLOCK, GOLD, GOLD_BLOCK, DIAMOND_BLOCK, \
    DIAMOND, COAL, COAL_BLOCK

# Recipe format: {
#   "name": "Recipe Name",
#   "inputs": {block_type: quantity, ...},
#   "output": (block_type, quantity)
# }

RECIPES = [
    {
        "name": "Oak Planks",
        "inputs": {OAK_LOG: 1},
        "output": (OAK_PLANK, 4)
    },
    {
        "name": "Stone",
        "inputs": {COBBLE_STONE: 1},
        "output": (STONE, 1)
    },
    {
        "name": "Iron Block",
        "inputs": {IRON: 9},
        "output": (IRON_BLOCK, 1)
    },
{
        "name": "Gold Block",
        "inputs": {GOLD: 9},
        "output": (GOLD_BLOCK, 1)
    },
{
        "name": "Diamond Block",
        "inputs": {DIAMOND: 9},
        "output": (DIAMOND_BLOCK, 1)
    },
{
        "name": "Coal Block",
        "inputs": {COAL: 9},
        "output": (COAL_BLOCK, 1)
    }
]

def can_craft(recipe: Dict, inventory: Any) -> bool:
    """
    Check if a recipe can be crafted with the current inventory.

    Args:
        recipe: The recipe to check
        inventory: The player's inventory

    Returns:
        True if the recipe can be crafted, False otherwise
    """
    for block_type, quantity in recipe["inputs"].items():
        if not inventory.has_block(block_type) or inventory.get_block_count(block_type) < quantity:
            return False
    return True

def craft_item(recipe: Dict, inventory: Any) -> bool:
    """
    Craft an item by consuming the required materials and adding the result.

    Args:
        recipe: The recipe to craft
        inventory: The player's inventory

    Returns:
        True if crafting was successful, False otherwise
    """
    # Check if we can craft this recipe
    if not can_craft(recipe, inventory):
        return False

    # Consume the input materials
    for block_type, quantity in recipe["inputs"].items():
        inventory.remove_block(block_type, quantity)

    # Add the crafted item to the inventory
    output_type, output_quantity = recipe["output"]
    inventory.add_block(output_type, output_quantity)

    return True

def get_available_recipes(inventory: Any) -> List[Dict]:
    """
    Get a list of recipes that can be crafted with the current inventory.

    Args:
        inventory: The player's inventory

    Returns:
        A list of recipes that can be crafted
    """
    return [recipe for recipe in RECIPES if can_craft(recipe, inventory)]

def get_all_recipes() -> List[Dict]:
    """
    Get a list of all available recipes.

    Returns:
        A list of all recipes
    """
    return RECIPES
