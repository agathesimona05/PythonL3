from pyvest.src.priceseries import PriceSeries
from pyvest.src.asset import Asset
from pyvest.src.loader import DataLoader
from pyvest.src.universe import Universe

# On instancie un "loader" à partir du DataLoader avec système de cache
loader = DataLoader(cache_dir=".cache")

# Récupération des données pour un actif via l'API Yahoo Finance
apple_ts = loader.fetch_single_ticker("AAPL", "Close", ("2024-01-01", "2024-12-01"))

# Test du système de cache (le second appel devrait être instantané)
apple_ts = loader.fetch_single_ticker("AAPL", "Close", ("2024-01-01", "2024-12-01"))

# Création de nos objets Asset
apple = Asset("AAPL", apple_ts, sector="Technology")
msft = Asset("MSFT", loader.fetch_single_ticker("MSFT", "Close", ("2024-01-01", "2024-12-01")), sector="Technology")

# Communication entre Asset et son interface PriceSeries
print(f"Volatilité AAPL: {apple.volatility:.2%}")

# Corrélation entre deux actifs
correlation = apple.correlation_with(msft)
print(f"Corrélation AAPL-MSFT: {correlation:.2f}")

# Agrégation dans un objet Universe
universe = Universe([apple, msft])
for asset in universe:
    print(f"{asset.ticker}: {asset.total_return:.2%}")