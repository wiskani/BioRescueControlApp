import {Polyline, Tooltip} from 'react-leaflet';

interface TransectHerpetofaunaMapProps {
        data: TransectHerpetoWithSpecies[];
}

const TransectHerpetofaunaMap: React.FC<TransectHerpetofaunaMapProps> = ({data}) => {
        const lineOptions = {
                color: 'green',
                weight: 2,
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
                                                <p>Number individuos rescatados: {transect.total_rescue}</p>
                                                <p>Especies rescatadas: </p>
                                                <>
                                                {transect.specie_names.map((specie, index) => (
                                                        <li>{index+1} {specie}</li>        
                                                ))}
                                                </>
                                        </div>
                                </Tooltip>
                        </Polyline>
                        ))}
        </>
                )
}

export default TransectHerpetofaunaMap;

