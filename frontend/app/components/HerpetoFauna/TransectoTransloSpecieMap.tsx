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

interface TransectTransloHerpetofaunaMapProps {
    data: TransectHerpetoTransWithSpeciesData[];
}

const TransectTransloHerpetofaunaSpecieMap: React.FC<TransectTransloHerpetofaunaMapProps> = ({data}) => {
    const lineOptions = {
        color: 'blue',
        weight: 2,
    };

    const reduceSpecies = (species: string[]) => {
        const speciesSet = new Set(species);
        return Array.from(speciesSet);
    }


    return (
        <>
            {data.map((transect, index) => (
                <Polyline
                    key={index}
                    pathOptions={lineOptions}
                    positions={[
                        [
                            transect.latitude_in,
                            transect.longitude_in
                        ],
                        [
                            transect.latitude_out,
                            transect.longitude_out
                        ],
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Transector de liberación de Herpetofauna
                            </h4>
                            <p>Codigo: {transect.cod}</p>
                            <p>
                                Number individuos liberados: {
                                    transect.total_translocation
                                }
                            </p>
                            <p>Especies liberadas: </p>
                            <>
                                {
                                    reduceSpecies(transect.specie_names).map(
                                        (specie, index) => (
                                    <li key={index}>{index+1} {specie}</li>        
                                ))}
                            </>
                        </div>
                    </Tooltip>
                </Polyline>
            ))}
        </>
    )
}

export default TransectTransloHerpetofaunaSpecieMap;

