"use client"
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
    data: PointTranslocationHerpetoWithMarkData;
    radius?: number;
}

const PointTransloHerpetofaunaRescueMap: React.FC<MapProps> = ({
    data,
    radius
}) => {
    const lineOptions = {
        color: 'blue',
        weight: 2,
    };
    
    let dateTranslo = dateFormat(data.date);

    return (
        <>
            <Circle
                pathOptions={lineOptions}
                radius={radius? radius: 10}
                center={[

                    data.latitude,
                    data.longitude

                ]}
            >
                <Tooltip>
                    <div>
                        <h4>
                            Punto de liberación de Herpetofauna
                        </h4>
                        <p>Codigo: {data.cod}</p>
                        <p>
                            Fecha de liberación: {
                               dateTranslo
                            }
                        </p>
                    </div>
                </Tooltip>
            </Circle>
        </>
    )
}

export default PointTransloHerpetofaunaRescueMap;

