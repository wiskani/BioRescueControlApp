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

interface MapProps {
    data: ReleaseMammalsWithSpecieData; 
    radius?: number;
}

const ReleaseMammalsSpecieMap: React.FC<MapProps> = ({
    data,
    radius
}) => {
    const lineOptions = {
        color: 'purple',
        weight:2,
    };


    return (
        {
            data.longitude && data.latitude ?
        <>
                <Circle
                    pathOptions={lineOptions}
                    radius={radius || 10}
                    center={[
                        data.latitude,
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

        </>
        :
        null
        }

    )

}

export default ReleaseMammalsSpecieMap

