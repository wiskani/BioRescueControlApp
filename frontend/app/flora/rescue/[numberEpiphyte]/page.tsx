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


    //predicados fuctions
    function isFloraRelocationSpeciesData(
        data: FloraRelocationWithSpecieData | {message: string} | null  
    ): data is FloraRelocationWithSpecieData {
        return  data !== null && 'relocation_date' in data;
    }
    const lineOptions = { color: 'red' }

    const legedColors = ['purple','blue', 'red' ]
    const legendLabels = [
        'Punto de relocalización',
        'Punto de rescate',
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
            >Rescate y traslocación para el número de epífita:&nbsp;
                <span
                    className='italic'
                >
                    {params.numberEpiphyte}
                </span>
            </h1>
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
                            rescueFloraData?
                                <FloraRescueSpecieMap
                                    data={[rescueFloraData]}
                                    radius={55}
                                /> :
                                null
                        }
                        {
                            isFloraRelocationSpeciesData(relocationFloraData)?
                                <FloraRelocationSpecieMap
                                    data={[relocationFloraData]}
                                    radius={55}
                                /> :
                                null
                        }
                        <Legend colors={legedColors} labels={legendLabels} />
                    </MapContainer>
                </div>
            </div>
            <div className="container mx-auto px-4 py-20">
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-2 gap-4">
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
                        <ol className="max-w-md space-y-1 text-gray-500 list-decimal list-inside dark:text-gray-400">
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Fecha de rescate:&nbsp; 
                                </span>
                                {
                                    rescueFloraData?.rescue_date? dateFormat(rescueFloraData.rescue_date): 'No disponible'
                                }

                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Especie:&nbsp; 
                                </span>
                                {rescueFloraData?.specie_name? rescueFloraData.specie_name: 'No identificada'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Género:&nbsp; 
                                </span>
                                {rescueFloraData?.genus_name? rescueFloraData.genus_name: 'No identificado'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Familia:&nbsp; 
                                </span>
                                {rescueFloraData?.family_name? rescueFloraData.family_name: 'No identificada'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Sustrato:&nbsp; 
                                </span>
                                {rescueFloraData?.substrate? rescueFloraData.substrate: 'No identificado'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    DAP del forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.dap_bryophyte? rescueFloraData.dap_bryophyte: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Altura del forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.height_bryophyte? rescueFloraData.height_bryophyte: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Posición del forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.bryophyte_position? rescueFloraData.bryophyte_position: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Hábito:&nbsp; 
                                </span>
                                {rescueFloraData?.growth_habit? rescueFloraData.growth_habit: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Fenología epífito:&nbsp; 
                                </span>
                                {rescueFloraData?.epiphyte_phenology? rescueFloraData.epiphyte_phenology: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Estado sanitario del epífito:&nbsp; 
                                </span>
                                {rescueFloraData?.health_status_epiphyte? rescueFloraData.health_status_epiphyte: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Microhabitat:&nbsp; 
                                </span>
                                {rescueFloraData?.microhabitat? rescueFloraData.microhabitat: 'No disponible'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Especie de forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.specie_bryophyte_name? rescueFloraData.specie_bryophyte_name: 'No identificado'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Género de forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.genus_bryophyte_name? rescueFloraData.genus_bryophyte_name: 'No identificado'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Familia de forofito:&nbsp; 
                                </span>
                                {rescueFloraData?.family_bryophyte_name? rescueFloraData.family_bryophyte_name: 'No identificado'}
                            </li>
                            <li>
                                <span
                                    className="font-semibold text-gray-900 dark:text-white"
                                >
                                    Otras observaciones:&nbsp; 
                                </span>
                                {rescueFloraData?.other_observations? rescueFloraData.other_observations: 'Sin observaciones'}
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
                            Datos de traslocación 
                        </h1>
                        {
                            isFloraRelocationSpeciesData(relocationFloraData) ?
                                <ol className="max-w-md space-y-1 text-gray-500 list-decimal list-inside dark:text-gray-400">
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Fecha de traslocación:&nbsp; 
                                        </span>
                                        {
                                            relocationFloraData.relocation_date? dateFormat(relocationFloraData.relocation_date): 'No disponible'
                                        }

                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Tamaño de la planta:&nbsp; 
                                        </span>
                                        {relocationFloraData.size? relocationFloraData.size: 'No identificado'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Fenología:&nbsp; 
                                        </span>
                                        {relocationFloraData.dap_bryophyte? relocationFloraData.dap_bryophyte: 'No disponible'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Zona de Johanson:&nbsp; 
                                        </span>
                                        {relocationFloraData.johanson_zone? relocationFloraData.johanson_zone: 'No disponible'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Especie de forofito:&nbsp; 
                                        </span>
                                        {relocationFloraData.specie_name_bryophyte? relocationFloraData.specie_name_bryophyte: 'No identificado'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Género de forofito:&nbsp; 
                                        </span>
                                        {relocationFloraData.genus_name_bryophyte? relocationFloraData.genus_name_bryophyte: 'No identificado'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Familia de forofito:&nbsp; 
                                        </span>
                                        {relocationFloraData.family_name_bryophyte? relocationFloraData.family_name_bryophyte: 'No identificado'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Tipo de corteza:&nbsp; 
                                        </span>
                                        {relocationFloraData.bark_type? relocationFloraData.bark_type: 'No disponible'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Lianas infestadas:&nbsp; 
                                        </span>
                                        {relocationFloraData.infested_lianas? relocationFloraData.infested_lianas: 'No disponible'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Otras observaciones:&nbsp; 
                                        </span>
                                        {relocationFloraData.other_observations? relocationFloraData.other_observations: 'Sin observaciones'}
                                    </li>
                                    <li>
                                        <span
                                            className="font-semibold text-gray-900 dark:text-white"
                                        >
                                            Zona de reunicación:&nbsp; 
                                        </span>
                                        {relocationFloraData.relocation_zone? relocationFloraData.relocation_zone: 'No disponible'}
                                    </li>
                                </ol>
                                :
                                <p>No se realizó reubicación</p>

                        }
                    </div>
                </div>
            </div>
        </div>


    )
}
