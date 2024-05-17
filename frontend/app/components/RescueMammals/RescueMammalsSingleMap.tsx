"use client"
import dynamic from 'next/dynamic'
import { dateFormat } from "@/app/services/dateFormat";
//import { Circle, Tooltip } from "react-leaflet";
const Circle = dynamic(
    async () => (await import('react-leaflet')).Circle,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

interface RescueMammalsWithSpecieMapProps {
    data: RescueMammalsWithSpecieExtendedData; 
    radius?: number;
}

const RescueMammalsSingleMap: React.FC<RescueMammalsWithSpecieMapProps> = ({
    data,
    radius
}) => {
    const lineOptions = {
        color: 'brown',
        weight:2,
    };

    return (
        <>
                <Circle
                    pathOptions={lineOptions}
                    radius={radius || 10}
                    center={[
                        data.latitude, data.longitude
                    ]}
                >
                    <Tooltip>
                    <div>
                        <h4>
                            Punto de rescate de mastozoología
                        </h4>
                        <p>Código: {data.cod}</p>
                        {
                            data.specie_name?
                                <p>Especie recatada: {
                                    data.specie_name
                                }</p>:
                                <p>Especie recatada: No se ha identificado la especie</p>
                        }
                        {
                            !data.specie_name ?
                                <p> Género identificado: {data.genus_name}</p>:
                                null
                        }
                        <p>Fecha de rescate: {dateFormat(data.date)}</p>
                    </div>
                </Tooltip>
            </Circle>

        </>

    )

}

export default RescueMammalsSingleMap
