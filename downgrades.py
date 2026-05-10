upgrades: dict[range, dict[str, dict[str, list[str]]]] = {
    range(1, 20): {
        "Running Shoes": {
            "benefit": ["spd++"],
            "detriment": ["trip+"]
        },
        "Big Guns": {
            "benefit": ["dmg+", "bspd+"],
            "detriment": ["sprd+", "spd-"]
        },
        "Curse of Piercing": {
            "benefit": ["bspd+++++++++++++++++++++++++++++++++++++++++++++", "dmg++++++++++++++++++"],
            "detriment": []
        }
    },
    range(5, 25): {
        "Plating": {
            "benefit": ["def++"],
            "detriment": ["spd--"]
        },
        "Curse Remedy (Piercing)": {
            "benefit": [],
            "detriment": ["dmg---------", "bspd----------------------------------------"]
        },
        "Careful Footing": {
            "benefit": ["trip--"],
            "detriment": ["spd-"]
        }
    },
    range(10, 30): {
        "Curse of Stillness": {
            "benefit": ["sprd-------------------------", "trip---------"],
            "detriment": ["spd------------------------"]
        }
    },
    range(15, 35): {
        "Curse Remedy (Stillness)": {
            "benefit": ["spd+++++++++++++++++"],
            "detriment": ["sprd++++++++++++++++++", "trip++++++++"]
        }
    }
}