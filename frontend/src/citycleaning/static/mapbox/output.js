// Return arrays of destinations to use in the v2 or v1 optimization api
function generate_calls(routings, dropoffs, token) {
    const output = [];

    // Get a map of the possible endpoints
    const endpoints = dropoffs.features.map(
        feature => feature.geometry.coordinates
    );

    /*
    * Api V2
    * To post the json we get we create a http request
    * We link it to a specific address
    * And we put it in the queue
    */
    // output.push(`https://api.mapbox.com/optimized-trips/v2?access_token=${token}`);

    /*
    * Api V1
    * To post the json as a line in the request
    * We link it to a specific address
    * We set the headers as below
    * And then we send it to the queue
    */
    for (const to_call in routings.v1) {
        const url_base = "https://api.mapbox.com/optimized-trips/v1";
        const url_options = [
            `access_token=${token}`,
            "overview=full",
            "steps=true",
            "geometries=geojson",
            "source=first",
            "destination=last",
        ];


        let { locations, profile } = routings.v1[to_call];
        let closest = [];

        // Loop over the endpoints to find the closest to one location
        for (const idx in endpoints) {
            let lon1 = parseFloat(endpoints[idx][0]);
            let lat1 = parseFloat(endpoints[idx][1]);
            
            for (const idx2 in locations) {
                let lon2 = parseFloat(locations[idx2].locations[0]);
                let lat2 = parseFloat(locations[idx2].locations[1]);

                // If there is one we check
                if (typeof closest[idx2] !== "undefined") {
                    let current = closest[idx2];
                    let lon_dst = lon2 >= lon1 ? lon2 - lon1 : lon1 - lon2;
                    let lat_dst = lat2 >= lat1 ? lat2 - lat1 : lat1 - lat2;

                    if (current.total_dst > lon_dst + lat_dst) {
                        closest[idx2] = {
                            index: idx2,
                            pickup: locations[idx2].locations,
                            dropoff: endpoints[idx],
                            lon_dst,
                            lat_dst,
                            total_dst: lon_dst + lat_dst,
                        };
                    }

                // Else we create
                } else {
                    let lon_dst = lon2 >= lon1 ? lon2 - lon1 : lon1 - lon2;
                    let lat_dst = lat2 >= lat1 ? lat2 - lat1 : lat1 - lat2;

                    closest.push({
                        index: idx2,
                        pickup: locations[idx2].locations,
                        dropoff: endpoints[idx],
                        lon_dst,
                        lat_dst,
                        total_dst: lon_dst + lat_dst,
                    });
                }
            }
        }

        closest.sort((a, b) => a.total_dst - b.total_dst);

        let url_coords = 
            `${closest[1].dropoff[0]},${closest[1].dropoff[1]};` +
            locations.map(loc => `${loc.locations[0]},${loc.locations[1]}`).join(";") +
            `;${closest[0].dropoff[0]},${closest[0].dropoff[1]}`;
        
        let this_url = 
            `${url_base}/${profile}/${url_coords}?${url_options.join("&")}`;
        
        output.push(this_url);
    }

    return output;
}