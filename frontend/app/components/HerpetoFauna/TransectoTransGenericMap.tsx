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
    data: TransectHerpetofaunaTranslocationData[];
    weight?: number;

}

const TransectTransloHerpetofaunaMap: React.FC<MapProps> = ({
    data,
    weight
}) => {
    const lineOptions = {
        color: 'blue',
        weight: weight? weight: 2,
    };

    return (
        <>
            {data.map((transect, index) => (
                <Polyline
                    key={index}
                    pathOptions={lineOptions}
                    positions={[
                        [transect.latitude_in, transect.longitude_in],
                        [transect.latitude_out, transect.longitude_out],
                    ]}
                >
                    <Tooltip>
                        <div>
                            <h4>Transector Herpetofauna</h4>
                            <p>Codigo: {transect.cod}</p>
                            <p>Fecha de liberación: {dateFormat(transect.date)}</p>
                        </div>
                    </Tooltip>
                </Polyline>
            ))}
        </>
    )
}

export default TransectTransloHerpetofaunaMap;

