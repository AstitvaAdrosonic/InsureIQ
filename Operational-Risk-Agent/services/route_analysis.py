import json
import searoute as sr


async def route_analysis(state):

    try:

        with open(
            "services/data/ports.json",
            "r",
            encoding="utf-8"
        ) as f:

            ports = json.load(f)

        # Validate ports

        if state.origin_port not in ports:

            raise ValueError(
                f"Unknown origin port: "
                f"{state.origin_port}"
            )

        if state.destination_port not in ports:

            raise ValueError(
                f"Unknown destination port: "
                f"{state.destination_port}"
            )

        origin = ports[
            state.origin_port
        ]

        destination = ports[
            state.destination_port
        ]

        # SeaRoute requires:
        # [longitude, latitude]

        origin_coords = [

            origin["lon"],
            origin["lat"]
        ]

        destination_coords = [

            destination["lon"],
            destination["lat"]
        ]

        # Generate maritime route

        route = sr.searoute(

            origin_coords,

            destination_coords
        )

        # Distance returned in km

        distance_km = round(
            route.properties["length"],
            2
        )

        # Full maritime path

        coordinates = route.geometry[
            "coordinates"
        ]

        # Store route information

        state.route_distance_km = (
            distance_km
        )

        state.route_coordinates = (
            coordinates
        )

        # ==================================
        # DISTANCE RISK
        # ==================================

        route_risk = 0

        if distance_km > 20000:

            route_risk += 25

        elif distance_km > 15000:

            route_risk += 20

        elif distance_km > 10000:

            route_risk += 15

        elif distance_km > 5000:

            route_risk += 10

        else:

            route_risk += 5

        # ==================================
        # MARITIME CHOKEPOINT RISK
        # ==================================

        chokepoints_detected = []

        for lon, lat in coordinates:

            # Strait of Hormuz

            if (
                55 <= lon <= 58
                and
                24 <= lat <= 28
            ):

                if "Hormuz" not in chokepoints_detected:

                    chokepoints_detected.append(
                        "Hormuz"
                    )

                    route_risk += 20

            # Gulf of Aden

            if (
                43 <= lon <= 52
                and
                10 <= lat <= 16
            ):

                if "Gulf of Aden" not in chokepoints_detected:

                    chokepoints_detected.append(
                        "Gulf of Aden"
                    )

                    route_risk += 20

            # Red Sea

            if (
                32 <= lon <= 44
                and
                12 <= lat <= 30
            ):

                if "Red Sea" not in chokepoints_detected:

                    chokepoints_detected.append(
                        "Red Sea"
                    )

                    route_risk += 25

            # Suez Canal

            if (
                31 <= lon <= 33
                and
                29 <= lat <= 32
            ):

                if "Suez Canal" not in chokepoints_detected:

                    chokepoints_detected.append(
                        "Suez Canal"
                    )

                    route_risk += 15

            # Gulf of Guinea

            if (
                -10 <= lon <= 10
                and
                0 <= lat <= 10
            ):

                if "Gulf of Guinea" not in chokepoints_detected:

                    chokepoints_detected.append(
                        "Gulf of Guinea"
                    )

                    route_risk += 20

        # Cap route risk

        route_risk = min(
            route_risk,
            50
        )

        state.route_risk = (
            route_risk
        )

        state.route_details = f"""
SeaRoute Maritime Route

Origin:
{state.origin_port}

Destination:
{state.destination_port}

Distance:
{distance_km} km

Route Points:
{len(coordinates)}

Chokepoints Detected:
{", ".join(chokepoints_detected) if chokepoints_detected else "None"}

Route Risk:
{route_risk}
"""

    except Exception as e:

        state.route_distance_km = 0

        state.route_coordinates = []

        state.route_risk = 0

        state.route_details = (
            f"Route Analysis Failed: "
            f"{str(e)}"
        )

    return state