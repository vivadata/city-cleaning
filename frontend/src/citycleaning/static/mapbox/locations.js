/*
 * Location json
 * const template = {
 *     name: "",          // Must be unique
 *     locations: [0, 0], // Must be longitude then latitude
 * };
 */

// Function to get clean coords in [lon, lat] format
function get_coords(params) {
    // Import values
    const { coords, town } = params;
    const bounds = town_bounds[town];

    // Default values
    let lon = 0, lat = 1;

    // Find the order of the coords if you can
    if (
        parseFloat(coords[0]) >= bounds.west &&
        parseFloat(coords[0]) <= bounds.east &&
        parseFloat(coords[1]) >= bounds.south &&
        parseFloat(coords[1]) <= bounds.north
    ) {
        lon = 0;
        lat = 1;

    } else if (
        parseFloat(coords[1]) >= bounds.west &&
        parseFloat(coords[1]) <= bounds.east &&
        parseFloat(coords[0]) >= bounds.south &&
        parseFloat(coords[0]) <= bounds.north
    ) {
        lon = 1;
        lat = 0;
    }

    // Format and return in proper order
    return [
        parseFloat(coords[lon]).toFixed(6),
        parseFloat(coords[lat]).toFixed(6),
    ];
}

// Function to determine locations from trash locations
function get_locations(params) {
    const { trash } = params;
    const locations = [];

    // For each point sent
    for (const evt in trash) {
        // Extract and clean data
        const { latitude, longitude, type } = trash[evt];
        const location = 
            get_coords({
                coords: [longitude, latitude],
                town: "paris",
            });

        // Check whether the point is already located
        const exists = locations.find(loc => loc.locations == location);

        // If it's not create it
        if (typeof exists == "undefined") {
            locations.push({
                locations: location,
                types: [type],
            });

        // If it is add an instance of it
        } else {
            let new_loc = exists;
            new_loc.types.push(type);

            locations = locations
                .map(loc => loc.locations == location ? new_loc : loc);
        }
    }

    // Name and return them
    return locations.map((loc, idx) => ({ ...loc, name: `trash-${idx}` }));
}
