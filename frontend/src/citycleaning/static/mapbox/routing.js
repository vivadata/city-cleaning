/*
 * Routing json
 * const routing = {
 *     version: 1,    // Do not touch, must be v1
 *     locations: [], // The locations in the route
 *     vehicles: [],  // The vehicles travelling
 *     services: [],  // Optional if shipments, else required. Locations not consuming capacity
 *     shipments: [], // Optional if services, else required. Locations consuming capacity
 * };
 */

// To generate temp groups
function generate_groups (params) {
    const { locations } = params;
    let profiles = [];

    // Loop on the locations
    for (const loc in locations) {
        // Check whether the group is already created
        const exists = profiles.find(
            pro => pro.profile == locations[loc].profiles[0]
        );

        // If it doesn't create it
        if (typeof exists == "undefined") {
            profiles.push({
                profile: locations[loc].profiles[0],
                locations: [locations[loc]],
            });
        
        // Else add to the existing
        } else {
            let new_pro = exists;
            exists.locations.push(locations[loc]);

            profiles = profiles.map(
                pro => pro.profile == new_pro.profile
                    ? new_pro
                    : pro
            );
        }
    }

    return profiles;
}

// To generate the general routing
function generate_routing (params) {
    /*
     * Generating a routing means generating 4 things
     * - Locations, max 25, for the vehicles
     * - Vehicles, defined by profile, policy, capacity, capability
     * - Services, defined by requirements
     * - Shipments, defined by size, requirements
     * 
     * In order to fit these requirements, each trash location must have parameters
     * - Location, the coordinates of the trash
     * - Profile, the profile of vehicle needed
     * - Policy, the policy if it is a shipment
     * - Capacity, the volume if it is a shipment
     * - Capability, a feature needed in the vehicle
     * 
     * A trash location may have multiple of each except of course location
     * A trash location can generate multiple vehicle passages though it should be minimized
     * In case we are missing data the location will be generated using WCS protocol
     * To generate this data the type and location will be used, they are required
     */

    // First sort the trash by approximative ascending geographical coordinates in a district
    const trash = params
        .sort((a, b) => 
            parseFloat(a.longitude).toFixed(6)
            + parseFloat(a.latitude).toFixed(6)
            - parseFloat(b.longitude).toFixed(6)
            - parseFloat(b.latitude).toFixed(6)
        )
        .sort(
            (a, b) => a.ville > b.ville ? 1 : b.ville > a.ville ? -1 : 0
        );

    // Then get locations with added attributes to discern other parameters
    const lctn_drt = get_locations({ trash });

    // Then use those locations to find other parameters
    const { vehicles: vhcl_cln, locations: lctn_tmp } = get_vehicles({ locations: lctn_drt });
    const srvc_cln = get_services({ locations: lctn_drt });
    const shpmnt_cln = get_shipments({ locations: lctn_drt });

    // Finally get a clean version of your locations
    const lctn_cln = lctn_drt.map(({ locations, name }) => ({ locations, name }));

    // Also use the temp locations to generate vehicle types location groups
    const prfl_cln = generate_groups({ locations: lctn_tmp });

    return {
        v1: prfl_cln,
        v2: {
            version: 1,
            locations: lctn_cln,
            vehicles: vhcl_cln,
            services: srvc_cln,
            shipments: shpmnt_cln,
        },
    };
}

// Separate routings to not overload vehicles
function generate_routings(params) {
    const data = typeof params !== "string" ? params : JSON.parse(params);
    const routings = generate_routing(data);

    const v1 = [];
    const v2 = [];

    let pass = 0;

    // V1: Let's check locations by profile to limit number of stops
    for (const profile in routings.v1) {
        let pro = routings.v1[profile];

        while (pass * 10 < pro.locations.length) {
            v1.push({
                profile: pro.profile,
                locations: pro.locations.slice(pass * 10, (pass + 1) * 10),
            });

            pass++;
        }

        pass = 0;
    }

    // V2: Let's check locations to limit number of stops
    while (pass * 23 < routings.v2.locations.length) {
        v2.push({
            version: 1,
            locations: routings.v2.locations.slice(pass * 23, (pass + 1) * 23),
            vehicles: routings.v2.vehicles,
            services: routings.v2.services,
            shipments: routings.v2.shipments,
        });

        pass++;
    }

    // And use them to create routings
    return {
        v1,
        v2,
    };
}