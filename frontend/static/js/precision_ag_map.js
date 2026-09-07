/**
 * Precision Agriculture Spatial Grid & VRA Map Client Visualizer.
 */

class PrecisionAgMapVisualizer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
    }

    renderGridZones(zones) {
        if (!this.container) return;
        let html = '<div class="row g-2">';
        zones.forEach(z => {
            const color = z.vigor_index_ndvi > 0.6 ? '#16a34a' : (z.vigor_index_ndvi > 0.4 ? '#eab308' : '#dc2626');
            html += `
                <div class="col-3">
                    <div class="p-3 text-white text-center rounded-3 shadow-sm" style="background-color: ${color}">
                        <div class="fw-bold">${z.zone_id}</div>
                        <small>NDVI: ${z.vigor_index_ndvi}</small><br/>
                        <span class="badge bg-light text-dark mt-1">${z.recommended_n_rate_kg_ha} kg/ha N</span>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        this.container.innerHTML = html;
    }
}
