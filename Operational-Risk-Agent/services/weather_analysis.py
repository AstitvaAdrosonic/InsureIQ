import requests


async def weather_analysis(state):

    try:

        route_points = state.route_coordinates

        if not route_points:

            state.weather_details = (
                "No route coordinates available."
            )

            state.weather_risk = 0

            return state

        # ==================================
        # SAMPLE ROUTE POINTS
        # ==================================

        sample_size = min(
            15,
            len(route_points)
        )

        step = max(
            1,
            len(route_points) // sample_size
        )

        sampled_points = route_points[::step]

        max_wave = 0

        avg_wave_values = []

        dangerous_locations = []

        severe_points = 0

        # ==================================
        # CHECK WEATHER ALONG ROUTE
        # ==================================

        for lon, lat in sampled_points:

            try:

                url = (
                    "https://marine-api.open-meteo.com/v1/marine"
                    f"?latitude={lat}"
                    f"&longitude={lon}"
                    "&hourly=wave_height"
                )

                response = requests.get(
                    url,
                    timeout=15
                )

                response.raise_for_status()

                data = response.json()

                waves = (
                    data.get("hourly", {})
                    .get("wave_height", [])
                )

                if not waves:
                    continue

                avg_wave = round(
                    sum(waves[:24]) /
                    min(24, len(waves)),
                    2
                )

                local_max_wave = round(
                    max(waves[:24]),
                    2
                )

                avg_wave_values.append(
                    avg_wave
                )

                if local_max_wave > max_wave:

                    max_wave = local_max_wave

                if local_max_wave >= 4:

                    severe_points += 1

                    dangerous_locations.append(
                        f"Lat {round(lat,2)}, "
                        f"Lon {round(lon,2)} "
                        f"({local_max_wave}m)"
                    )

            except Exception:

                continue

        # ==================================
        # AGGREGATION
        # ==================================

        overall_avg_wave = 0

        if avg_wave_values:

            overall_avg_wave = round(
                sum(avg_wave_values)
                /
                len(avg_wave_values),
                2
            )

        # ==================================
        # WEATHER RISK MODEL
        # ==================================

        risk = 0

        if max_wave >= 7:

            risk += 25

        elif max_wave >= 5:

            risk += 20

        elif max_wave >= 4:

            risk += 15

        elif max_wave >= 3:

            risk += 10

        if overall_avg_wave >= 4:

            risk += 10

        elif overall_avg_wave >= 3:

            risk += 5

        if severe_points >= 5:

            risk += 10

        elif severe_points >= 3:

            risk += 5

        risk = min(
            risk,
            40
        )

        state.weather_risk = risk

        state.weather_details = f"""
Marine Route Weather Analysis

Route Points Sampled:
{len(sampled_points)}

Average Wave Height:
{overall_avg_wave} m

Maximum Wave Height:
{max_wave} m

Severe Weather Points:
{severe_points}

High Risk Locations:
{chr(10).join(dangerous_locations[:10])}

Weather Risk:
{risk}
"""

    except Exception as e:

        state.weather_details = (
            f"Weather analysis failed: "
            f"{str(e)}"
        )

        state.weather_risk = 0

    return state