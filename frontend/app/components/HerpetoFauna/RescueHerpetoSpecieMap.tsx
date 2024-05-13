"use client"
import dynamic from 'next/dynamic'

const Polyline = dynamic(
    async () => (await import('react-leaflet')).Polyline,
    { ssr: false }
)


const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

interface RescueHerpetoMapProps {
    data: RescueHerpetoWithSpeciesData[];
}

const RescueHerpetoSpecieMap: React.FC<RescueHerpetoMapProps> = ({data}) => {
    const lineOptions = {
        color: 'green',
        weight: 3,
    };

    return (
        <>
            {data.map((rescue, index) => (
                <Polyline
                    key={index}
                    pathOptions={lineOptions}
                    positions={[
                        [
                            rescue.latitude_in,
                            rescue.longitude_in
                        ],
                        [
                            rescue.latitude_out,
                            rescue.longitude_out
                        ],
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Transector de rescate
                            </h4>
                            <p>Codigo: {rescue.number}</p>
                            <p>Especies liberadas: {rescue.specie_name} </p>
                        </div>
                    </Tooltip>
                </Polyline>
            ))}
        </>
    )
}

export default RescueHerpetoSpecieMap;

