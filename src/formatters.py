def format_duration(duration: int) -> str:
    hours = duration // 60
    minutes = duration % 60
    if duration < 60:
        return f"{duration}m"
    if duration == 60:
        return f"{hours}h"
    return f"{hours}h {minutes}m"


def format_price(price: float) -> str:
    return f"${price:,.2f} MXN p/p"
