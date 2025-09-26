// The vehicle routing profiles
const routing_profiles = [
    "mapbox/driving-traffic", // Route will be calculated based on car routes and assimilated traffic
    "mapbox/driving", // Route will be calculated based on car routes
    "mapbox/cycling", // Route will be calculated based on bike routes
    "mapbox/walking", // Route will be calculated based on pedestrian routes
];

// The vehicle loading policies
const loading_policies = [
    "any", // No specific policy
    "fifo", // First item in is first item out
    "lifo", // Last item in is first item out
];

// The time range types for shipments and services
const time_range_types = [
    "strict", // Inflexible limits
    "soft", // Flexible limits
    "soft_start", // Flexible start, inflexible end
    "soft_end", // Inflexible start, flexible end
];

/*
 * Different map styles
 * Most are deprecated, two active
 * Note it should be possible to create your own map style here:
 * https://docs.mapbox.com/help/tutorials/aa-standard-in-studio/?step=0
 */
const map_styles = {
    // Maintained
    standard: "mapbox://styles/mapbox/standard",
    standard_satellite: "mapbox://styles/mapbox/standard-satellite",
    // Deprecated
    streets: "mapbox://styles/mapbox/streets-v12",
    outdoors: "mapbox://styles/mapbox/outdoors-v12",
    light: "mapbox://styles/mapbox/light-v11",
    dark: "mapbox://styles/mapbox/dark-v11",
    satellite: "mapbox://styles/mapbox/satellite-v9",
    satellite_streets: "mapbox://styles/mapbox/satellite-streets-v12",
    navigation_day: "mapbox://styles/mapbox/navigation-day-v1",
    navigation_night: "mapbox://styles/mapbox/navigation-night-v1",
}; 

/*
 * Extreme coordinates by town, to determine position
 * If more towns are added stock in other script and import
 */
const town_bounds = {
    paris: {
        north: 48.902146,
        east: 2.469841,
        south: 48.815565,
        west: 2.224214,
    },
};

/*
 * In order to have distinct colors for each map
 * Let's setup a color map
 */
const colors = [
    "#800000",
    "#9A6324",
    "#808000",
    "#469990",
    "#000075",
    //"#000000",
    "#E6194B",
    "#F58231",
    "#FFE119",
    "#BFEF45",
    "#3CB44B",
    "#42D4F4",
    "#4363D8",
    "#911EB4",
    "#F032E6",
    //"#A9A9A9",
    "#FABED4",
    "#FFD8B1",
    "#FFFAC8",
    "#AAFFC3",
    "#DCBEFF",
    //"#FFFFFF",
];