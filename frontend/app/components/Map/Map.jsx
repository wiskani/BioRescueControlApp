import { MapContainer, TileLayer,Marker,Popup, Polyline } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import "leaflet-defaulticon-compatibility"
import { LineProyect } from './lineProyect'

const Map = () => {
        const lineOptions = { color: 'red' }
    return(
        <MapContainer
            center={[-17.655, -65.320]}
            zoom={13}
            scrollWheelZoom={false}
            style={{height:"100%",  width:"50%"}}
             >
                <TileLayer
                
                url={`https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`}
                attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                />
                <Polyline pathOptions={lineOptions} positions={LineProyect} />
            </MapContainer>
    )
}

export default Map