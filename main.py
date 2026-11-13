from bakery import assert_equal
from drafter import *
from dataclasses import dataclass

set_site_information(
    author="Thomas Pollutri (pollutri@udel.edu)",
    description="""A website that helps fishermen find the closest
    fishing spot for the kind of fish they want to catch. The user enters
    a ZIP code, picks a fish type, and gets a list of the nearest spots
    with a Google Maps link.""",
    sources=["Official Drafter documentation",
             "Fishing spot locations and fish types are approximate and "
             "based on Delaware state park and DNREC public information"],
    planning=["Pick_a_Problem.pdf", "Design.pdf"],
    links=["https://github.com/tpollpy/Fishing-Spot-Finder"]
)
hide_debug_information()
set_website_title("Fishing Spot Finder")
set_website_framed(False)



# Global constants 


# The fish types the user can pick from in the SelectBox
FISH_TYPES = ["Largemouth Bass", "Smallmouth Bass", "Trout", "Catfish",
              "Bluegill", "Crappie", "Striped Bass"]

# Each ZIP code we know about, mapped to [latitude, longitude]
ZIP_LOCATIONS = {
    "19711": [39.684, -75.746],
    "19716": [39.679, -75.752],
    "19702": [39.623, -75.696],
    "19701": [39.591, -75.700],
    "19709": [39.449, -75.716],
    "19720": [39.668, -75.589],
    "19801": [39.737, -75.550],
    "19803": [39.800, -75.545],
    "19901": [39.158, -75.524],
    "19963": [38.913, -75.428],
    "19973": [38.641, -75.611],
    "19958": [38.774, -75.139],
    "19971": [38.720, -75.076],
    "19703": [39.800, -75.460],
    "19706": [39.577, -75.592],
    "19707": [39.787, -75.684],
    "19713": [39.667, -75.712],
    "19730": [39.457, -75.660],
    "19734": [39.395, -75.691],
    "19802": [39.756, -75.533],
    "19804": [39.717, -75.613],
    "19805": [39.744, -75.592],
    "19806": [39.758, -75.563],
    "19807": [39.792, -75.611],
    "19808": [39.734, -75.666],
    "19809": [39.759, -75.500],
    "19810": [39.819, -75.506],
    "19904": [39.170, -75.580],
    "19930": [38.539, -75.060],
    "19933": [38.742, -75.604],
    "19934": [39.100, -75.530],
    "19938": [39.250, -75.680],
    "19939": [38.548, -75.245],
    "19940": [38.456, -75.577],
    "19943": [39.010, -75.580],
    "19944": [38.462, -75.051],
    "19947": [38.690, -75.385],
    "19950": [38.810, -75.590],
    "19952": [38.923, -75.578],
    "19956": [38.556, -75.571],
    "19962": [39.070, -75.480],
    "19966": [38.590, -75.290],
    "19968": [38.777, -75.310],
    "19970": [38.545, -75.090],
    "19975": [38.460, -75.220],
    "19977": [39.298, -75.605]
}

# Roughly how many miles are in one degree of latitude / longitude
# (longitude miles are for Delaware's latitude)
MILES_PER_LAT_DEGREE = 69.0
MILES_PER_LON_DEGREE = 53.0

# Only spots within this many miles of the user count as "nearby"
MAX_MILES = 25.0



# Dataclasses


@dataclass
class FishingSpot:
    name: str
    latitude: float
    longitude: float
    fish_types: list[str]
    public_access: bool
    distance: float


@dataclass
class State:
    zip_code: str
    fish_type: str
    spots: list[FishingSpot]
    favorites: list[FishingSpot]
    selected_spot: str



# Helper functions


def all_spots() -> list[FishingSpot]:
    """
    Makes a fresh list of every fishing spot the site knows about.
    The distance starts at 0.0 and is calculated during a search.

    Args:
        None

    Returns:
        list[FishingSpot]: every fishing spot on file
    """
    return [
        FishingSpot("Lums Pond State Park", 39.558, -75.728,
                    ["Largemouth Bass", "Bluegill", "Catfish", "Crappie"],
                    True, 0.0),
        FishingSpot("White Clay Creek State Park", 39.733, -75.765,
                    ["Trout", "Smallmouth Bass"], True, 0.0),
        FishingSpot("Becks Pond", 39.640, -75.712,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0),
        FishingSpot("Brandywine Creek State Park", 39.812, -75.578,
                    ["Trout", "Smallmouth Bass"], True, 0.0),
        FishingSpot("Hoopes Reservoir", 39.775, -75.640,
                    ["Largemouth Bass", "Crappie"], False, 0.0),
        FishingSpot("C&D Canal", 39.560, -75.640,
                    ["Striped Bass", "Catfish"], True, 0.0),
        FishingSpot("Garrisons Lake", 39.240, -75.600,
                    ["Largemouth Bass", "Catfish", "Bluegill"], True, 0.0),
        FishingSpot("Silver Lake (Dover)", 39.172, -75.525,
                    ["Largemouth Bass", "Bluegill", "Crappie"], True, 0.0),
        FishingSpot("Killens Pond State Park", 38.986, -75.546,
                    ["Largemouth Bass", "Catfish", "Crappie", "Bluegill"],
                    True, 0.0),
        FishingSpot("Indian River Inlet", 38.609, -75.064,
                    ["Striped Bass"], True, 0.0),
        FishingSpot("Trap Pond State Park", 38.528, -75.479,
                    ["Largemouth Bass", "Bluegill", "Crappie"], True, 0.0),
        FishingSpot("Bellevue State Park", 39.775, -75.495,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0),
        FishingSpot("Red Clay Creek", 39.795, -75.660,
                    ["Trout"], True, 0.0),
        FishingSpot("Mill Creek", 39.770, -75.700,
                    ["Trout"], True, 0.0),
        FishingSpot("Pike Creek", 39.735, -75.705,
                    ["Trout"], True, 0.0),
        FishingSpot("Battery Park (New Castle)", 39.657, -75.561,
                    ["Striped Bass", "Catfish"], True, 0.0),
        FishingSpot("Fort DuPont State Park", 39.573, -75.585,
                    ["Striped Bass", "Catfish"], True, 0.0),
        FishingSpot("Augustine Beach", 39.502, -75.578,
                    ["Striped Bass", "Catfish"], True, 0.0),
        FishingSpot("Noxontown Pond", 39.430, -75.690,
                    ["Largemouth Bass", "Crappie", "Bluegill"], True, 0.0),
        FishingSpot("Lake Como (Smyrna)", 39.296, -75.611,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0),
        FishingSpot("Moores Lake", 39.130, -75.540,
                    ["Largemouth Bass", "Crappie", "Bluegill"], True, 0.0),
        FishingSpot("Haven Lake (Milford)", 38.906, -75.435,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0),
        FishingSpot("Wagamons Pond (Milton)", 38.775, -75.311,
                    ["Largemouth Bass", "Bluegill", "Crappie"], True, 0.0),
        FishingSpot("Hearns Pond (Seaford)", 38.660, -75.613,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0),
        FishingSpot("Records Pond (Laurel)", 38.555, -75.570,
                    ["Largemouth Bass", "Crappie", "Catfish"], True, 0.0),
        FishingSpot("Cape Henlopen Fishing Pier", 38.785, -75.095,
                    ["Striped Bass"], True, 0.0)
    ]


def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """
    Estimates the distance in miles between two map points using the
    distance formula, rounded to 1 decimal place.

    Args:
        lat1 (float): latitude of the first point
        lon1 (float): longitude of the first point
        lat2 (float): latitude of the second point
        lon2 (float): longitude of the second point

    Returns:
        float: the distance in miles
    """
    north_south = (lat2 - lat1) * MILES_PER_LAT_DEGREE
    east_west = (lon2 - lon1) * MILES_PER_LON_DEGREE
    miles = (north_south ** 2 + east_west ** 2) ** 0.5
    return round(miles, 1)


def spot_matches(spot: FishingSpot, fish_type: str,
                 public_only: bool) -> bool:
    """
    Checks if a spot has the chosen fish, and (if the user only wants
    public spots) that the spot has public access.

    Args:
        spot (FishingSpot): the spot being checked
        fish_type (str): the fish the user is looking for
        public_only (bool): True if the user only wants public spots

    Returns:
        bool: True if the spot should be shown to the user
    """
    if fish_type not in spot.fish_types:
        return False
    if public_only and not spot.public_access:
        return False
    return True


def sort_by_distance(spots: list[FishingSpot]) -> list[FishingSpot]:
    """
    Puts the spots in order from nearest to farthest. Each spot is
    put after every spot that is already closer than it.

    Args:
        spots (list[FishingSpot]): the spots to sort

    Returns:
        list[FishingSpot]: a new list sorted by distance
    """
    sorted_spots = []
    for spot in spots:
        position = 0
        for placed in sorted_spots:
            if placed.distance <= spot.distance:
                position = position + 1
        sorted_spots.insert(position, spot)
    return sorted_spots


def find_matching_spots(spots: list[FishingSpot], fish_type: str,
                        public_only: bool, user_lat: float,
                        user_lon: float) -> list[FishingSpot]:
    """
    Loops over all the spots, keeps the ones that match the search and
    are within MAX_MILES of the user, and sorts them by distance.

    Args:
        spots (list[FishingSpot]): all the spots to search through
        fish_type (str): the fish the user is looking for
        public_only (bool): True if the user only wants public spots
        user_lat (float): the user's latitude
        user_lon (float): the user's longitude

    Returns:
        list[FishingSpot]: matching spots, closest first
    """
    matches = []
    for spot in spots:
        if spot_matches(spot, fish_type, public_only):
            spot.distance = calculate_distance(user_lat, user_lon,
                                               spot.latitude, spot.longitude)
            if spot.distance <= MAX_MILES:
                matches.append(spot)
    return sort_by_distance(matches)


def is_favorite(favorites: list[FishingSpot], spot_name: str) -> bool:
    """
    Checks if a spot with the given name is already a favorite.

    Args:
        favorites (list[FishingSpot]): the user's saved spots
        spot_name (str): the name of the spot to look for

    Returns:
        bool: True if the spot is already saved
    """
    for spot in favorites:
        if spot.name == spot_name:
            return True
    return False


def maps_link(spot: FishingSpot) -> str:
    """
    Builds a Google Maps link that points at the spot's location.

    Args:
        spot (FishingSpot): the spot to make a link for

    Returns:
        str: the Google Maps URL
    """
    return ("https://www.google.com/maps/search/?api=1&query="
            + str(spot.latitude) + "," + str(spot.longitude))


def access_text(spot: FishingSpot) -> str:
    """
    Describes whether the public can fish at the spot.

    Args:
        spot (FishingSpot): the spot to describe

    Returns:
        str: a sentence about public access
    """
    if spot.public_access:
        return "Public access: Yes"
    return "Public access: No - private property, ask for permission first"



# Routes


@route
def index(state: State) -> Page:
    """
    The home page, where the user enters their ZIP code, picks a fish
    type, and chooses whether they only want public spots.

    Args:
        state (State): the current state of the website

    Returns:
        Page: the home page
    """
    return Page(state, [
        Header("Fishing Spot Finder"),
        "Find the closest place to catch the fish you want.",
        "Enter your ZIP code (Delaware):",
        TextBox("zip_code", state.zip_code),
        "What fish are you looking for?",
        SelectBox("fish_type", FISH_TYPES, state.fish_type),
        "Only show spots with public access:",
        CheckBox("public_only", True),
        Button("Find Fish", "show_results"),
        Button("My Favorites", "favorites")
    ])


@route
def show_results(state: State, zip_code: str, fish_type: str,
                 public_only: bool) -> Page:
    """
    Saves the search in the state, finds the matching spots closest to
    the user's ZIP code, and shows them. Goes to the no_results page if
    the ZIP code is unknown or nothing matches.

    Args:
        state (State): the current state of the website
        zip_code (str): the ZIP code the user typed in
        fish_type (str): the fish the user picked
        public_only (bool): True if the user only wants public spots

    Returns:
        Page: the results page, or the no results page
    """
    state.zip_code = zip_code.strip()
    state.fish_type = fish_type
    state.spots = []
    if state.zip_code not in ZIP_LOCATIONS:
        return no_results(state)
    location = ZIP_LOCATIONS[state.zip_code]
    state.spots = find_matching_spots(all_spots(), fish_type, public_only,
                                      location[0], location[1])
    if len(state.spots) == 0:
        return no_results(state)
    content = [Header(fish_type + " spots near " + state.zip_code),
               "Closest spots first:", LineBreak()]
    for spot in state.spots:
        content.append(spot.name + " - " + str(spot.distance)
                       + " miles away")
        content.append(Button("View Details", "spot_details",
                              [Argument("spot_name", spot.name)]))
        content.append(LineBreak())
    content.append(Button("New Search", "reset_search"))
    content.append(Button("My Favorites", "favorites"))
    return Page(state, content)


@route
def spot_details(state: State, spot_name: str) -> Page:
    """
    Shows the details for one spot: distance, fish, public access, and
    a Google Maps link. Lets the user save the spot as a favorite.

    Args:
        state (State): the current state of the website
        spot_name (str): the name of the spot to show

    Returns:
        Page: the spot details page (or the home page if not found)
    """
    state.selected_spot = spot_name
    for spot in state.spots + state.favorites:
        if spot.name == spot_name:
            content = [Header(spot.name),
                       "Distance: " + str(spot.distance) + " miles",
                       "Fish found here:",
                       BulletedList(spot.fish_types),
                       access_text(spot),
                       Link("Open in Google Maps", maps_link(spot))]
            if is_favorite(state.favorites, spot.name):
                content.append("This spot is in your favorites.")
            else:
                content.append(Button("Save Spot", "save_favorite",
                                      [Argument("spot_name", spot.name)]))
            content.append(Button("My Favorites", "favorites"))
            content.append(Button("Back to Home", "index"))
            return Page(state, content)
    return index(state)


@route
def save_favorite(state: State, spot_name: str) -> Page:
    """
    Adds the spot to the user's favorites (if it isn't already there),
    then goes to the favorites page.

    Args:
        state (State): the current state of the website
        spot_name (str): the name of the spot to save

    Returns:
        Page: the favorites page
    """
    if not is_favorite(state.favorites, spot_name):
        for spot in state.spots:
            if spot.name == spot_name:
                state.favorites.append(spot)
    return favorites(state)


@route
def favorites(state: State) -> Page:
    """
    Shows every spot the user has saved.

    Args:
        state (State): the current state of the website

    Returns:
        Page: the favorites page
    """
    content = [Header("My Favorite Spots")]
    if len(state.favorites) == 0:
        content.append("You have not saved any spots yet.")
    for spot in state.favorites:
        content.append(spot.name)
        content.append(Button("View Details", "spot_details",
                              [Argument("spot_name", spot.name)]))
        content.append(LineBreak())
    content.append(Button("Back to Home", "index"))
    return Page(state, content)


@route
def no_results(state: State) -> Page:
    """
    Tells the user why no spots were found (unknown ZIP code or no
    matching spots) and lets them try again.

    Args:
        state (State): the current state of the website

    Returns:
        Page: the no results page
    """
    if state.zip_code not in ZIP_LOCATIONS:
        message = ("Sorry, " + state.zip_code + " is not a ZIP code we "
                   "have on file. Please try a Delaware ZIP code.")
    else:
        message = ("Sorry, no spots for " + state.fish_type
                   + " were found within " + str(MAX_MILES)
                   + " miles of " + state.zip_code + ".")
    return Page(state, [
        Header("No Results"),
        message,
        Button("Try Again", "index")
    ])


@route
def reset_search(state: State) -> Page:
    """
    Clears the current search (but keeps favorites) and goes back home.

    Args:
        state (State): the current state of the website

    Returns:
        Page: the home page
    """
    state.zip_code = ""
    state.fish_type = FISH_TYPES[0]
    state.spots = []
    state.selected_spot = ""
    return index(state)



# Unit tests


# Spots used in the tests below
LUMS = FishingSpot("Lums Pond State Park", 39.558, -75.728,
                   ["Largemouth Bass", "Bluegill", "Catfish", "Crappie"],
                   True, 8.8)
BECKS = FishingSpot("Becks Pond", 39.640, -75.712,
                    ["Largemouth Bass", "Bluegill", "Catfish"], True, 3.5)
HOOPES = FishingSpot("Hoopes Reservoir", 39.775, -75.640,
                     ["Largemouth Bass", "Crappie"], False, 1.0)

# calculate_distance
assert_equal(calculate_distance(39.0, -75.0, 39.0, -75.0), 0.0)
assert_equal(calculate_distance(39.0, -75.0, 40.0, -75.0), 69.0)
assert_equal(calculate_distance(39.0, -75.0, 39.0, -76.0), 53.0)

# spot_matches
assert_equal(spot_matches(LUMS, "Catfish", True), True)
assert_equal(spot_matches(LUMS, "Trout", False), False)
assert_equal(spot_matches(HOOPES, "Crappie", True), False)
assert_equal(spot_matches(HOOPES, "Crappie", False), True)

# sort_by_distance
assert_equal(sort_by_distance([]), [])
assert_equal(sort_by_distance([LUMS, BECKS, HOOPES]), [HOOPES, BECKS, LUMS])
assert_equal(sort_by_distance([BECKS, LUMS]), [BECKS, LUMS])

# find_matching_spots
assert_equal(find_matching_spots([], "Trout", True, 39.684, -75.746), [])
assert_equal(find_matching_spots(
    [FishingSpot("Lums Pond State Park", 39.558, -75.728,
                 ["Largemouth Bass", "Bluegill", "Catfish", "Crappie"],
                 True, 0.0),
     FishingSpot("Becks Pond", 39.640, -75.712,
                 ["Largemouth Bass", "Bluegill", "Catfish"], True, 0.0)],
    "Catfish", True, 39.684, -75.746),
    [FishingSpot("Becks Pond", 39.640, -75.712,
                 ["Largemouth Bass", "Bluegill", "Catfish"], True, 3.5),
     FishingSpot("Lums Pond State Park", 39.558, -75.728,
                 ["Largemouth Bass", "Bluegill", "Catfish", "Crappie"],
                 True, 8.7)])
assert_equal(find_matching_spots(
    [FishingSpot("Indian River Inlet", 38.609, -75.064,
                 ["Striped Bass"], True, 0.0)],
    "Striped Bass", True, 39.684, -75.746), [])

# is_favorite
assert_equal(is_favorite([], "Becks Pond"), False)
assert_equal(is_favorite([LUMS, BECKS], "Becks Pond"), True)
assert_equal(is_favorite([LUMS], "Becks Pond"), False)

# maps_link
assert_equal(maps_link(BECKS),
             "https://www.google.com/maps/search/?api=1&query=39.64,-75.712")

# access_text
assert_equal(access_text(LUMS), "Public access: Yes")
assert_equal(access_text(HOOPES),
             "Public access: No - private property, ask for permission first")

# index
assert_equal(index(State("", "Trout", [], [], "")),
             Page(State("", "Trout", [], [], ""), [
                 Header("Fishing Spot Finder"),
                 "Find the closest place to catch the fish you want.",
                 "Enter your ZIP code (Delaware):",
                 TextBox("zip_code", ""),
                 "What fish are you looking for?",
                 SelectBox("fish_type", FISH_TYPES, "Trout"),
                 "Only show spots with public access:",
                 CheckBox("public_only", True),
                 Button("Find Fish", "show_results"),
                 Button("My Favorites", "favorites")
             ]))

# show_results - a good search
INLET = FishingSpot("Indian River Inlet", 38.609, -75.064,
                    ["Striped Bass"], True, 7.7)
PIER = FishingSpot("Cape Henlopen Fishing Pier", 38.785, -75.095,
                   ["Striped Bass"], True, 4.6)
assert_equal(show_results(State("", "Trout", [], [], ""),
                          "19971", "Striped Bass", True),
             Page(State("19971", "Striped Bass", [PIER, INLET], [], ""), [
                 Header("Striped Bass spots near 19971"),
                 "Closest spots first:",
                 LineBreak(),
                 "Cape Henlopen Fishing Pier - 4.6 miles away",
                 Button("View Details", "spot_details",
                        [Argument("spot_name",
                                  "Cape Henlopen Fishing Pier")]),
                 LineBreak(),
                 "Indian River Inlet - 7.7 miles away",
                 Button("View Details", "spot_details",
                        [Argument("spot_name", "Indian River Inlet")]),
                 LineBreak(),
                 Button("New Search", "reset_search"),
                 Button("My Favorites", "favorites")
             ]))

# show_results - unknown ZIP code goes to no_results
assert_equal(show_results(State("", "Trout", [], [], ""),
                          "12345", "Trout", True),
             Page(State("12345", "Trout", [], [], ""), [
                 Header("No Results"),
                 "Sorry, 12345 is not a ZIP code we have on file. "
                 "Please try a Delaware ZIP code.",
                 Button("Try Again", "index")
             ]))

# show_results - no spots nearby goes to no_results
assert_equal(show_results(State("", "Trout", [], [], ""),
                          "19971", "Trout", True),
             Page(State("19971", "Trout", [], [], ""), [
                 Header("No Results"),
                 "Sorry, no spots for Trout were found within 25.0 miles "
                 "of 19971.",
                 Button("Try Again", "index")
             ]))

# spot_details - spot that is not saved yet
assert_equal(spot_details(State("19711", "Catfish", [BECKS], [], ""),
                          "Becks Pond"),
             Page(State("19711", "Catfish", [BECKS], [], "Becks Pond"), [
                 Header("Becks Pond"),
                 "Distance: 3.5 miles",
                 "Fish found here:",
                 BulletedList(["Largemouth Bass", "Bluegill", "Catfish"]),
                 "Public access: Yes",
                 Link("Open in Google Maps", maps_link(BECKS)),
                 Button("Save Spot", "save_favorite",
                        [Argument("spot_name", "Becks Pond")]),
                 Button("My Favorites", "favorites"),
                 Button("Back to Home", "index")
             ]))

# spot_details - spot that is already a favorite
assert_equal(spot_details(State("", "Trout", [], [HOOPES], ""),
                          "Hoopes Reservoir"),
             Page(State("", "Trout", [], [HOOPES], "Hoopes Reservoir"), [
                 Header("Hoopes Reservoir"),
                 "Distance: 1.0 miles",
                 "Fish found here:",
                 BulletedList(["Largemouth Bass", "Crappie"]),
                 "Public access: No - private property, "
                 "ask for permission first",
                 Link("Open in Google Maps", maps_link(HOOPES)),
                 "This spot is in your favorites.",
                 Button("My Favorites", "favorites"),
                 Button("Back to Home", "index")
             ]))

# save_favorite - adds a new favorite
assert_equal(save_favorite(State("19711", "Catfish", [BECKS], [], ""),
                           "Becks Pond"),
             Page(State("19711", "Catfish", [BECKS], [BECKS], ""), [
                 Header("My Favorite Spots"),
                 "Becks Pond",
                 Button("View Details", "spot_details",
                        [Argument("spot_name", "Becks Pond")]),
                 LineBreak(),
                 Button("Back to Home", "index")
             ]))

# save_favorite - does not add the same spot twice
assert_equal(save_favorite(State("19711", "Catfish", [BECKS], [BECKS], ""),
                           "Becks Pond"),
             Page(State("19711", "Catfish", [BECKS], [BECKS], ""), [
                 Header("My Favorite Spots"),
                 "Becks Pond",
                 Button("View Details", "spot_details",
                        [Argument("spot_name", "Becks Pond")]),
                 LineBreak(),
                 Button("Back to Home", "index")
             ]))

# favorites - no favorites yet
assert_equal(favorites(State("", "Trout", [], [], "")),
             Page(State("", "Trout", [], [], ""), [
                 Header("My Favorite Spots"),
                 "You have not saved any spots yet.",
                 Button("Back to Home", "index")
             ]))

# no_results
assert_equal(no_results(State("99999", "Trout", [], [], "")),
             Page(State("99999", "Trout", [], [], ""), [
                 Header("No Results"),
                 "Sorry, 99999 is not a ZIP code we have on file. "
                 "Please try a Delaware ZIP code.",
                 Button("Try Again", "index")
             ]))

# reset_search - clears the search but keeps favorites
assert_equal(reset_search(State("19711", "Catfish", [BECKS], [LUMS],
                                "Becks Pond")),
             Page(State("", "Largemouth Bass", [], [LUMS], ""), [
                 Header("Fishing Spot Finder"),
                 "Find the closest place to catch the fish you want.",
                 "Enter your ZIP code (Delaware):",
                 TextBox("zip_code", ""),
                 "What fish are you looking for?",
                 SelectBox("fish_type", FISH_TYPES, "Largemouth Bass"),
                 "Only show spots with public access:",
                 CheckBox("public_only", True),
                 Button("Find Fish", "show_results"),
                 Button("My Favorites", "favorites")
             ]))


start_server(State("", "Largemouth Bass", [], [], ""))

