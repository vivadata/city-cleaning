/*
 * Service json
 * let service = {
 *     name: "",          // Must be unique
 *     location: "",      // Linked to locations, name of the location of the service
 *     duration: 0,       // Optional, duration in seconds needed to complete the service
 *     requirements: [],  // Optional, linked to vehicles, abilities needed to perform as an array of strings
 *     service_times: [], // Optional, time intervals during which the service can be performed
 * };
 * 
 * Time Interval json
 * let service_time_ = {
 *     earliest: null, // Start date and time of service in format "YYYY-MM-DDThh:mm:ssZ"
 *     latest: null,   // End date and time of service in format "YYYY-MM-DDThh:mm:ssZ"
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

// Function to get services from locations
function get_services(params) {
    const { locations } = params;

    let services = [];

    // Loop on each location to check if there are only services or services without shipments
    for (const loc in locations) {
        let is_service = true;

        // Loop on each type to make sure
        for (const type in locations[loc].types) {
            if (
                !Object.keys(trash_params.capability).includes(locations[loc].types[type]) ||
                Object.keys(trash_params.capacity).includes(locations[loc].types[type])
            ) {
                is_service = false;
            }
        }

        if (is_service) {
            services.push({
                name: `service-${locations[loc].name}`,
                location: locations[loc].name,
                requirements: get_requirements({ loc: locations[loc] }),
            });
        }
    }

    return services;
}
