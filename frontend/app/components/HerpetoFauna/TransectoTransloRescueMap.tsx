"use client"
import dynamic from 'next/dynamic'

//service imports
import { dateFormat } from '@/app/services/dateFormat';

const Polyline = dynamic(
    async () => (await import('react-leaflet')).Polyline,
    { ssr: false }
)


const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

interface MapProps {
    data: TransectTranslocationHerpetoWithMarkData;
    weight?: number;

}

const TransectTransloHerpetofaunaRescueMap: React.FC<MapProps> = ({
    data,
    weight
}) => {
    const lineOptions = {
        color: 'blue',
        weight: weight? weight: 2,
    };

    let dateTranslo = dateFormat(data.date);


    return (
        <>
                <Polyline
                    pathOptions={lineOptions}
                    positions={[
                        [
                            data.latitude_in,
                            data.longitude_in
                        ],
                        [
                            data.latitude_out,
                            data.longitude_out
                        ],
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>
                                Transector de liberación de Herpetofauna
                            </h4>
                            <p>Codigo: {data.cod}</p>
                            <p>
                                Fecha de liberación: {
                                   dateTranslo 
                                }
                            </p>
                        </div>
                    </Tooltip>
                </Polyline>
            
        </>
    )
}

export default TransectTransloHerpetofaunaRescueMap;

