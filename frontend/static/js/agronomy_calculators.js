/**
 * Agronomy Calculators Client Engine.
 * Provides client-side mathematical calculations for ET0, GDD, Sowing Rates, and Fertilizer Blending.
 */

const AgronomyCalculators = {
    calculatePenmanMonteithET0: function(tempMin, tempMax, rh, windSpeed, solarRad) {
        const tMean = (tempMin + tempMax) / 2.0;
        const eTmin = 0.61078 * Math.exp((17.27 * tempMin) / (tempMin + 237.3));
        const eTmax = 0.61078 * Math.exp((17.27 * tempMax) / (tempMax + 237.3));
        const es = (eTmin + eTmax) / 2.0;
        const ea = (rh / 100.0) * es;
        const delta = (4098.0 * (0.61078 * Math.exp((17.27 * tMean) / (tMean + 237.3)))) / Math.pow(tMean + 237.3, 2);
        const gamma = 0.066;

        const numerator = 0.408 * delta * 15.0 + gamma * (900.0 / (tMean + 273.0)) * windSpeed * (es - ea);
        const denominator = delta + gamma * (1.0 + 0.34 * windSpeed);
        return Math.max(0.1, (numerator / denominator)).toFixed(2);
    },

    calculateGDD: function(tempMin, tempMax, tBase, tMaxCutoff) {
        const minAdj = Math.max(tBase, Math.min(tempMin, tMaxCutoff));
        const maxAdj = Math.max(tBase, Math.min(tempMax, tMaxCutoff));
        const avg = (minAdj + maxAdj) / 2.0;
        return Math.max(0.0, avg - tBase).toFixed(1);
    },

    calculateSowingRate: function(targetPop, tgwGrams, germPct, purityPct) {
        const germFrac = Math.max(0.5, germPct / 100.0);
        const purFrac = Math.max(0.5, purityPct / 100.0);
        const rateKgHa = (targetPop * tgwGrams) / (germFrac * purFrac * 10000.0);
        return rateKgHa.toFixed(2);
    }
};
