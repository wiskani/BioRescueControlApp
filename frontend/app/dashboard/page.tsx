"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';

//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Apis imports
import { ApiRescueFlora } from "../api/rescue_flora/route";
import { ApiTransectHerpetofaunaWithSpecies } from '../api/rescue_herpetofaina/route';
import { SpeciesItem } from '../api/species/route';

//Leaflet imports
import { MapContainer, TileLayer,Circle, Polyline, Tooltip } from 'react-leaflet'
import {LatLngExpression} from "leaflet";
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'
import "leaflet-defaulticon-compatibility"

//Components imports
import SpecieList from '../components/Species/SpecieList';
import TransectHerpetofaunaMap from '../components/Transectors/Transecto';
import { LineProyect } from '../components/Map/lineProyect';
import Legend from '../components/Map/Legend';


export default function Dashboard() {
    const { data: session } = useSession();
    const [centers, setCenters] = useState<LatLngExpression[]>([]);
    const [specieData, setSpecieData] = useState<SpecieItemData[]>([])
    const [transectData, setTransectData] = useState<TransectHerpetoWithSpecies[]>([])

    const user = session?.user;

    const rescueDataFlora = useCallback(async (): Promise<LatLngExpression[]>=>{
      if (user){
       const data= await ApiRescueFlora({token: user?.token})
       return data.map((item:FloraRescueData)=>[item.rescue_area_latitude, item.rescue_area_longitude] )
      }
      else{
        return []
      }
    }, [user])
    
    const speciesData = useCallback(async (): Promise<SpecieItemData[]>=>{
        if (user){
            const data= await SpeciesItem({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const transectDataHerpeto = useCallback(async (): Promise<TransectHerpetoWithSpecies[]>=>{
        if (user){
            const data= await ApiTransectHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else{
            rescueDataFlora().then((data)=>{
                setCenters(data)
            })
            speciesData().then((data)=>{
                setSpecieData(data)
            })
            transectDataHerpeto().then((data)=>{
                setTransectData(data)
            })

        }

    }, [session, rescueDataFlora, speciesData])


    const lineOptions = { color: 'red' }

    const legedColors = ['green', 'blue', 'red' ]
    const legendLabels = ['Transcetors Herpetofauna', 'Puntos Rescates de Flora', 'Proyecto 230 kV Mizque - Sehuencas']
        return (
            <div>
                <div className="flex flex-col  h-96 2xl:mb-52 xl:mb-52 lg:mb-40 md:flex-row md:mb-0 sm:mb-0 justify-center">
                    <div className="h-full p-0 z-50 md:w-1/2 p-4 md:h-[16rem] sd:h-[6rem]">
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
                                <TransectHerpetofaunaMap data={transectData}/>
                                <Polyline pathOptions={lineOptions} positions={LineProyect} >
                                        <Tooltip>
                                                <div>
                                                <h4>Detalles</h4>
                                                <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                                </div>
                                        </Tooltip>
                                </Polyline>
                                {centers.map((center, index) => (
                                    <Circle key={index} center={center} pathOptions={{color: 'blue'}} radius={10} />
                                ))}

                            <Legend colors={legedColors} labels={legendLabels} />

                            </MapContainer>
                    </div>
                    <div className='md:w-1/2 p-4'>
                        <h1> Hola datos </h1>
                    </div>
                </div>
                    <SpecieList species={specieData}  />

            </div>
        )

}
