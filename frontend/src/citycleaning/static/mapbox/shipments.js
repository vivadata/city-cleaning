/*
 * Shipment json
 * let shipment_ = {
 *     name: "",            // Must be unique
 *     from: "",            // Linked to locations, name of the start of the shipment
 *     to: "",              // Linked to locations, name of the end of the shipment
 *     pickup_duration: 0,  // Default value, time needed to pick up shipment in seconds
 *     dropoff_duration: 0, // Default value, time needed to drop off shipment in seconds
 *     size: {},            // Optional, linked to vehicles, capacity needed to carry shipment as a dict of integers
 *     requirements: [],    // Optional, linked to vehicles, abilities needed to ship as an array of strings
 *     pickup_times: [],    // Optional , array of 1 time when shipment can be picked up
 *     dropoff_times: [],   // Optional , array of 1 time when shipment can be dropped off
 * };
 * 
 * Pickup json
 * let pickup_time_ = {
 *     earliest: null, // Start date and time of pickup in format "YYYY-MM-DDThh:mm:ssZ"
 *     latest: null,   // End date and time of pickup in format "YYYY-MM-DDThh:mm:ssZ"
 *     type: "strict", // Default value, type of adherence to to the time interval provided
 * };
 * 
 * Dropoff json
 * let dropoff_time_ = {
 *     earliest: null, // Start date and time of dropoff in format "YYYY-MM-DDThh:mm:ssZ"
 *     latest: null,   // End date and time of dropoff in format "YYYY-MM-DDThh:mm:ssZ"
 *     type: "strict", // Default value, type of adherence to to the time interval provided
 * };
 */


// Function to get requirements from location
function get_requirements(params) {
    const { loc } = params;
    const { capability } = trash_params;

    let requirements = [];

    // Loop on the types to get all services
    for (const type in loc.types) {
        if (Object.keys(capability).includes(loc.types[type])) {
            requirements = requirements.concat(capability[loc.types[type]]);
        }
    }

    // Then remove duplicates
    requirements = [...new Set(requirements)];

    return requirements;
}

// Function to get sizes of shipments from location
function get_sizes(params) {
    const { loc } = params;
    const { capacity } = trash_params;

    let sizes = {};

    // Loop on the types to get all sizes
    for (const type in loc.types) {
        if (Object.keys(capacity).includes(loc.types[type])) {
            let size = Object.keys(capacity[loc.types[type]])[0];

            if (Object.keys(sizes).includes(size)) {
                sizes[size] += Math.ceil(capacity[loc.types[type]][size] / 10);
            } else {
                sizes[size] = Math.ceil(capacity[loc.types[type]][size] / 10);
            }
        }
    }

    return sizes;
}

// Function to get services from locations
function get_shipments(params) {
    const { locations } = params;

    let shipments = [];

    // Loop on each location to check if there are only services or services without shipments
    for (const loc in locations) {
        let is_shipment = true;

        // Loop on each type to make sure
        for (const type in locations[loc].types) {
            if (
                !Object.keys(trash_params.capacity).includes(locations[loc].types[type])
            ) {
                is_shipment = false;
            }
        }

        if (is_shipment) {
            shipments.push({
                name: `shipment-${locations[loc].name}`,
                from: locations[loc].name,
                to: locations[loc].name,
                requirements: get_requirements({ loc: locations[loc] }),
                size: get_sizes({ loc: locations[loc] }),
            });
        }
    }

    return shipments;
}
