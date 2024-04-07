"use client"
import { useState, useEffect} from 'react'
import dynamic from 'next/dynamic'

const Circle = dynamic(
    async () => (await import('react-leaflet')).Circle,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

interface ReleaseMammalsWithSpecieMapProps {
    data: ReleaseMammalsWithSpecieData[]; 
}

interface ReleaseWithCoordinates extends Omit<ReleaseMammalsWithSpecieData, 'longitude' | 'latitude'> {
    longitude: number;
    latitude: number;
}

const ReleaseMammalsSpecieMap: React.FC<ReleaseMammalsWithSpecieMapProps> = ({data}) => {
    const [filteredData, setFilteredData] = useState<ReleaseWithCoordinates[]>([])
    const lineOptions = {
        color: 'purple',
        weight:2, };

    const handleFilterData = (
        data: ReleaseMammalsWithSpecieData[]
    ): ReleaseWithCoordinates[] => {
        return data.filter((release) => release.longitude && release.latitude).map((release) => ({
        ...release,
        longitude: release.longitude!,
        latitude: release.latitude!
        }))
    }

    useEffect(() => {
        setFilteredData(handleFilterData(data))
    }, [data])

        


    return (
        <>
            {filteredData.map((release, index) =>(
                <Circle
                    key={index}
                    pathOptions={lineOptions}
                    radius={10}
                    center={[
                        release.latitude,
                        release.longitude
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Punto de liberación de mastozoología
                            </h4>
                            <p>Código: {release.cod}</p>
                            {
                                release.specie_name?
                                    <p>Especie: {
                                        release.specie_name
                                    }</p>:
                                    <p>Especie: No se ha identificado la especie</p>
                            }
                            {
                                !release.specie_name ?
                                    <p> Género identificado: {release.genus_name}</p>:
                                    null
                            }
                            {
                                release.sustrate?
                                    <p>Sustrato: {release.sustrate}</p>:
                                    <p>Sustrato: No se ha identificado el sustrato</p>
                            }
                            {
                                release.site_release_mammals?
                                    <p>Ubicación: {release.site_release_mammals}</p>:
                                    <p>Ubicación: No se ha identificado la ubicación</p>
                            }
                        </div>
                    </Tooltip>
                </Circle>

            ))}
        </>

    )

}

export default ReleaseMammalsSpecieMap
