from typing import Dict


class DisputeWarningService:

    def analyze(
        self,
        dispute_count: int,
        dispute_growth_percentage: float,
        land_use_change_percentage: float,
        population_growth_percentage: float,
        anomaly_detected: bool
    ) -> Dict:

        if dispute_count < 0:
            raise ValueError(
                "Dispute count cannot be negative."
            )

        indicators = []

        risk_score = 0.0

        # -----------------------------------------
        # Dispute frequency
        # -----------------------------------------

        if dispute_count >= 100:
            risk_score += 0.30
            indicators.append(
                "High number of recorded land disputes."
            )

        elif dispute_count >= 50:
            risk_score += 0.20
            indicators.append(
                "Moderate number of recorded land disputes."
            )

        elif dispute_count > 0:
            risk_score += 0.10
            indicators.append(
                "Land disputes have been recorded."
            )

        # -----------------------------------------
        # Dispute growth
        # -----------------------------------------

        if dispute_growth_percentage >= 50:
            risk_score += 0.25
            indicators.append(
                "Land disputes are increasing rapidly."
            )

        elif dispute_growth_percentage >= 20:
            risk_score += 0.15
            indicators.append(
                "Land disputes show an increasing trend."
            )

        # -----------------------------------------
        # Land-use change
        # -----------------------------------------

        if land_use_change_percentage >= 30:
            risk_score += 0.20
            indicators.append(
                "Significant land-use change detected."
            )

        elif land_use_change_percentage >= 10:
            risk_score += 0.10
            indicators.append(
                "Moderate land-use change detected."
            )

        # -----------------------------------------
        # Population pressure
        # -----------------------------------------

        if population_growth_percentage >= 30:
            risk_score += 0.15
            indicators.append(
                "High population growth may increase "
                "land-use pressure."
            )

        elif population_growth_percentage >= 10:
            risk_score += 0.10
            indicators.append(
                "Population growth may increase "
                "land-use pressure."
            )

        # -----------------------------------------
        # Anomaly signal
        # -----------------------------------------

        if anomaly_detected:
            risk_score += 0.10

            indicators.append(
                "Anomalous activity was detected "
                "in the underlying data."
            )

        # -----------------------------------------
        # Clamp score
        # -----------------------------------------

        risk_score = min(
            round(risk_score, 2),
            1.0
        )

        # -----------------------------------------
        # Risk level
        # -----------------------------------------

        if risk_score >= 0.70:

            risk_level = "High"

        elif risk_score >= 0.40:

            risk_level = "Moderate"

        else:

            risk_level = "Low"

        # -----------------------------------------
        # Warning
        # -----------------------------------------

        if risk_level == "High":

            warning = (
                "Early-warning indicators suggest "
                "a high potential for land-dispute "
                "pressure. Further investigation "
                "is recommended."
            )

        elif risk_level == "Moderate":

            warning = (
                "Early-warning indicators suggest "
                "moderate land-dispute pressure. "
                "The affected area should be monitored."
            )

        else:

            warning = (
                "No strong land-dispute early-warning "
                "signal was detected from the supplied "
                "indicators."
            )

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "warning": warning,
            "indicators": indicators,
            "anomaly_detected": anomaly_detected
        }