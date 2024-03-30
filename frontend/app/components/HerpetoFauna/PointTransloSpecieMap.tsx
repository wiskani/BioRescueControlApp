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

interface PointTransloHerpetofaunaMapProps {
    data: PointHerpetoTransloWithSpeciesData[];
}

const PointTransloHerpetofaunaSpecieMap: React.FC<PointTransloHerpetofaunaMapProps> = ({data}) => {
    const lineOptions = {
        color: 'purple',
        weight: 2,
    };

    const reduceSpecies = (species: string[]) => {
        const speciesSet = new Set(species);
        return Array.from(speciesSet);
    }


    return (
        <>
            {data.map((point, index) => (
                <Circle
                    key={index}
                    pathOptions={lineOptions}
                    radius={10}
                    center={[

                        point.latitude,
                        point.longitude

                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Punto de liberación de Herpetofauna
                            </h4>
                            <p>Codigo: {point.cod}</p>
                            <p>
                                Number individuos liberados: {
                                    point.total_translocation
                                }
                            </p>
                            <p>Especies liberadas: </p>
                            <>
                                {
                                    reduceSpecies(point.specie_names).map(
                                        (specie, index) => (
                                            <li key={index}>{index+1} {specie}</li>        
                                        ))}
                            </>
                        </div>
                    </Tooltip>
                </Circle>
            ))}
        </>
    )
}

export default PointTransloHerpetofaunaSpecieMap;

