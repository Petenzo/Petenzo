"""
MCP "Giełdy" — darmowy serwer MCP do analizy rynków krypto na ~100 giełdach.

Korzysta z biblioteki CCXT (publiczne API giełd, bez kluczy, za darmo).
Daje Claude'owi narzędzia: ceny, świece (wykres), orderbook, wskaźniki
techniczne (SMA/EMA/RSI/MACD/Bollinger), porównanie cen między giełdami
(arbitraż) i stawki funding rate na kontraktach perpetual.

Uruchomienie:  python server.py
"""
from __future__ import annotations

import asyncio
import math
from typing import Any

import ccxt.async_support as ccxt

try:  # mcp >= 2.0
    from mcp.server.mcpserver import MCPServer as _Server
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server

mcp = _Server(
    "gieldy",
    instructions=(
        "Darmowe dane rynkowe krypto z ~100 giełd (Binance, Bybit, OKX, Kraken, "
        "Coinbase, KuCoin, Gate, MEXC, Bitget...). Symbole w formacie 'BTC/USDT'. "
        "Kontrakty perpetual: 'BTC/USDT:USDT'. Interwały: 1m,5m,15m,1h,4h,1d,1w."
    ),
)

DEFAULT_EXCHANGES = ["binance", "bybit", "okx", "kraken", "coinbase", "kucoin", "gateio", "bitget", "mexc", "htx"]

_clients: dict[str, Any] = {}


async def _ex(name: str):
    name = name.lower().strip()
    if name not in ccxt.exchanges:
        raise ValueError(f"Nieznana giełda '{name}'. Użyj list_exchanges.")
    if name not in _clients:
        _clients[name] = getattr(ccxt, name)({"enableRateLimit": True, "timeout": 15000})
    return _clients[name]


# ---------------------------------------------------------------- wskaźniki
def _sma(v: list[float], n: int) -> float | None:
    return sum(v[-n:]) / n if len(v) >= n else None


def _ema_series(v: list[float], n: int) -> list[float]:
    if not v:
        return []
    k, out = 2 / (n + 1), [v[0]]
    for x in v[1:]:
        out.append(x * k + out[-1] * (1 - k))
    return out


def _rsi(v: list[float], n: int = 14) -> float | None:
    if len(v) <= n:
        return None
    gains = [max(v[i] - v[i - 1], 0) for i in range(1, len(v))]
    losses = [max(v[i - 1] - v[i], 0) for i in range(1, len(v))]
    ag, al = sum(gains[:n]) / n, sum(losses[:n]) / n
    for g, l in zip(gains[n:], losses[n:]):  # wygładzanie Wildera
        ag, al = (ag * (n - 1) + g) / n, (al * (n - 1) + l) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def _r(x: float | None, d: int = 6) -> float | None:
    return None if x is None else round(x, d)


# ---------------------------------------------------------------- narzędzia
@mcp.tool()
async def list_exchanges() -> dict:
    """Lista wszystkich obsługiwanych giełd (id do użycia w innych narzędziach)."""
    return {"count": len(ccxt.exchanges), "exchanges": ccxt.exchanges, "popular": DEFAULT_EXCHANGES}


@mcp.tool()
async def search_markets(exchange: str, query: str, limit: int = 30) -> list[dict]:
    """Szukaj par/rynków na giełdzie, np. query='SOL' zwróci SOL/USDT, SOL/USDT:USDT itd."""
    ex = await _ex(exchange)
    markets = await ex.load_markets()
    q = query.upper()
    hits = [
        {"symbol": m["symbol"], "type": m.get("type"), "active": m.get("active")}
        for m in markets.values()
        if q in m["symbol"].upper()
    ]
    return hits[:limit]


@mcp.tool()
async def get_ticker(symbol: str, exchange: str = "binance") -> dict:
    """Aktualna cena, bid/ask, zmiana 24h i wolumen dla pary na danej giełdzie."""
    ex = await _ex(exchange)
    t = await ex.fetch_ticker(symbol)
    return {k: t.get(k) for k in ("symbol", "last", "bid", "ask", "high", "low", "percentage", "baseVolume", "quoteVolume", "datetime")} | {"exchange": exchange}


@mcp.tool()
async def get_ohlcv(symbol: str, exchange: str = "binance", timeframe: str = "1h", limit: int = 100) -> dict:
    """Świece OHLCV (dane do wykresu): [czas, open, high, low, close, volume]."""
    ex = await _ex(exchange)
    candles = await ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=min(limit, 1000))
    return {
        "exchange": exchange, "symbol": symbol, "timeframe": timeframe,
        "columns": ["datetime", "open", "high", "low", "close", "volume"],
        "candles": [[ex.iso8601(c[0])] + c[1:] for c in candles],
    }


@mcp.tool()
async def get_orderbook(symbol: str, exchange: str = "binance", depth: int = 20) -> dict:
    """Orderbook (bids/asks), spread i nierównowaga popytu/podaży."""
    ex = await _ex(exchange)
    ob = await ex.fetch_order_book(symbol, limit=depth)
    bids, asks = ob["bids"][:depth], ob["asks"][:depth]
    bid_vol, ask_vol = sum(b[1] for b in bids), sum(a[1] for a in asks)
    best_bid, best_ask = (bids[0][0] if bids else None), (asks[0][0] if asks else None)
    spread = (best_ask - best_bid) if best_bid and best_ask else None
    return {
        "exchange": exchange, "symbol": symbol,
        "best_bid": best_bid, "best_ask": best_ask,
        "spread": spread, "spread_pct": _r(spread / best_ask * 100, 4) if spread else None,
        "bid_volume": bid_vol, "ask_volume": ask_vol,
        "imbalance": _r((bid_vol - ask_vol) / (bid_vol + ask_vol), 4) if bid_vol + ask_vol else None,
        "bids": bids, "asks": asks,
    }


@mcp.tool()
async def technical_analysis(symbol: str, exchange: str = "binance", timeframe: str = "1d", limit: int = 300) -> dict:
    """Analiza techniczna: SMA20/50/200, EMA12/26, RSI14, MACD, Bollinger, ATR14, trend i sygnały."""
    ex = await _ex(exchange)
    c = await ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=min(limit, 1000))
    if len(c) < 30:
        raise ValueError("Za mało świec do analizy (min. 30).")
    closes, highs, lows = [x[4] for x in c], [x[2] for x in c], [x[3] for x in c]
    price = closes[-1]

    ema12, ema26 = _ema_series(closes, 12), _ema_series(closes, 26)
    macd_line = [a - b for a, b in zip(ema12, ema26)]
    signal = _ema_series(macd_line, 9)
    sma20 = _sma(closes, 20)
    std20 = math.sqrt(sum((x - sma20) ** 2 for x in closes[-20:]) / 20)
    trs = [max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1])) for i in range(1, len(c))]
    atr = sum(trs[-14:]) / 14
    rsi = _rsi(closes)
    sma50, sma200 = _sma(closes, 50), _sma(closes, 200)

    signals = []
    if rsi is not None:
        signals.append("RSI wykupienie (>70)" if rsi > 70 else "RSI wyprzedanie (<30)" if rsi < 30 else "RSI neutralny")
    signals.append("MACD powyżej sygnału (byczo)" if macd_line[-1] > signal[-1] else "MACD poniżej sygnału (niedźwiedzio)")
    if sma50 and sma200:
        signals.append("Golden cross (SMA50>SMA200)" if sma50 > sma200 else "Death cross (SMA50<SMA200)")
    if price > sma20 + 2 * std20:
        signals.append("Cena nad górną wstęgą Bollingera")
    elif price < sma20 - 2 * std20:
        signals.append("Cena pod dolną wstęgą Bollingera")

    above = sum(1 for s in (sma20, sma50, sma200) if s and price > s)
    trend = {3: "silny wzrostowy", 2: "wzrostowy", 1: "spadkowy", 0: "silny spadkowy"}[above]

    return {
        "exchange": exchange, "symbol": symbol, "timeframe": timeframe, "candles": len(c),
        "price": price, "trend": trend,
        "change_pct": {"1": _r((price / closes[-2] - 1) * 100, 2), "7": _r((price / closes[-8] - 1) * 100, 2) if len(closes) > 8 else None, "30": _r((price / closes[-31] - 1) * 100, 2) if len(closes) > 31 else None},
        "sma": {"20": _r(sma20), "50": _r(sma50), "200": _r(sma200)},
        "ema": {"12": _r(ema12[-1]), "26": _r(ema26[-1])},
        "rsi14": _r(rsi, 2),
        "macd": {"macd": _r(macd_line[-1]), "signal": _r(signal[-1]), "histogram": _r(macd_line[-1] - signal[-1])},
        "bollinger": {"upper": _r(sma20 + 2 * std20), "middle": _r(sma20), "lower": _r(sma20 - 2 * std20)},
        "atr14": _r(atr), "atr_pct": _r(atr / price * 100, 2),
        "support_resistance": {"low_period": min(lows[-50:]), "high_period": max(highs[-50:])},
        "signals": signals,
        "note": "To nie jest porada inwestycyjna.",
    }


@mcp.tool()
async def compare_prices(symbol: str, exchanges: list[str] | None = None) -> dict:
    """Porównaj cenę pary na wielu giełdach naraz i znajdź różnicę (okazje arbitrażowe)."""
    names = exchanges or DEFAULT_EXCHANGES

    async def one(n: str):
        try:
            t = await (await _ex(n)).fetch_ticker(symbol)
            return {"exchange": n, "last": t.get("last"), "bid": t.get("bid"), "ask": t.get("ask"), "quoteVolume": t.get("quoteVolume")}
        except Exception as e:  # giełda może nie mieć pary albo być niedostępna
            return {"exchange": n, "error": type(e).__name__}

    rows = await asyncio.gather(*(one(n) for n in names))
    ok = [r for r in rows if r.get("bid") and r.get("ask")]
    result: dict[str, Any] = {"symbol": symbol, "prices": sorted(rows, key=lambda r: r.get("last") or 0)}
    if len(ok) >= 2:
        buy = min(ok, key=lambda r: r["ask"])
        sell = max(ok, key=lambda r: r["bid"])
        result["best_buy"] = {"exchange": buy["exchange"], "ask": buy["ask"]}
        result["best_sell"] = {"exchange": sell["exchange"], "bid": sell["bid"]}
        result["gross_spread_pct"] = _r((sell["bid"] / buy["ask"] - 1) * 100, 4)
        result["note"] = "Brutto — bez opłat transakcyjnych, wypłat i czasu transferu."
    return result


@mcp.tool()
async def funding_rates(symbol: str = "BTC/USDT:USDT", exchanges: list[str] | None = None) -> dict:
    """Funding rate kontraktów perpetual na kilku giełdach (np. 'ETH/USDT:USDT')."""
    names = exchanges or ["binance", "bybit", "okx", "bitget", "gateio", "mexc"]

    async def one(n: str):
        try:
            ex = await _ex(n)
            if not ex.has.get("fetchFundingRate"):
                return {"exchange": n, "error": "brak wsparcia"}
            f = await ex.fetch_funding_rate(symbol)
            rate = f.get("fundingRate")
            return {"exchange": n, "funding_rate_pct": _r(rate * 100, 5) if rate is not None else None,
                    "next_funding": f.get("fundingDatetime"), "mark_price": f.get("markPrice")}
        except Exception as e:
            return {"exchange": n, "error": type(e).__name__}

    return {"symbol": symbol, "rates": await asyncio.gather(*(one(n) for n in names))}


@mcp.tool()
async def top_movers(exchange: str = "binance", quote: str = "USDT", limit: int = 10, min_volume: float = 1_000_000) -> dict:
    """Największe wzrosty i spadki 24h na giełdzie (pary spot z wolumenem >= min_volume w walucie quote)."""
    ex = await _ex(exchange)
    await ex.load_markets()
    tickers = await ex.fetch_tickers()
    rows = [
        {"symbol": s, "last": t.get("last"), "change_pct": t.get("percentage"), "quoteVolume": t.get("quoteVolume")}
        for s, t in tickers.items()
        if s.endswith(f"/{quote}") and t.get("percentage") is not None and (t.get("quoteVolume") or 0) >= min_volume
    ]
    rows.sort(key=lambda r: r["change_pct"])
    return {"exchange": exchange, "gainers": rows[::-1][:limit], "losers": rows[:limit]}


if __name__ == "__main__":
    mcp.run()
