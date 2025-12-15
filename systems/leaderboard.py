"""
Systém pro správu žebříčků hráčů.

Ukládá výsledky hráčů do JSON souborů podle obtížnosti
a poskytuje metody pro čtení a řazení nejlepších výsledků.
Žebříčky se řadí primárně podle doby hraní, sekundárně podle skóre, terciárně podle přesnosti.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


LEADERBOARDS_DIR = Path("leaderboards")
DIFFICULTIES = ["Lama", "Machr", "Superman"]


def ensure_leaderboards_dir():
    """Vytvoří adresář pro žebříčky, pokud neexistuje."""
    LEADERBOARDS_DIR.mkdir(exist_ok=True)


def get_leaderboard_path(difficulty: str) -> Path:
    """Vrátí cestu k souboru žebříčku pro danou obtížnost."""
    filename = difficulty.lower() + ".json"
    return LEADERBOARDS_DIR / filename


def save_result(
    difficulty: str,
    player_name: str,
    score: int,
    shoots: int,
    accuracy: int,
    game_duration_ms: int,
    game_start_datetime: str,
):
    """
    Uloží výsledek hráče do žebříčku dané obtížnosti.
    
    Args:
        difficulty: Obtížnost (Lama, Machr, Superman)
        player_name: Jméno hráče
        score: Dosažené skóre
        shoots: Počet výstřelů
        accuracy: Procento přesnosti
        game_duration_ms: Doba hraní v milisekundách
        game_start_datetime: ISO formát data/času startu hry
    """
    ensure_leaderboards_dir()
    
    path = get_leaderboard_path(difficulty)
    
    # Načti existující výsledky
    results = []
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                results = json.load(f)
        except (json.JSONDecodeError, IOError):
            results = []
    
    # Přidej nový výsledek
    result = {
        "name": player_name,
        "score": score,
        "shoots": shoots,
        "accuracy": accuracy,
        "game_duration_ms": game_duration_ms,
        "game_start_datetime": game_start_datetime,
    }
    results.append(result)
    
    # Ulož zpět
    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def get_leaderboard(difficulty: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Vrátí seznam nejlepších výsledků pro danou obtížnost.
    
    Řadí primárně podle doby hraní (delší je lepší),
    sekundárně podle skóre, terciárně podle přesnosti.
    
    Args:
        difficulty: Obtížnost (Lama, Machr, Superman)
        limit: Maximální počet výsledků
        
    Returns:
        Seznam výsledků řazených od nejlepšího
    """
    ensure_leaderboards_dir()
    
    path = get_leaderboard_path(difficulty)
    
    if not path.exists():
        return []
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            results = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    
    # Řaď podle doby hraní (sestupně), pak skóre (sestupně), pak přesnosti (sestupně)
    sorted_results = sorted(
        results,
        key=lambda x: (
            -x.get("game_duration_ms", 0),  # Negativní pro sestupné řazení
            -x.get("score", 0),
            -x.get("accuracy", 0),
        ),
    )
    
    return sorted_results[:limit]

