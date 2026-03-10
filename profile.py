from datetime import datetime


def get_zodiac(birth_date: str):
    """
    Determine zodiac sign from birth date
    Format: YYYY-MM-DD
    """

    date = datetime.strptime(birth_date, "%Y-%m-%d")
    day = date.day
    month = date.month

    zodiac_dates = [
        ((3, 21), (4, 19), "Aries"),
        ((4, 20), (5, 20), "Taurus"),
        ((5, 21), (6, 20), "Gemini"),
        ((6, 21), (7, 22), "Cancer"),
        ((7, 23), (8, 22), "Leo"),
        ((8, 23), (9, 22), "Virgo"),
        ((9, 23), (10, 22), "Libra"),
        ((10, 23), (11, 21), "Scorpio"),
        ((11, 22), (12, 21), "Sagittarius"),
        ((12, 22), (1, 19), "Capricorn"),
        ((1, 20), (2, 18), "Aquarius"),
        ((2, 19), (3, 20), "Pisces"),
    ]

    for start, end, sign in zodiac_dates:
        if (month == start[0] and day >= start[1]) or (
            month == end[0] and day <= end[1]
        ):
            return sign

    return "Unknown"


def build_user_profile(user_profile: dict):

    zodiac = get_zodiac(user_profile["birth_date"])

    return {
        "name": user_profile["name"],
        "zodiac": zodiac,
        "birth_place": user_profile["birth_place"],
        "preferred_language": user_profile.get("preferred_language", "en"),
    }