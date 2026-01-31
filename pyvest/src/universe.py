from pyvest.core.asset import Asset
from typing import Iterator


class Universe:
    """
    Collection d'actifs représentant un univers d'investissement.
    
    Pattern de conception : AGRÉGATION
    ──────────────────────────────────
    Universe CONTIENT des Asset, mais les Asset peuvent exister 
    indépendamment de l'Universe.
    
    La classe implémente le protocole d'itération (__iter__) et
    de conteneur (__contains__, __len__) pour une utilisation
    pythonique.
    """
    
    def __init__(self, assets: list[Asset] | None = None) -> None:
        self._assets: dict[str, Asset] = {}. 'tu crées le dictionnaire'
        if assets:
            for asset in assets:
                self.add(asset)
    
    def add(self, asset: Asset) -> None:
        """Ajoute un actif à l'univers."""
        self._assets[asset.ticker.upper()] = asset
        
    
    def get(self, ticker: str) -> Asset | None:
        """Récupère un actif par son ticker."""
        return self._assets.get(ticker.upper())
        
    
    def remove(self, ticker: str) -> Asset | None:
        """Retire un actif de l'univers."""
        return self._assets.pop(ticker.upper(), None)
    
    def __len__(self) -> int:
        return len(self._assets)
       
    
    def __iter__(self) -> Iterator[Asset]:
        return iter(self._assets.values())
    
    def __contains__(self, ticker: str) -> bool:
        return ticker.upper() in self._assets

    
    @property
    def tickers(self) -> list[str]:
        return list(self._assets.keys())

    
    def filter_by_sector(self, sector: str) -> list[Asset]:
        """Filtre les actifs par secteur."""
        s = sector.strip().lower()
        return [asset for asset in self._assets.values()if asset.sector is not None and asset.sector.strip().lower() == s]
  
from itertools import combinations


def top_k_correlations(
    assets: list[Asset],k: int = 20,use_absolute: bool = False) -> list[tuple[str, str, float]]:
    """
    Extrait les K paires les plus corrélées d'une liste d'actifs
    sur la base de la corrélation de Pearson.
    
    Args:
        assets:
        k: Nombre de paires
        use_absolute: Si True, trie par |corrélation| pour capturer aussi les fortes corrélations négatives
    
    Returns:
        Liste de tuples (ticker_1, ticker_2, corrélation) triée
        par corrélation décroissante
    """
    correlations = []
    
    # itertools.combinations génère toutes les paires uniques
    # évitant les doublons (A,B) et (B,A) et les auto-corrélations (A,A)
    for asset_1, asset_2 in combinations(assets, 2):
        try:
            corr = asset_1.correlation_with(asset_2)
        except ValueError:
            # Pas assez de données communes / variance nulle / etc.
            continue

        correlations.append((asset_1.ticker, asset_2.ticker, corr))
    
    # Trier par corrélation (ou valeur absolue) et retourner les k premières
    key_fn = (lambda t: abs(t[2])) if use_absolute else (lambda t: t[2])
    correlations.sort(key=key_fn, reverse=True)

    return correlations[:k]

    import pandas as pd
import numpy as np
from itertools import combinations


def build_correlation_matrix(assets: list[Asset]) -> pd.DataFrame:
    """
    Construit une matrice de corrélation pour tous les actifs.
    
    Returns:
        DataFrame symétrique avec tickers en index et colonnes
    """
    tickers = [a.ticker for a in assets]
    n = len(tickers)
    
    # Initialiser la matrice avec NaN
    matrix = np.full((n, n), np.nan)
    
    # Pre-remplir la diagonale avec 1.0
    np.fill_diagonal(matrix, 1.0)
    
    # Créer un mapping ticker -> index pour un accès rapide O(1)
    ticker_to_idx = {t: i for i, t in enumerate(tickers)}
    
    # Remplir le triangle supérieur et inférieur (symétrie)
    # Votre code ici
    
    return pd.DataFrame(matrix, index=tickers, columns=tickers)


def extract_upper_triangle(corr_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Extrait les paires uniques du triangle supérieur de la matrice.
    
    Utile pour éviter les doublons (AAPL-MSFT et MSFT-AAPL) et
    exclure la diagonale (auto-corrélations).
    
    Cette méthode est similaire à celle utilisée dans le projet
    "Global Multi-Asset Correlation Lab".
    
    Args:
        corr_matrix: Matrice de corrélation (DataFrame carré)
    
    Returns:
        DataFrame avec colonnes ['asset_1', 'asset_2', 'correlation']
        trié par corrélation décroissante
    """
    # Créer un masque pour le triangle supérieur (excluant la diagonale k=1)
    mask = np.triu(np.ones(corr_matrix.shape, dtype=bool), k=1)
    
    for asset_1, asset_2 in combinations(assets, 2):
        i = ticker_to_idx[asset_1.ticker]
        j = ticker_to_idx[asset_2.ticker]

        try:
            corr = asset_1.correlation_with(asset_2)
        except ValueError:
            # Pas assez de données / variance nulle
            continue

        # Symétrie de la matrice
        matrix[i, j] = corr
        matrix[j, i] = corr