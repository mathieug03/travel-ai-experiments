"""Generate affiliate booking URLs for various partners."""

from urllib.parse import quote


def trainline_url(origin: str, destination: str, date: str) -> str:
    """Build a Trainline affiliate redirect URL."""
    base = "https://www.thetrainline.com/book/results"
    return f"{base}?origin={quote(origin)}&destination={quote(destination)}&outwardDate={date}"


def booking_com_url(city: str, check_in: str, check_out: str) -> str:
    """Build a Booking.com affiliate URL."""
    base = "https://www.booking.com/searchresults.html"
    return f"{base}?ss={quote(city)}&checkin={check_in}&checkout={check_out}"


def get_your_guide_url(city: str) -> str:
    """Build a GetYourGuide affiliate URL."""
    base = "https://www.getyourguide.com/s/"
    return f"{base}?q={quote(city)}"
