"use client"

import bannerHerpeto from "../../public/images/banner-herpeto.gif"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'

//React imports
import React, { useEffect, useState, useCallback } from "react"

//Apis imports
import { GetTransectHerpetofaunaWithSpecies } from '../libs/rescue_herpetofaina/ApiRescueHerpetofauna';
import { GetRescueFloraSpecie } from "../libs/rescue_flora/ApiRescueFlora";

//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

//Components imports
import { LineProyect } from '../components/Map/lineProyect';

//import with dynamic
const MapContainer = dynamic(
    async () => (await import('react-leaflet')).MapContainer,
    { ssr: false }
)

const TileLayer = dynamic(
    async () => (await import('react-leaflet')).TileLayer,
    { ssr: false }
)


const Polyline = dynamic(
    async () => (await import('react-leaflet')).Polyline,
    { ssr: false }
)

const Tooltip = dynamic(
    async () => (await import('react-leaflet')).Tooltip,
    { ssr: false }
)

const Legend = dynamic(
    () => (import('../components/Map/Legend')),
    { ssr: false }
)

const TransectHerpetofaunaSpecieMap = dynamic(
        () => (import('../components/Transectors/TransectoSpecieMap')),
        { ssr: false }
)


export default function HerpetoFauna() {
    const { data: session } = useSession();
    const [rescueFloraData, setRescueFloraData] = useState<FloraRescueSpeciesData[]>([]);
    const [transectData, setTransectData] = useState<TransectHerpetoWithSpecies[]>([])

    const user = session?.user;

    const transectDataHerpeto = useCallback(async (): Promise<TransectHerpetoWithSpecies[]>=>{
        if (user){
            const data= await GetTransectHerpetofaunaWithSpecies({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    const rescueDataFlora = useCallback(async (): Promise<FloraRescueSpeciesData[]>=>{
        if (user){
            const data= await GetRescueFloraSpecie({token: user?.token})
            return data
        }
        else{
            return []
        }
    }, [user])

    useEffect(() => {
        let cont = 0
        if (!session?.user) {
            if (cont <= 0){
                cont++
            }
            else{
                redirect('/')
            }
        }
        else{
            rescueDataFlora().then((data)=>{
                setRescueFloraData(data)
            })
            transectDataHerpeto().then((data)=>{
                setTransectData(data)
            })
        }
    }, [session, transectDataHerpeto, rescueDataFlora])


    const lineOptions = { color: 'red' }

    const legedColors = ['green', 'red' ]
    const legendLabels = [
        'Transcetors Herpetofauna',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    return (
        <div>
            <div
                className="w-full bg-cover bg-center"
                style={{
                    height: "28rem",
                    backgroundImage: `url(${bannerHerpeto.src})`,
                }}
            >
                <div
                    className="
                    flex
                    items-center
                    justify-center
                    h-full w-full
                    bg-gray-900
                    bg-opacity-50
                    "
                >
                    <div className="text-center">
                        <h1
                            className="
                            text-white
                            text-2xl
                            font-semibold
                            uppercase md:text-3xl"
                        >
                            Rescate de <
                                span className="text-emerald-400"
                            >
                               Herpetofauna 
                            </span>
                        </h1>
                    </div>
                </div>

            </div>
            <div
                className="
                flex
                flex-col
                h-full
                2xl:mb-52
                xl:mb-52
                lg:mb-40
                md:flex-row
                md:mb-0
                sm:mb-0
                justify-center"
            >
                <div className="
                    h-96
                    p-0
                    z-50
                    md:w-1/2
                    p-4 md:h-[16rem]
                    sd:h-[6rem]
                    "
                >
                    <MapContainer
                        center={[-17.489, -65.271]}
                        zoom={12}
                        scrollWheelZoom={false}
                        className='
                        h-80
                        w-full
                        2xl:h-[40rem]
                        xl:h-[40rem]
                        lg:h-[35rem]
                        '
                    >
                        <TileLayer

                            url={
                                `https://api.mapbox.com/styles/v1/mapbox/streets-v12/tiles/256/{z}/{x}/{y}@2x?access_token=${process.env.NEXT_PUBLIC_MAPBOX_TOKEN}`
                            }
                            attribution='Map data &copy; <a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors, <a href=&quot;https://creativecommons.org/licenses/by-sa/2.0/&quot;>CC-BY-SA</a>, Imagery &copy; <a href=&quot;https://www.mapbox.com/&quot;>Mapbox</a>'
                        />
                        <TransectHerpetofaunaSpecieMap data={transectData}/>
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                           <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer> 
                    
                </div>
            </div>
        </div>


    )
}
