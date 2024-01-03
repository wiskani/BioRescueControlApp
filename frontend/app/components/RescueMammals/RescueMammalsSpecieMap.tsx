import { Circle, Tooltip } from "react-leaflet";

interface RescueMammalsWithSpecieMapProps {
        data: RescueMammalsWithSpecieData[]; 
        }

const RescueMammalsSpecieMap: React.FC<RescueMammalsWithSpecieMapProps> = ({data}) => {
        const lineOptions = {
                color: 'brown',
                weight:2,
                };

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
                                                <h4>Punto de rescate de mastozoología</h4>
                                                <p>Código: {rescue.cod}</p>
                                                {rescue.specie_name? <p>Especie recatada: {rescue.specie_name}</p>: <p>Especie recatada: No se ha identificado la especie</p>}
                                                {!rescue.specie_name ? <p> Género identificado: {rescue.genus_name}</p>: null}
                                        </div>
                                </Tooltip>
                        </Circle>

                        ))}
        </>

        )

        }

export default RescueMammalsSpecieMap
