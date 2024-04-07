"use client"
import dynamic from 'next/dynamic'

const Circle = dynamic(
    async () => (await import('react-leaflet')).Circle,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

interface RealeaseMammalsWithSpecieMapProps {
    data: RescueMammalsWithSpecieData[]; 
}

const RealeaseMammalsSpecieMap: React.FC<RealeaseMammalsWithSpecieMapProps> = ({data}) => {
    const lineOptions = {
        color: 'purple',
        weight:2, };

    return (
        <>
            {data.map((rescue, index) =>(
                <Circle
                    key={index}
                    pathOptions={lineOptions}
                    radius={10}
                    center={[
                        rescue.latitude, rescue.longitude
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Punto de liberación de mastozoología
                            </h4>
                            <p>Código: {rescue.cod}</p>
                            {
                                rescue.specie_name?
                                    <p>Especie: {
                                        rescue.specie_name
                                    }</p>:
                                    <p>Especie: No se ha identificado la especie</p>
                            }
                            {
                                !rescue.specie_name ?
                                    <p> Género identificado: {rescue.genus_name}</p>:
                                    null
                            }
                        </div>
                    </Tooltip>
                </Circle>

            ))}
        </>

    )

}

export default RealeaseMammalsSpecieMap
