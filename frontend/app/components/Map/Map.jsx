import { MapContainer, TileLayer,Marker,Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import "leaflet-defaulticon-compatibility"

const Map = () => {
    return(
        <MapContainer
            center={[51.505, -0.09]}
            zoom={13}
            scrollWheelZoom={false}
            style={{height:"100%",  width:"100%"}}
             >
                <TileLayer
                
                url={`https://api.mapbox.com/styles/v1/wiskani/streets-v11/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoid2lza2FuaSIsImEiOiJjbGs4bG03ZDYwZ3d5M3JucGw5bWNyaTV0In0.-CdLlvt-RDogWVJU21pmew`}

                attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                />
            <Marker
                position={[51.505, -0.09]}
                draggable={true}
                animate={true}
                >
                    <Popup>
                        Mapa prueba
                    </Popup>
            </Marker>
            </MapContainer>
    )
}

export default Map
