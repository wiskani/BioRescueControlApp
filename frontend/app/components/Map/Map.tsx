import { MapContainer, TileLayer,Circle, Polyline } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import "leaflet-defaulticon-compatibility"
import { LineProyect } from './lineProyect'
import {LatLngExpression} from "leaflet";

interface MapProps {
    centers: LatLngExpression;
}

const Map:  React.FC<MapProps>= ({centers})  => {
    const lineOptions = { color: 'red' }
    return(
        <MapContainer
            center={[-17.489, -65.271]}
            zoom={12}
            scrollWheelZoom={false}
            className='h-80 w-full 2xl:h-[40rem] xl:h-[40rem] lg:h-[35rem]'
             >
                <TileLayer
                
                url={`https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`}
                attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                />
                <Polyline pathOptions={lineOptions} positions={LineProyect} />
            <Circle center={centers} radius={2} />
            </MapContainer>
    )
}

export default Map
