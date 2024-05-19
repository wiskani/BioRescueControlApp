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
    GetRescueHerpetofaunaWithSpecieByNumber,
    GetTranslocationHerpetoByRescueNumber
} from '@/app/libs/rescue_herpetofaina/ApiRescueHerpetofauna';

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

const RescueHerpetoSpecieMap = dynamic(
    () => (import('@/app/components/HerpetoFauna/RescueHerpetoSpecieMap')),
    { ssr: false }
)

const PointTransloHerpetofaunaRescueMap = dynamic(
    () => (import('@/app/components/HerpetoFauna/PointTransloRescueMap')),
    { ssr: false }
)

const TransectTransloHerpetofaunaRescueMap = dynamic(
    () => (import('@/app/components/HerpetoFauna/TransectoTransloRescueMap')),
    { ssr: false }
)

const TransectTransloHerpetofaunaMap = dynamic(
    () => (import('@/app/components/HerpetoFauna/TransectoTransGenericMap')),
    { ssr: false }
)


export default function Page({params}: {params: { number: string}}) {   
    const { data: session } = useSession();
    const user = session?.user;
    const [rescueData, setRescueData] = useState<RescueHerpetoWithSpeciesData | null>(null)
    const [
    translocationData,
    setTranslocation
            ] = useState<TranslocationHerpetoByNumberRescue | null>(null)
    const [errorMessage, SetErrorMessage]= useState<string>();
    const router = useRouter()

    //Api calls
    const rescueDataHerpeto = useCallback(
        async (): Promise<RescueHerpetoWithSpeciesData| null>=>{
            if (user){
                try {
                    const data= await GetRescueHerpetofaunaWithSpecieByNumber({
                        token: user?.token,
                        number: params.number
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
        }, [user, params.number])


    const traslocationDataHerpeto = useCallback(
        async (): Promise<TranslocationHerpetoByNumberRescue | null> =>{
            if (user){
                try {
                    const data= await GetTranslocationHerpetoByRescueNumber({
                        token: user?.token,
                        rescue_number: params.number
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
        }, [user, params.number])

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }

        else{
            rescueDataHerpeto().then((data)=>{
                setRescueData(data)
            })
            traslocationDataHerpeto().then((data)=>{
                setTranslocation(data)
            })
        }

    }, [session])

    //Predicados fuctions
    function isTransectTranslocationHerpetoWithMarkData(
        data: TranslocationHerpetoByNumberRescue | null
    ): data is TransectTranslocationHerpetoWithMarkData {
        if (data === null) return false;
        return data && "cod" in data && "latitude_in" in data && data !== null;
    }

    function isPointTranslocationHerpetoWithMarkData(
        data: TranslocationHerpetoByNumberRescue | null
    ): data is PointTranslocationHerpetoWithMarkData {
        if (data === null) return false;
        return data
            && "cod" in data && "latitude" in data && "longitude" in data && "number_mark" in data;

    }

    function isTransectHerpetofaunaTranslocationData(
        data: TranslocationHerpetoByNumberRescue | null
    ): data is TransectHerpetofaunaTranslocationData[] {
        if (data === null) return false;
        return Array.isArray(data); 
    }

    //Map options

    const lineOptions = { color: 'red' }
    const legendOptions : () => string[] = () => {
        if (isPointTranslocationHerpetoWithMarkData(translocationData)) {
            return ['blue', 'green', 'red' ]
        }
        if (isTransectTranslocationHerpetoWithMarkData(translocationData)) {
            return ['blue', 'green', 'red' ]
        }
        if (isTransectHerpetofaunaTranslocationData(translocationData)) {
            return ['blue', 'green', 'red' ]
        }
        return ['green', 'red' ]
    }
    const legendLabels: () => string[] = () => {
        if (isPointTranslocationHerpetoWithMarkData(translocationData)) {
            return [
                'puntos lineración',
                'transcetors de rescate herpetofauna',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        if (isTransectTranslocationHerpetoWithMarkData(translocationData)) {
            return [
                'transcetors de liberación herpetofauna',
                'transcetors de rescate herpetofauna',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        if (isTransectHerpetofaunaTranslocationData(translocationData)) {
            return [
                `transectos de liberación para la especie: ${rescueData?.specie_name}`,
                'transcetors de rescate herpetofauna',
                'proyecto 230 kv mizque - sehuencas'
            ]
        }
        return [
            'transcetors de rescate herpetofauna',
            'proyecto 230 kv mizque - sehuencas'
        ]
    }


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
                    {params.number}
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
                                <RescueHerpetoSpecieMap
                                    data={[rescueData]}
                                /> : null
                        }
                        {
                            isPointTranslocationHerpetoWithMarkData(translocationData)?
                            <PointTransloHerpetofaunaRescueMap
                                    data={translocationData}
                                    radius={30}
                                />
                            : null

                        }
                        {
                            isTransectTranslocationHerpetoWithMarkData(translocationData)?
                            <TransectTransloHerpetofaunaRescueMap
                                    data={translocationData}
                                    weight={5}
                            />
                            : null
                        }
                        {
                            isTransectHerpetofaunaTranslocationData(translocationData)?
                            <TransectTransloHerpetofaunaMap
                                    data={translocationData}
                                    weight={5}
                            />
                            : null
                        }
                        <Legend colors={legendOptions()} labels={legendLabels()} />
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
                                    rescueData?.date_rescue?
                                        dateFormat(rescueData.date_rescue):
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
                            isPointTranslocationHerpetoWithMarkData(translocationData) ?
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
                                            Fecha de liberación:&nbsp; 
                                        </span>
                                        {
                                            translocationData.date?
                                                dateFormat(translocationData.date):
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
                                            Numero de marca:&nbsp; 
                                        </span>
                                        {
                                            translocationData.number_mark?
                                                translocationData.number_mark:
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
                                            Código:&nbsp; 
                                        </span>
                                        {
                                            translocationData.code_mark?
                                                translocationData.code_mark:
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
                                            LHC:&nbsp; 
                                        </span>
                                        {
                                            translocationData.LHC?
                                                translocationData.LHC:
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
                                            Peso:&nbsp; 
                                        </span>
                                        {
                                            translocationData.weight?
                                                translocationData.weight:
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
                                            Tipo de marcación:&nbsp; 
                                        </span>
                                        {
                                            translocationData.is_photo_mark?
                                                'fotografía/':
                                               null 
                                        }
                                        {
                                            translocationData.is_elastomer_mark?
                                                'elastomero':
                                               null 
                                        }
                                    </li>
                                </ol>
                                :
                                null

                        }
                        {
                            isTransectTranslocationHerpetoWithMarkData(translocationData) ?
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
                                            Fecha de liberación:&nbsp; 
                                        </span>
                                        {
                                            translocationData.date?
                                                dateFormat(translocationData.date):
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
                                            Numero de marca:&nbsp; 
                                        </span>
                                        {
                                            translocationData.number_mark?
                                                translocationData.number_mark:
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
                                            Código:&nbsp; 
                                        </span>
                                        {
                                            translocationData.code_mark?
                                                translocationData.code_mark:
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
                                            LHC:&nbsp; 
                                        </span>
                                        {
                                            translocationData.LHC?
                                                translocationData.LHC:
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
                                            Peso:&nbsp; 
                                        </span>
                                        {
                                            translocationData.weight?
                                                translocationData.weight:
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
                                            Tipo de marcación:&nbsp; 
                                        </span>
                                        {
                                            translocationData.is_photo_mark?
                                                'fotografía/':
                                               null 
                                        }
                                        {
                                            translocationData.is_elastomer_mark?
                                                'elastomero':
                                               null 
                                        }
                                    </li>
                                </ol>
                                :
                                null
                        }
                        {
                            isTransectHerpetofaunaTranslocationData(translocationData) ?
                                <h1 className="
                                    max-w-md
                                    space-y-1
                                    text-gray-500
                                    list-decimal
                                    list-inside
                                    dark:text-gray-400"
                                >
                                no hay datos de liberación
                                </h1>
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
