"use client"
import dynamic from 'next/dynamic'
//import { Circle, Tooltip } from "react-leaflet";

const Circle = dynamic(
    async () => (await import('react-leaflet')).Circle,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)



interface FloraRescueSpecieMapProps {
    data: FloraRescueSpeciesData[]; 
    radius?: number;
}

const FloraRescueSpecieMap: React.FC<FloraRescueSpecieMapProps> = ({
    data,
    radius
}) => {
    const lineOptions = {
        color: 'blue',
        weight:2,
    };

    return (
        <>
            {data.map((rescue, index) =>(
                <Circle
                    key={index}
                    pathOptions={lineOptions}
                    radius={radius? radius: 10}
                    center={[
                        rescue.rescue_area_latitude, rescue.rescue_area_longitude
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>Punto de rescate de flora</h4>
                            <p>Código: {rescue.epiphyte_number}</p>
                            {rescue.specie_name? <p>Especie recatada: {rescue.specie_name}</p>: <p>Especie recatada: No se ha identificado la especie</p>}
                            {!rescue.specie_name && rescue.genus_name ? <p>Genero de la especie: {rescue.genus_name}</p> : null }
                            {!rescue.specie_name && !rescue.genus_name && rescue.family_name ? <p>Familia de la especie: {rescue.family_name}</p>: null }
                        </div>
                    </Tooltip>
                </Circle>

            ))}
        </>

    )

}

export default FloraRescueSpecieMap; 
