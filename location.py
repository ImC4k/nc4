
def get_coordinate_pairs(location):
    # return [{"min_lat": 22.08, "max_lat": 22.35, "min_lon": 113.49, "max_lon": 114.31}]
    return [
        [(22.08, 113.49), (22.35, 114.31)]
    ]

def get_region_coordinate_pairs(location):
    return [ # 1 location, containing many regions
        { # 1 region, containing many rectangular areas
            "region_name": "Hong Kong",
            "coordinate_pairs": [
                [(22.08, 113.41), (22.35, 114.31)]
            ]
        },
        {
            "region_name": "Hong Kong 2",
            "coordinate_pairs": [
                [(22.08, 113.49), (22.35, 114.31)]
            ]
        },
        {
            "region_name": "Hong Kong 3",
            "coordinate_pairs": [
                [(22.08, 113.19), (22.35, 114.31)]
            ]
        }
    ]