"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation';

//React imports
import React, { useEffect, useState, useCallback } from "react"

//Apis imports
import {
   GetRescueFloraSpecieByEpiphyteNumber, 
   GetRelocationFloraSpecieByEpiphyteNumber,
} from '../../../libs/rescue_flora/ApiRescueFlora';


//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'


//Components imports
import { LineProyect } from '../../../components/Map/lineProyect';
import Loading from '../../loading';
import { dateFormat } from "../../../services/dateFormat";

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
    () => (import('../../../components/Map/Legend')),
    { ssr: false }
)

const FloraRescueSpecieMap = dynamic(
    () => (import('../../../components/RescueFlora/rescueFloraSpecieMap')),
    { ssr: false }
)

const FloraRelocationSpecieMap = dynamic(
    () => (import('../../../components/RescueFlora/relocationFloraSpecieMap')),
    { ssr: false }
)


//Types
interface FloraColumns extends FloraRescueSpeciesData{
    ver: string;
}


export default function Page({ params} : { params: { numberEpiphyte: string } }) {
    const { data: session } = useSession();
    const [rescueFloraData, setRescueFloraData] = useState<FloraRescueSpeciesData | null>(null);
    const [
    relocationFloraData,
    setRelocationFloraData
] = useState<FloraRelocationWithSpecieData | {message: string} | null>(null);
    const [errorMessage, SetErrorMessage]= useState<string>();
    const router = useRouter();

    const user = session?.user;


    const rescueDataFlora = useCallback(
        async (): Promise<FloraRescueSpeciesData | null>=>{
            if (user){
                try {
                    const data= await GetRescueFloraSpecieByEpiphyteNumber({
                        token: user?.token,
                        epiphyte_number: params.numberEpiphyte
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        SetErrorMessage(error.message)
                        return null;
                    }
                    return null;
                }
            }
            else {
                return null
            }
        }, [user, params.numberEpiphyte])

    const relocationDataFlora = useCallback(
        async (): Promise<FloraRelocationWithSpecieData | {message:string} | null>=>{
            if (user){
                try {
                    const data= await GetRelocationFloraSpecieByEpiphyteNumber({
                        token: user?.token,
                        epiphyte_number: params.numberEpiphyte
                    });
                    return data
                } catch (error) {
                    if (error instanceof Error) {
                        SetErrorMessage(error.message)
                        return null;
                    }
                    return null;
                }
            }
            else{
                return null
            }
        }, [user, params.numberEpiphyte])

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else{
            rescueDataFlora().then((data)=>{
                setRescueFloraData(data)
            })
            relocationDataFlora().then((data)=>{
                setRelocationFloraData(data)
            })
        }
    }, [session, rescueDataFlora, relocationDataFlora])


    const lineOptions = { color: 'red' }

    const legedColors = ['purple','blue', 'red' ]
    const legendLabels = [
        'Puntos de relocalización de Flora',
        'Puntos Rescates de Flora',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]

    return (
        <div>
            <div
                className="
                flex
                flex-col
                h-full
                2xl:mb-52
                xl:mb-52
                lg:mb-52
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
                        <Polyline pathOptions={lineOptions} positions={LineProyect} >
                            <Tooltip>
                                <div>
                                    <h4>Detalles</h4>
                                    <p>Proyecto 230 kV Mizque - Sehuencas</p>
                                </div>
                            </Tooltip>
                        </Polyline>
                        {
                            rescueFloraData? <FloraRescueSpecieMap data={[rescueFloraData]}/> : null
                        }
                        <FloraRelocationSpecieMap data={relocationFloraData} radius={12}/>
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer>
                </div>
                <div className='
                    md:w-1/2
                    p-4 h-144
                    flex
                    justify-center
                    items-center
                    2xl:h-144
                    xl:h-128
                    md:h-96
                    sm:h-80
                    '
                >

                </div>
            </div>
        </div>


    )
}
