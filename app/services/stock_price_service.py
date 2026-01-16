import yfinance as yf
from typing import Optional, Dict, List
from datetime import datetime, timedelta

class StockPriceService:
    """Service for fetching real-time stock prices from Yahoo Finance"""
    
    # Cache for stock prices (simple in-memory cache)
    _price_cache: Dict[str, Dict] = {}
    _cache_duration = timedelta(minutes=5)  # Cache for 5 minutes
    
    @staticmethod
    def get_current_price(symbol: str) -> Optional[float]:
        """
        Get current stock price for a given symbol
        
        Args:
            symbol: Stock ticker symbol (e.g., AAPL, GOOGL)
            
        Returns:
            Current price as float, or None if not found
        """
        try:
            # Check cache first
            cached_data = StockPriceService._get_from_cache(symbol)
            if cached_data:
                print(f"Retrieved price for {symbol} from cache: ${cached_data['price']}")
                return cached_data['price']
            
            # Fetch from Yahoo Finance
            print(f"Fetching current price for {symbol} from Yahoo Finance")
            ticker = yf.Ticker(symbol)
            
            # Get current price
            info = ticker.info
            current_price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if current_price:
                # Cache the result
                StockPriceService._save_to_cache(symbol, current_price, info)
                print(f"Retrieved price for {symbol}: ${current_price}")
                return float(current_price)
            else:
                print(f"Warning: No price found for symbol: {symbol}")
                return None
                
        except Exception as e:
            print(f"Error fetching price for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def get_stock_info(symbol: str) -> Optional[Dict]:
        """
        Get detailed stock information
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            Dictionary with stock information
        """
        try:
            # Check cache
            cached_data = StockPriceService._get_from_cache(symbol)
            if cached_data and 'info' in cached_data:
                print(f"Retrieved info for {symbol} from cache")
                return cached_data['info']
            
            print(f"Fetching detailed info for {symbol}")
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            stock_info = {
                'symbol': symbol,
                'name': info.get('longName') or info.get('shortName'),
                'current_price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'previous_close': info.get('previousClose'),
                'open': info.get('open'),
                'day_high': info.get('dayHigh'),
                'day_low': info.get('dayLow'),
                'volume': info.get('volume'),
                'market_cap': info.get('marketCap'),
                'currency': info.get('currency', 'USD'),
                'exchange': info.get('exchange'),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
            }
            
            # Cache the result
            if stock_info['current_price']:
                StockPriceService._save_to_cache(symbol, stock_info['current_price'], stock_info)
            
            print(f"Retrieved info for {symbol}")
            return stock_info
            
        except Exception as e:
            print(f"Error fetching info for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def get_historical_prices(
        symbol: str, 
        period: str = "1mo"
    ) -> Optional[List[Dict]]:
        """
        Get historical stock prices
        
        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            List of dictionaries with historical data
        """
        try:
            print(f"Fetching historical data for {symbol} (period: {period})")
            ticker = yf.Ticker(symbol)
            
            # Get historical data
            hist = ticker.history(period=period)
            
            if hist.empty:
                print(f"Warning: No historical data found for {symbol}")
                return None
            
            # Convert to list of dictionaries
            historical_data = []
            for date, row in hist.iterrows():
                historical_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'close': round(row['Close'], 2),
                    'volume': int(row['Volume'])
                })
            
            print(f"Retrieved {len(historical_data)} historical records for {symbol}")
            return historical_data
            
        except Exception as e:
            print(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        Validate if a stock symbol exists
        
        Args:
            symbol: Stock ticker symbol
            
        Returns:
            True if valid, False otherwise
        """
        try:
            price = StockPriceService.get_current_price(symbol)
            return price is not None
        except Exception:
            return False
    
    @staticmethod
    def _get_from_cache(symbol: str) -> Optional[Dict]:
        """Get price from cache if not expired"""
        if symbol in StockPriceService._price_cache:
            cached = StockPriceService._price_cache[symbol]
            if datetime.now() - cached['timestamp'] < StockPriceService._cache_duration:
                return cached
            else:
                # Cache expired, remove it
                del StockPriceService._price_cache[symbol]
        return None
    
    @staticmethod
    def _save_to_cache(symbol: str, price: float, info: Dict):
        """Save price to cache with timestamp"""
        StockPriceService._price_cache[symbol] = {
            'price': price,
            'info': info,
            'timestamp': datetime.now()
        }
    
    @staticmethod
    def clear_cache():
        """Clear the entire price cache"""
        StockPriceService._price_cache.clear()
        print("Stock price cache cleared")
