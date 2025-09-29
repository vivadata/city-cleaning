/*
 * Vehicle json
 * let template = {
 *     name: "",                          // Must be unique
 *     routing_profile: "mapbox/driving", // Default value, all accepted in the profiles const
 *     loading_policy: "any",             // Default value, all accepted are in the policies const
 *     start_location: null,              // Optional, linked to locations, name of the location the route will start from
 *     end_location: null,                // Optional, linked to locations, name of the location the route will end at
 *     capacities: {},                    // Optional, linked to shipments, sizes that can be fit into the vehicle, as a dict of integers
 *     capabilities: [],                  // Optional, linked to services/shipments, requirements of the vehicle as array of strings
 *     earliest_start: null,              // Optional, start date and time of route in format "YYYY-MM-DDThh:mm:ssZ"
 *     latest_end: null,                  // Optional, end date and time of route in format "YYYY-MM-DDThh:mm:ssZ"
 *     breaks: [],                        // Optional, mandatory breaks that can be taken along the route
 * };
 * 
 * Break json
 * let break_tmpl = {
 *     earliest_start: null, // Start date and time of break in format "YYYY-MM-DDThh:mm:ssZ"
 *     latest_end: null,     // End date and time of break in format "YYYY-MM-DDThh:mm:ssZ"
 *     duration: 0,          // The duration of the break in seconds
 * };
 */

// Function to get profiles of location
function get_profile(params) {
    const { loc } = params;
    const { types } = loc;
    const { profile: all_profiles } = trash_params;

    let profiles = [];
    let is_profile = null;

    // For each type create profile array    
    for (const type in types) {
        let profile = [];

        // For each profile if type fill array
        for (const key in Object.keys(all_profiles)) {
            let this_key = Object.keys(all_profiles)[key];
            if (all_profiles[this_key].includes(types[type])) profile.push(this_key);
        }

        // Then fill general array with either array or sole element
        profiles.push(profile.length > 1 ? profile : profile[0]);
    }

    // For each profile check whether it's always usable
    for (const key in Object.keys(all_profiles)) {
        let this_key = Object.keys(all_profiles)[key];
        let is_keyed = 0;

        for (const profile in profiles) {
            if (typeof profiles[profile] == "string") {
                if (profiles[profile] == this_key) is_keyed += 1;

            } else {
                if (profiles[profile].includes(this_key)) is_keyed += 1;
            }
        }

        if (is_keyed == profiles.length) is_profile = this_key;
    }

    // If a profile exists for all types return it along with all types
    if (is_profile) {
        loc.profiles = [is_profile];

        return { 
            with_profiles: [{ types, profile: [is_profile] }],
            loc,
        };
    }

    // Else loop over the profiles to associate the types
    profiles = profiles.map(
        profile => typeof profile == "string" ? profile : profile.at(-1)
    );

    let output = [];
    loc.profiles = profiles;

    for (const idx in Object.keys(profiles)) {
        let this_index = Object.keys(profiles)[idx];
        const profile = profiles[this_index];

        // Check whether the profile is already created
        const exists = output.find(pro => pro.profile == profile);

        // If it's not create it
        if (typeof exists == "undefined") {
            output.push({
                profile,
                types: [types[this_index]],
            });

        // If it is add an instance of it
        } else {
            let new_pro = exists;
            new_pro.types.push(types[this_index]);

            output = output
                .map(pro => pro.profile == profile ? new_pro : pro);
        }
    }

    return { 
        with_profiles: output,
        loc,
    };
}

// Function to get policies of location
function get_policy(params) {
    const { data } = params;
    const { policy: all_policies } = trash_params;

    let policies = [];

    // Loop on each data point with an intermediary array
    for (const point in data) {
        let between = [];

        // For each type in the point create a policy array
        for (const type in data[point].types) {
            let policy = null;

            // For each policy if type fill array
            for (const key in Object.keys(all_policies)) {
                let this_key = Object.keys(all_policies)[key];
                if (all_policies[this_key].includes(data[point].types[type])) policy = this_key;
            }

            // Then fill general array with either array or sole element
            between.push({
                type: data[point].types[type],
                profile: data[point].profile,
                policy,
            });
        }

        // For each occurrence of between check if same policy and group in general array
        for (const tween in between) {
            // Check whether the point is already created
            const exists = policies.find(
                pol => 
                    pol.profile == between[tween].profile && pol.policy == between[tween].policy
            );

            // If it's not create it
            if (typeof exists == "undefined") {
                policies.push({
                    profile: between[tween].profile,
                    policy: between[tween].policy,
                    types: [between[tween].type],
                });

            // If it is add an instance of it
            } else {
                let new_pol = exists;
                new_pol.types.push(between[tween].type);

                policies = policies.map(pol => 
                    pol.profile == between[tween].profile && pol.policy == between[tween].policy
                        ? new_pol
                        : pol
                );
            }
        }
    }

    return policies;
}

// Function to get capacities needed in vehicle
function get_capacities(params) {
    const { data } = params;
    const { capacity: all_capacities } = trash_params;

    let capacities = [];

    // Loop on each data point with an intermediary array
    for (const point in data) {
        let between = [];

        // For each type in the point push a capacity array
        for (const type in data[point].types) {
            between.push({
                type: data[point].types[type],
                profile: data[point].profile,
                policy: data[point].policy,
                capacity: all_capacities[data[point].types[type]] ? all_capacities[data[point].types[type]] : {},
            });
        }

        // For each occurrence of between check if same capacity and group in general array
        for (const tween in between) {
            // Check whether the point is already created
            const exists = capacities.find(
                cap => 
                    cap.profile == between[tween].profile &&
                    cap.policy == between[tween].policy &&
                    JSON.stringify(Object.keys(cap.capacity).sort()) == 
                        JSON.stringify(Object.keys(between[tween].capacity).sort())
            );

            // If it's not create it
            if (typeof exists == "undefined") {
                capacities.push({
                    profile: between[tween].profile,
                    policy: between[tween].policy,
                    capacity: between[tween].capacity,
                    types: [between[tween].type],
                });

            // If it is add an instance of it
            } else {
                let new_cap = exists;
                new_cap.types.push(between[tween].type);

                capacities = capacities.map(cap => 
                    cap.profile == between[tween].profile &&
                    cap.policy == between[tween].policy &&
                    JSON.stringify(Object.keys(cap.capacity).sort()) == 
                        JSON.stringify(Object.keys(between[tween].capacity).sort())
                        ? new_cap
                        : cap
                );
            }
        }
    }

    return capacities;
}

// Function to get capacities needed in vehicle
function get_capabilities(params) {
    const { data } = params;
    const { capability: all_capabilities } = trash_params;

    let capabilities = [];

    // Loop on each data point with an intermediary array
    for (const point in data) {
        let between = [];

        // For each type in the point push a capability array
        for (const type in data[point].types) {
            between.push({
                type,
                profile: data[point].profile,
                policy: data[point].policy,
                capacity: data[point].capacity,
                capability: all_capabilities[data[point].types[type]] ? all_capabilities[data[point].types[type]] : [],
            });
        }

        // For each occurrence of between check if same capability and group in general array
        for (const tween in between) {
            // Check whether the point is already created
            const exists = capabilities.find(
                cap => 
                    cap.profile == between[tween].profile &&
                    cap.policy == between[tween].policy &&
                    JSON.stringify(Object.keys(cap.capacity).sort()) == 
                        JSON.stringify(Object.keys(between[tween].capacity).sort()) &&
                    JSON.stringify(cap.capability.sort()) ==
                        JSON.stringify(between[tween].capability.sort())
            );

            // If it's not create it
            if (typeof exists == "undefined") {
                capabilities.push({
                    profile: between[tween].profile,
                    policy: between[tween].policy,
                    capacity: between[tween].capacity,
                    capability: between[tween].capability,
                    types: [between[tween].type],
                });

            // If it is add an instance of it
            } else {
                let new_cap = exists;
                new_cap.types.push(between[tween].type);

                capabilities = capabilities.map(pol => 
                    cap.profile == between[tween].profile &&
                    cap.policy == between[tween].policy &&
                    JSON.stringify(Object.keys(cap.capacity).sort()) == 
                        JSON.stringify(Object.keys(between[tween].capacity).sort()) &&
                    JSON.stringify(cap.capability.sort()) ==
                        JSON.stringify(between[tween].capability.sort())
                        ? new_cap
                        : cap
                );
            }
        }
    }

    return capabilities;
}

// Function to generate vehicles from locations
function get_vehicles(params) {
    const { locations } = params;

    let vehicles = [];

    // get the profiles, policy, capacities, capabilities needed for each location
    for (const loc in locations) {
        const { with_profiles, loc: new_loc } = get_profile({ loc: locations[loc] });
        const with_policies = get_policy({ data: with_profiles });
        const with_capacities = get_capacities({ data: with_policies });
        const complete = get_capabilities({ data: with_capacities });

        for (const vehicle in complete) {
            // Check whether the vehicle is already created
            const exists = vehicles.find(
                vhcl => 
                    vhcl.profile == complete[vehicle].profile &&
                    vhcl.policy == complete[vehicle].policy &&
                    JSON.stringify(Object.keys(vhcl.capacity).sort()) == 
                        JSON.stringify(Object.keys(complete[vehicle].capacity).sort()) &&
                    JSON.stringify(vhcl.capability.sort()) ==
                        JSON.stringify(complete[vehicle].capability.sort())
            );

            // If it's not create it
            if (typeof exists == "undefined") {
                vehicles.push({
                    ...complete[vehicle],
                    name: `vehicle-${locations[loc].name}-${vehicles.length}`,
                });
            }
        }

        locations[loc] = new_loc;
    }

    return { vehicles, locations };
}