class Asset:
    """
    Représente un actif financier avec son historique de prix.
   
    Pattern de conception : COMPOSITION
    ───────────────────────────────────
    Asset POSSÈDE une PriceSeries (relation HAS-A, pas IS-A).
   
    Le cycle de vie de PriceSeries est lié à celui de Asset :
    - Créé quand Asset est créé
    - Détruit quand Asset est détruit
   
    Attributes:
        ticker: Ticker (ex: 'AAPL')
        prices: Instance PriceSeries contenant l'historique (COMPOSÉE)
        sector: Classification sectorielle
        currency: Devise des prix (défaut: USD)
    """
   
    def __init__(
        self,
        ticker: str,
        prices: PriceSeries,
        sector: str | None = None,
        currency: CurrencyEnum = CurrencyEnum.USD
    ) -> None:
        """
        Initialise un Asset.
       
        Args:
            ticker: Symbole boursier (ne peut pas être vide)
            prices: Série de prix (ne peut pas être vide)
            sector: Secteur d'activité (optionnel)
            currency: Devise (défaut: USD)
       
        Raises:
            ValueError: Si ticker est vide ou prices est vide
        """
        # Validation des entrées dans le constructeur
        if not ticker or not ticker.strip():
            raise ValueError("Le ticker ne peut pas être vide")
        if len(prices) == 0:
            raise ValueError("La série de prix ne peut pas être vide")
       
        self.ticker = ticker.upper()  # Normalisation en majuscules
        self.prices = prices  # Composition : Asset POSSÈDE une PriceSeries
        self.sector = sector
        self.currency = currency
   
    def __repr__(self) -> str:
        """Représentation pour le développement."""
        return f"Asset({self.ticker!r}, {len(self.prices)} prices)"
   
    def __str__(self) -> str:
        """Représentation pour l'utilisateur."""
        return f"{self.ticker}: ${self.current_price:.2f}"