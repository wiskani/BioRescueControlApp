'use client'

import { useMap } from "react-leaflet";
import L from "leaflet";
import { useEffect } from "react";

interface LegendProps {
    colors: string[];
    labels: string[];
}

const Legend: React.FC<LegendProps> = ({colors, labels}) => {
    const map = useMap();

    useEffect(() => {
        const legendConstrol = new L.Control({position: 'bottomright'});
        legendConstrol.onAdd = () => {
            const div = L.DomUtil.create('div', 'info legend bg-white p-4 border border-gray-300');

            colors.forEach((color, i) => {
                div.innerHTML +=
                    '<i class="block w-4 h-4 mr-2 float-left" style="background: ' + color + '"></i>' +
                    '<span class="opacity-70">' + (labels[i] || '') + '</span><br>';
            });

            return div;
        }
        legendConstrol.addTo(map);

        return () => {
            legendConstrol.remove();
        }
    }, [colors, labels, map]);

    return null;

}

export default Legend;

