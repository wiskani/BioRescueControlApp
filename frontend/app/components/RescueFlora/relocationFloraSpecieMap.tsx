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



interface FloraRelocationSpecieMapProps {
    data: FloraRelocationWithSpecieData[]; 
    radius?: number;
}

const FloraRelocationSpecieMap: React.FC<FloraRelocationSpecieMapProps> = ({data, radius}) => {
    const lineOptions = {
        color: 'purple',
        weight:2,
    };

    return (
        <>
            {data.map((relocation, index) =>(
                <Circle
                    key={index}
                    pathOptions={lineOptions}
                    radius={radius? radius: 10}
                    center={[
                        relocation.relocation_position_latitude,
                        relocation.relocation_position_longitude
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>Punto de rescate de flora</h4>
                            <p>Código: {relocation.flora_rescue}</p>
                            {
                                relocation.specie_name_epiphyte?
                                    <p>
                                        Especie recatada: {
                                            relocation.specie_name_epiphyte
                                        }
                                    </p>:
                                    <p>
                                        Especie recatada: No se ha identificado la especie
                                    </p>
                            }
                            {
                                !relocation.specie_name_epiphyte && relocation.genus_name_epiphyte ?
                                    <p>Genero de la especie: {relocation.genus_name_epiphyte}</p> :
                                    null
                            }
                            {
                                !relocation.specie_name_epiphyte && !relocation.genus_name_epiphyte && relocation.family_name_epiphyte ?
                                    <p>Familia de la especie: {relocation.family_name_epiphyte}</p>:
                                    null
                            }
                        </div>
                    </Tooltip>
                </Circle>

            ))}
        </>

    )

}

export default FloraRelocationSpecieMap; 
