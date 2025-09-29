// Params to determine input of requests
const trash_params = {
    profile: {
        "mapbox/driving-traffic" : [ // Big trucks, specialized vehicles
            "Autos, motos, vélos...", // Will necessite large capacity
            "Autos, motos, vélos, trottinettes...", // May necessite large capacity
            "Mobiliers urbains", // Cumbersome loads
            "Arbres, végétaux et animaux", // Capacity and material needed
            "Problème sur un chantier", // Heavy capacity
        ],
        "mapbox/driving" : [ // Cars, small trucks
            "Éclairage / Électricité", // Material and small or retractable parts
            "Graffitis, tags, affiches et autocollants", // Material and small parts
            "Eau", // Intervention, heavy components possible
            "Activités commerciales et professionnelles", // Material needed
            "Du vert près de chez moi", // Green maintenance, medium loads and material
            "Mobiliers urbains", // Cumbersome loads
            "Arbres, végétaux et animaux", // Capacity and material needed
            "Dégradation du sol", // Medium material
        ],
        "mapbox/cycling" : [ // Motorcycles, bicycles
            "Objets abandonnés", // Small volumes with unknown weight
            "Voirie et espace public", // Advanced cleaning
            "Propreté", // Simple cleaning
        ],
        "mapbox/walking" : [ // Pedestrians, esoteric
            "Propreté", // Simple cleaning
            "Voirie et espace public", // Advanced cleaning
        ],
    },
    policy: {
        "any": [ // No loading bay
            "Éclairage / Électricité", // Material and small or retractable parts
            "Graffitis, tags, affiches et autocollants", // Material and small parts
            "Objets abandonnés", // Small volumes with unknown weight
            "Voirie et espace public", // Advanced cleaning
            "Dégradation du sol", // Medium material
            "Propreté", // Simple cleaning
        ],
        "fifo": [ // Ordered loading bay
            "Autos, motos, vélos...", // Will necessite large capacity
            "Autos, motos, vélos, trottinettes...", // May necessite large capacity
            "Mobiliers urbains", // Cumbersome loads
            "Arbres, végétaux et animaux", // Capacity and material needed
            "Problème sur un chantier", // Heavy capacity
        ],
        "lifo": [ // Unordered loading bay
            "Eau", // Intervention, heavy components possible
            "Activités commerciales et professionnelles", // Material needed
            "Du vert près de chez moi", // Green maintenance, medium loads and material
        ],
    },
    capacity: {
        "Autos, motos, vélos...": { // Will necessite large capacity
            two_wheeler: 30, // 1 bike, 2 motorbike, 3 car
        },
        "Autos, motos, vélos, trottinettes...": { // May necessite large capacity
            two_wheeler: 30, // 1 bike, 2 motorbike, 3 car
        },
        "Mobiliers urbains": { // Cumbersome loads
            cube: 20, // 1 small, 2 large or tall, 3 very of each, 4 combination
        },
        "Arbres, végétaux et animaux": { // Capacity and material needed
            boxes: 10, // 1 dog or cat or greenery, 2 horse or tree
        },
        "Problème sur un chantier": { // Heavy capacity
            load: 5, // 1 heavy debris, 2 machinery
        },
        "Eau": { // Intervention, heavy components possible
            pipes: 5, // 1medium material, 2 pipes
        },
        "Du vert près de chez moi": { // Green maintenance, medium loads and material
            trash: 5, // 1 bin
        },
        "Éclairage / Électricité": { // Material and small or retractable parts
            trash: 10, // 1 bin
        },
        "Graffitis, tags, affiches et autocollants": { // Material and small parts
            trash: 5, // 1 bin
        },
        "Objets abandonnés": { // Small volumes with unknown weight
            trash: 2, // 1 item
        },
        "Voirie et espace public": { // Advanced cleaning
            tash: 6, // 1 bag
        },
    },
    capability: {
        "Autos, motos, vélos...": [ // Will necessite large capacity
            "vehicle_bay", // Loading vehicles in
        ],
        "Autos, motos, vélos, trottinettes...": [ // May necessite large capacity
            "vehicle_bay", // Loading vehicles in
        ],
        "Mobiliers urbains": [ // Cumbersome loads
            "furniture_bay", // Loading heavy furniture in
        ],
        "Arbres, végétaux et animaux": [ // Capacity and material needed
            "animal_cages", // Boxes for animals
            "greenery_tools", // Tools for greenery maintenance
        ],
        "Du vert près de chez moi": [ // Green maintenance, medium loads and material
            "greenery_tools", // Tools for greenery maintenance
        ],
        "Problème sur un chantier": [ // Heavy capacity
            "heavy_material", // Loading heavy machines and construction debris
        ],
        "Eau" : [ // Intervention, heavy components possible
            "plumbing_tools", // Tools for water system maintenance
        ],
        "Éclairage / Électricité": [ // Material and small or retractable parts
            "electricity_tools", // Tools for electric maintenance
        ],
        "Graffitis, tags, affiches et autocollants": [ // Material and small parts
            "cleaning_tools", // Light cleaning tools
        ],
        "Voirie et espace public": [ // Advanced cleaning
            "cleaning_tools", // Light cleaning tools
        ],
        "Propreté": [ // Simple cleaning
            "cleaning_tools", // Light cleaning tools
        ],
        "Dégradation du sol": [ // Medium material
            "cleaning_tools", // Light cleaning tools
            "repair_tools", // Light repair material
        ],
        "Activités commerciales et professionnelles": [ // Material needed
            "specific_tools", // Tools of the trade
        ],
    },
};
