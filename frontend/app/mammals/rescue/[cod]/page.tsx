"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation';

//React imports
import React, {
    useEffect,
    useState,
    useCallback
} from "react"

//Apis imports
import {
    GetRescueMammalsWithSpecieByNumber,
    GetReleaseMammalsWithSpecieByNumber
} from '@/app/libs/rescue_mammals/ApiRescueMammalsWithSpecies';

//Leaflet imports
import 'leaflet/dist/leaflet.css'
import 'leaflet-defaulticon-compatibility/dist/leaflet-defaulticon-compatibility.css'

//Components imports
import { LineProyect } from '@/app/components/Map/lineProyect';
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
    () => (import('@/app/components/Map/Legend')),
    { ssr: false }
)

const RescueMammalsSingleMap = dynamic(
    () => (import('@/app/components/RescueMammals/RescueMammalsSingleMap')),
    { ssr: false }
) 

const ReleaseMammalsSingleMap = dynamic(
    () => (import('@/app/components/RescueMammals/ReleaseMammalsSingleMap')),
    { ssr: false }
)

export default function Page({params}: {params: { cod: string}}) {   
    const { data: session } = useSession();
    const user = session?.user;
    const [rescueData, setRescueData] = useState<RescueMammalsWithSpecieExtendedData | null>(null)
    const [
    releaseData,
    setReleaseData
            ] = useState<ReleaseMammalsWithSpecieData| null>(null)
    const [errorMessage, SetErrorMessage]= useState<string>();
    const router = useRouter()

    //Api calls
    const rescueDataMammals = useCallback(
        async (): Promise<RescueMammalsWithSpecieExtendedData | null>=>{
            if (user){
                try {
                    const data= await GetRescueMammalsWithSpecieByNumber({
                        token: user?.token,
                        cod: params.cod
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
        }, [user, params.cod])


    const releaseDataMammals = useCallback(
        async (): Promise<ReleaseMammalsWithSpecieData| null> =>{
            if (user){
                try {
                    const data= await GetReleaseMammalsWithSpecieByNumber({
                        token: user?.token,
                        cod: params.cod
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        SetErrorMessage(error.message)
                    }
                    return null;
                }
            }
            else {
                return null
            }
        }, [user, params.cod])

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }

        else{
            rescueDataMammals().then((data)=>{
                setRescueData(data)
            })
            releaseDataMammals().then((data)=>{
                setReleaseData(data)
            })
        }

    }, [session])


    //Map options

    const lineOptions = { color: 'red' }

    const legedColors = ['purple','brown', 'red' ]
    const legendLabels = [
        'Punto de liberación',
        'Puntos de rescate',
        'Proyecto 230 kV Mizque - Sehuencas'
    ]


    return (
        <div>
            <h1
                className="
                m-4
                text-gl
                text-center
                font-bold
                leading-none
                tracking-tight
                text-gray-600
                md:text-xl
                lg:text-xl
                dark:text-white
                "
            >Rescate y liberación para el rescate:&nbsp;
                <span
                    className='italic'
                >
                    {params.cod}
                </span>
            </h1>
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
                    2xl:mb-52
                    xl:mb-52
                    lg:mb-40
                    md:w-1/2
                    p-4
                    md:h-[16rem]
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
                            rescueData?
                                <RescueMammalsSingleMap 
                                    data={rescueData}
                                    radius={55}
                                /> :
                                null
                        }
                        {
                            releaseData?
                                <ReleaseMammalsSingleMap
                                    data={releaseData}
                                    radius={55}
                                /> :
                                null
                        }
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer> 
                </div>
            </div>
            <div className="container mx-auto px-4 py-20">
                <div className="
                    grid
                    grid-cols-1
                    sm:grid-cols-2
                    md:grid-cols-2
                    lg:grid-cols-2
                    gap-4"
                >
                    <div className="w-full mt-6">
                        <h1
                            className="
                            text-gray-900
                            text-xl
                            text-center
                            title-font
                            font-medium
                            mb-5
                            "
                        >
                            Datos de rescate 
                        </h1>
                        <ol className="
                            max-w-md
                            space-y-1
                            text-gray-500
                            list-decimal
                            list-inside
                            dark:text-gray-400"
                        >
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Fecha de rescate:&nbsp; 
                                </span>
                                {
                                    rescueData?.date?
                                        dateFormat(rescueData.date):
                                        'No disponible'
                                }

                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Especie:&nbsp; 
                                </span>
                                {
                                    rescueData?.specie_name?
                                    rescueData.specie_name:
                                    'No identificada'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Género:&nbsp; 
                                </span>
                                {
                                    rescueData?.genus_name?
                                        rescueData.genus_name:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Marca:&nbsp; 
                                </span>
                                {
                                    rescueData?.mark?
                                        rescueData.mark:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Sexo:&nbsp; 
                                </span>
                                {
                                    rescueData?.gender?
                                        rescueData.gender:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    LT:&nbsp; 
                                </span>
                                {
                                    rescueData?.LT?
                                        rescueData.LT:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    LC:&nbsp; 
                                </span>
                                {
                                    rescueData?.LC?
                                        rescueData.LC:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    LP:&nbsp; 
                                </span>
                                {
                                    rescueData?.LP?
                                        rescueData.LP:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    LO:&nbsp; 
                                </span>
                                {
                                    rescueData?.LO?
                                        rescueData.LO:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    LA:&nbsp; 
                                </span>
                                {
                                    rescueData?.LA?
                                        rescueData.LA:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Peso:&nbsp; 
                                </span>
                                {
                                    rescueData?.weight?
                                        rescueData.weight:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Hábitat:&nbsp; 
                                </span>
                                {
                                    rescueData?.habitat_name?
                                        rescueData.habitat_name:
                                        'No identificado'
                                }
                            </li>
                            <li>
                                <span
                                    className="
                                    font-semibold
                                    text-gray-900
                                    dark:text-white
                                    "
                                >
                                    Grupo de edad:&nbsp; 
                                </span>
                                {
                                    rescueData?.age_group_name?
                                        rescueData.age_group_name:
                                        'No identificada'
                                }
                            </li>
                        </ol>
                    </div>
                    <div className="w-full mt-6">
                        <h1
                            className="
                            text-gray-900
                            text-xl
                            text-center
                            title-font
                            font-medium
                            mb-5
                            "
                        >
                            Datos de liberación 
                        </h1>
                        {
                            releaseData?
                                <ol className="
                                    max-w-md
                                    space-y-1
                                    text-gray-500
                                    list-decimal
                                    list-inside
                                    dark:text-gray-400"
                                >
                                    <li>
                                        <span
                                            className="
                                            font-semibold
                                            text-gray-900
                                            dark:text-white
                                            "
                                        >
                                            Código:&nbsp; 
                                        </span>
                                        {
                                            releaseData.cod?
                                                releaseData.cod:
                                                'No identificado'
                                        }
                                    </li>
                                    <li>
                                        <span
                                            className="
                                            font-semibold
                                            text-gray-900
                                            dark:text-white
                                            "
                                        >
                                            Sustrato:&nbsp; 
                                        </span>
                                        {
                                            releaseData.sustrate?
                                                releaseData.sustrate:
                                                'No disponible'
                                        }
                                    </li>
                                    <li>
                                        <span
                                            className="
                                            font-semibold
                                            text-gray-900
                                            dark:text-white
                                            "
                                        >
                                            Sítio de liberación:&nbsp; 
                                        </span>
                                        {
                                            releaseData.site_release_mammals?
                                                releaseData.site_release_mammals:
                                                'No disponible'
                                        }
                                    </li>
                                </ol>
                                :
                                null

                        }
                    </div>
                </div>
            </div>
            <div
                className="flex justify-center"
            >
                <button 
                    type="button"
                    onClick={() => router.back()}
                    className="bg-emerald-900  hover:bg-emerald-500 text-white font-bold py-2 px-4 rounded"
                >
                    Volver
                </button>
            </div>
        </div>


    )
}
