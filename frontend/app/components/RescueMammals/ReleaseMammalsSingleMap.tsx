"use client"
import { useState, useEffect} from 'react'
import dynamic from 'next/dynamic'

//service imports
import { dateFormat } from '@/app/services/dateFormat';

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

const ReleaseMammalsSingleMap: React.FC<MapProps> = ({
    data,
    radius
}) => {
    const lineOptions = {
        color: 'purple',
        weight:2,
    };


    return (
        
            data.longitude && data.latitude ?
        <>
                <Circle
                    pathOptions={lineOptions}
                    radius={radius || 10}
                    center={[
                        data.latitude,
                        data.longitude
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Punto de liberación de mastozoología
                            </h4>
                            <p>Código: {data.cod}</p>
                            {
                                data.specie_name?
                                    <p>Especie: {
                                        data.specie_name
                                    }</p>:
                                    <p>Especie: No se ha identificado la especie</p>
                            }
                            {
                                !data.specie_name ?
                                    <p> Género identificado: {data.genus_name}</p>:
                                    null
                            }
                            {
                                data.sustrate?
                                    <p>Sustrato: {data.sustrate}</p>:
                                    <p>Sustrato: No se ha identificado el sustrato</p>
                            }
                            {
                                data.site_release_mammals?
                                    <p>Ubicación: {data.site_release_mammals}</p>:
                                    <p>Ubicación: No se ha identificado la ubicación</p>
                            }
                        </div>
                    </Tooltip>
                </Circle>

        </>
        :
        null

    )

}

export default ReleaseMammalsSingleMap

