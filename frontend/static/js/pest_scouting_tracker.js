/**
 * Insect Pest Scouting & Economic Threshold Client Tracker.
 */

const PestScoutingTracker = {
    evaluatePestDensity: function(scoutedCount, squareMeters, ethresh) {
        const density = (scoutedCount / squareMeters).toFixed(2);
        const actionNeeded = parseFloat(density) >= parseFloat(ethresh);

        return {
            pestDensityM2: density,
            actionRequired: actionNeeded,
            statusBadgeClass: actionNeeded ? 'badge bg-danger' : 'badge bg-success',
            statusMessage: actionNeeded ? 'ALERT: Scouted density exceeds Economic Threshold!' : 'Pest population is within safe threshold.'
        };
    }
};
